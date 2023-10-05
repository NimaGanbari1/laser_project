# Django
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Cart(models.Model):
    Code = models.IntegerField()
    Count = models.PositiveIntegerField()
    user = models.ForeignKey(to=User, related_name='ca',
                             on_delete=models.CASCADE)
    create_time = models.DateTimeField(
        verbose_name=_("create time"), auto_now_add=True)
    update_time = models.DateTimeField(
        verbose_name=_("updade time"), auto_now=True)

    class Meta:
        db_table = "Carts"
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

    def __str__(self):
        return str(self.user)
