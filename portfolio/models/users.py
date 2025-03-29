from django.contrib.auth.models import AbstractUser
from django.db import models

from .roles import Role


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'
        ordering = ['-created_at']

    @property
    def is_moderator(self):
        return self.role and self.role.name == 'moderator'
