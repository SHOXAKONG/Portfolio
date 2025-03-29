from .base import Base
from django.db import models

from .category import Category
from .project import Project


class CategoryProject(Base):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.project} | {self.category}'

    class Meta:
        db_table = 'category_project'
        ordering = ['-created_at']
