# Generated by Django 4.1.2 on 2023-01-10 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_api', '0008_alter_coursemodel_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemodel',
            name='key',
            field=models.CharField(default='947fir', editable=False, max_length=6, unique=True),
        ),
    ]
