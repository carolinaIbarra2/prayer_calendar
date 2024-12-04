# calendar_app/models.py
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class PrayerDay(models.Model):
    date = models.DateField(unique=True)   #fecha de la oración
    participants = models.ManyToManyField(Person, through="PrayerCompletion")

    def __str__(self):
        return f"Prayer day for {self.date}"
    

class PrayerCompletion(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    prayer_day = models.ForeignKey(PrayerDay, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)  # Si la persona completó la oración para este día

    def __str__(self):
        return f"{self.person.name} - {self.prayer_day.date} - {'Completed' if self.completed else 'Not Completed'}"

class Registro(models.Model):
    day = models.DateField()
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    color = models.CharField(max_length=20, default='yellow')

    def __str__(self):
        return f"{self.person.name} - {self.day} - {self.color}"