# Generated by Django 2.0.2 on 2018-02-25 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Date_record_notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.CharField(max_length=500)),
                ('date_record', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracker.Date_record')),
            ],
        ),
    ]