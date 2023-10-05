# Django
from django.db import models
from django.utils.translation import gettext_lazy as _


class About(models.Model):

    Address = models.CharField(verbose_name=_("Address"), max_length=512)
    phoneNumber = models.CharField(
        verbose_name=_("phone number"), max_length=11)
    email = models.EmailField(verbose_name=_("email"))
    description = models.TextField(verbose_name=_("description"))
    code = models.IntegerField(verbose_name=_("code"), default=1)
    create_time = models.DateTimeField(
        verbose_name=_("create time"), auto_now_add=True)
    update_time = models.DateTimeField(
        verbose_name=_("updade time"), auto_now=True)

    class Meta:
        db_table = "Abouts"
        verbose_name = _("About")
        verbose_name_plural = _("Abouts")
