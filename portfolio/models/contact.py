from .base import Base
from django.db import models

from .users import User


class Contact(Base):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=False)
    message = models.TextField()
    data_sent = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'contact'
        ordering = ['-created_at']