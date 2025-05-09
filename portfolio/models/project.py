from .base import Base
from django.db import models



class Project(Base):
    project_img = models.URLField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateField()
    end_time = models.DateField()
    git_hub = models.URLField()
    deploy_link = models.URLField()
    contributors = models.ManyToManyField(
        'ProjectContributor',
        through='ProjectUser',
        related_name='projects'
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'project'
        ordering = ['-created_at']
