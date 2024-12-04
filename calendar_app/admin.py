from django.contrib import admin
from .models import Person, PrayerCompletion, PrayerDay, Registro

admin.site.register(Person)
admin.site.register(PrayerDay)
admin.site.register(PrayerCompletion)
admin.site.register(Registro)