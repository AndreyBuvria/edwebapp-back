# Generated by Django 4.1.2 on 2022-10-23 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_userprofile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]
