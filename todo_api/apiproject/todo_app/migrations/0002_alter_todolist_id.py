# Generated by Django 5.1.1 on 2024-10-04 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='id',
            field=models.CharField(editable=False, max_length=15, primary_key=True, serialize=False, unique=True),
        ),
    ]
