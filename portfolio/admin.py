from django.contrib import admin
from .models import *
admin.site.register([User, ProjectContributor, Project, ProjectUser, Contact,Category, CategoryProject, Feedback, Files, Role, Portfolio])