from .base import Base
from django.db import models

class Role(Base):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'role'
        ordering = ['-created_at']