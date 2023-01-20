# Generated by Django 4.1.2 on 2023-01-19 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_api', '0011_coursemodel_access_alter_coursemodel_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemodel',
            name='access',
            field=models.IntegerField(default=0, verbose_name=((0, 'Public'), (1, 'Private'))),
        ),
        migrations.AlterField(
            model_name='coursemodel',
            name='key',
            field=models.CharField(default='igwkhk', editable=False, max_length=6),
        ),
    ]