from .users import User
from .base import Base
from django.db import models

from .project import Project


class Feedback(Base):
    author_name = models.CharField(max_length=200)
    feedback = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.author_name

    class Meta:
        db_table = 'feedback'
        ordering = ['-created_at']