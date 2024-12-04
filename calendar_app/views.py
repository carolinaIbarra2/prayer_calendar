from django.shortcuts import render
from calendar import monthrange, month_name
import datetime
from django.utils import timezone
from .models import Person, PrayerDay, PrayerCompletion, Registro


def december_calendar(request):
    # Obtener la fecha actual
    today = timezone.localdate()
    month = today.month
    year = today.year
    current_day = today.day
        
    # Generar el calendario del mes actual
    first_day, num_days = monthrange(year, month)


    # Ajustar el índice para que las semanas comiencen en domingo
    first_day = (first_day + 1) % 7  # Mover lunes a domingo (0-6)

    month_calendar = []
    week = [0] * first_day  # Días vacíos antes del primer día del mes
    for day in range(1, num_days + 1):
        week.append(day)
        if len(week) == 7:
            month_calendar.append(week)
            week = []
    if week:  # Última semana
        month_calendar.append(week)

    # Recuperar personas y manejar el formulario
    people = Person.objects.all()
    selected_person = None
    message = None

    if request.method == "POST" and "submit_button" in request.POST:
        person_id = request.POST.get("person")
        if person_id:
            try:
                person = Person.objects.get(id=person_id)
                selected_person = person

                # Verificar si ya existe un registro para el día actual
                prayer_day, created = PrayerDay.objects.get_or_create(date=today)
                prayer_completion, created = PrayerCompletion.objects.get_or_create(
                    person=person, prayer_day=prayer_day
                )

                if prayer_completion.completed:
                    message = f"{person.name} ,  ya realizaste el registro para hoy. "
                else:
                    prayer_completion.completed = True
                    prayer_completion.save()
                    message = f"{person.name} , tu registro fue EXITOSO. Bendiciones"
            
            
                # Actualizar el color del día (amarillo si no todos completaron, verde si todos lo hicieron)
                total_participants = 4
                completed_count = PrayerCompletion.objects.filter(
                    prayer_day=prayer_day, completed=True
                ).count()

                
                color = "yellow"  # Valor predeterminado
                if completed_count == total_participants:
                    color = "green"  # Todos han completado


                # Actualizar o crear registros de color para el día
                registro, _ = Registro.objects.get_or_create(day=today, person=person)
                registro.color = color
                registro.save()
            
            
            except Person.DoesNotExist:
                message = "La persona seleccionada no existe."

    # Obtener colores marcados por día
    registros = Registro.objects.filter(day__month=month, day__year=year)
    day_colors = {registro.day.day: registro.color for registro in registros}

    

    completions_by_day = {}
     # Obtener completions por día (como antes)
    prayer_completions = PrayerCompletion.objects.filter(
        prayer_day__date__month=month, prayer_day__date__year=year
    ).select_related("person", "prayer_day")
    
    for completion in prayer_completions:
        day = completion.prayer_day.date.day
        name = completion.person.name
        if day not in completions_by_day:
            completions_by_day[day] = []
        completions_by_day[day].append(name)

    context = {
        "month_calendar": month_calendar,
        "month_name": month_name[month],
        "year": year,
        "people": people,
        "selected_person": selected_person,
        "current_day": current_day,
        "message": message,
        "completions_by_day": completions_by_day,
        "day_colors": day_colors,
    }

    print(day_colors)

    return render(request, "calendar.html", context)
