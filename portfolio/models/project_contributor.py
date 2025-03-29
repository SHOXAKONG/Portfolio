from .base import Base
from django.db import models


class Position(models.TextChoices):
    FRONTEND = ("Frontend", "Frontend")
    BACKEND = ("Backend", "Backend")
    DEVOPS = ("DevOPS", "DevOPS")
    PM = ("PM", "PM")
    TESTER = ("Tester", "Tester")


class ProjectContributor(Base):
    full_name = models.CharField(max_length=200)
    github_link = models.URLField()
    linkedin_link = models.URLField()
    email = models.EmailField()
    position = models.CharField(max_length=100, choices=Position.choices)

    class Meta:
        db_table = 'project_contributor'
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name

