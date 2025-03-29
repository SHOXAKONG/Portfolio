from django.db import models
from .base import Base
from .users import User


class Portfolio(Base):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()


    def __str__(self):
        return f"{self.title} by {self.user}"

    class Meta:
        db_table = 'portfolio'
        ordering = ['-created_at']

