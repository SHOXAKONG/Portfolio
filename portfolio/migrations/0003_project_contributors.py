# Generated by Django 5.1.7 on 2025-03-28 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_alter_role_name_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='contributors',
            field=models.ManyToManyField(related_name='projects', through='portfolio.ProjectUser', to='portfolio.projectcontributor'),
        ),
    ]
