from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import User
from .utils import send_mail_change_status


@receiver(pre_save, sender=User)
def upgrade_from_guest(sender, instance: User, **kwargs):
    if not instance.pk is None:
        previous = User.objects.get(pk=instance.pk)
        if previous.is_guest != instance.is_guest:
            send_mail_change_status(instance)

