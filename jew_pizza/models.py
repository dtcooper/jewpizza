from django.db import models


from recurrence.fields import RecurrenceField


class Show(models.Model):
    name = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField()
    recurrences = RecurrenceField()

    def __str__(self):
        return self.name
