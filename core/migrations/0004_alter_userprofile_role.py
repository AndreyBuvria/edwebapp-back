# Generated by Django 4.1.2 on 2022-10-22 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_roles_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.role'),
        ),
    ]