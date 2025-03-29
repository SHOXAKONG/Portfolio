from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Feedback, Contact
from .middleware import get_current_request


@receiver(pre_save, sender=[Feedback, Contact])
def set_approved_by(sender, instance, **kwargs):
    if instance.approved_by is None:
        request = get_current_request()
        if request and request.user.is_authenticated:
            instance.approved_by = request.user
