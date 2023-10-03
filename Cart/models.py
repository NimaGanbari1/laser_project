from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.translation import gettext_lazy as _


class Cart(models.Model):
    Code = models.IntegerField()
    Count = models.PositiveIntegerField()
    user = models.ForeignKey(to=User,related_name='ca', on_delete=models.CASCADE)
    
    class Meta:
        db_table = "Carts"
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")
    