# Generated by Django 3.1.13 on 2022-04-19 22:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('civictechprojects', '0058_auto_20220414_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventConferenceRoomParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zoom_user_name', models.CharField(max_length=100)),
                ('zoom_user_id', models.BigIntegerField(default=0)),
                ('enter_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='civictechprojects.eventconferenceroom')),
            ],
        ),
    ]