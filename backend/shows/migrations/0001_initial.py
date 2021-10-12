# Generated by Django 3.2.8 on 2021-10-12 23:38

from django.db import migrations, models
import django.db.models.deletion
import recurrence.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('slug', models.SlugField(blank=True, help_text="Required if 'render as page' is set.", unique=True, verbose_name='URL slug')),
            ],
        ),
        migrations.CreateModel(
            name='ShowDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.TimeField(verbose_name='start time')),
                ('duration', models.DurationField()),
                ('dates', recurrence.fields.RecurrenceField()),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dates', to='shows.show')),
            ],
        ),
    ]
