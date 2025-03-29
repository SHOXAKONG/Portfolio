from .base import Base
from django.db import models

from .project import Project
from .project_contributor import ProjectContributor


class ProjectUser(Base):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    contributor = models.ForeignKey(ProjectContributor, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'project_users'
        ordering = ['-created_at']

