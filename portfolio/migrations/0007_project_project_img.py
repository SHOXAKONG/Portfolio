# Generated by Django 5.1.8 on 2025-04-20 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0006_alter_user_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_img',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]
