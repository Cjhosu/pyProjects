# Generated by Django 2.0.2 on 2018-07-04 02:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracker', '0005_auto_20180607_1048'),
    ]

    operations = [
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('journal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracker.Journal')),
                ('shared_with_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='group',
            name='journal',
        ),
        migrations.RemoveField(
            model_name='group',
            name='user',
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.AlterUniqueTogether(
            name='share',
            unique_together={('shared_with_user', 'journal')},
        ),
    ]