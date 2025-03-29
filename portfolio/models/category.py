from .base import Base
from django.db import models

class Category(Base):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        ordering = ['-created_at']

        