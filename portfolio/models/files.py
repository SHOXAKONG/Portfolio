from .base import Base
from django.db import models

from .project import Project


class Files(Base):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    downloaded_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'file'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

