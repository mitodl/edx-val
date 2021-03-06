# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-27 09:06


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edxval', '0008_remove_subtitles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transcriptpreference',
            name='three_play_turnaround',
            field=models.CharField(blank=True, choices=[(u'extended', u'10-Day/Extended'), (u'standard', u'4-Day/Standard'), (u'expedited', u'2-Day/Expedited'), (u'rush', u'24 hour/Rush'), (u'same_day', u'Same Day'), (u'two_hour', u'2 Hour')], max_length=20, null=True, verbose_name=u'3PlayMedia Turnaround'),
        ),
    ]
