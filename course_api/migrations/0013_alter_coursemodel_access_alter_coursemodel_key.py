# Generated by Django 4.1.2 on 2023-01-19 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_api', '0012_alter_coursemodel_access_alter_coursemodel_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemodel',
            name='access',
            field=models.CharField(choices=[(0, 'Public'), (1, 'Private')], max_length=10),
        ),
        migrations.AlterField(
            model_name='coursemodel',
            name='key',
            field=models.CharField(default='gypfde', editable=False, max_length=6),
        ),
    ]
