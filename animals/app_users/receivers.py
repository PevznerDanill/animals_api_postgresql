from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import User
from .utils import send_mail_change_status
from django.core.exceptions import ObjectDoesNotExist


@receiver(pre_save, sender=User)
def upgrade_from_guest(sender, instance: User, **kwargs) -> None:
    """
    Receives a pre_save signal. If the User instance that sent the signal existed and
    its is_guest field was changed, calls send_mail_change_status() function.
    """
    try:
        previous = User.objects.get(pk=instance.pk)
        if previous.is_guest != instance.is_guest:
            send_mail_change_status(instance)
    except ObjectDoesNotExist:
        pass

