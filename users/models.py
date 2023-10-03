import random
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, send_mail
from django_mysql.models import ListCharField

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, phone_number, email, password, is_staff, is_superuser, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number,
                          is_staff=is_staff,
                          is_superuser=is_superuser,
                          date_joined=now,
                          username=username,
                          email=email,
                          **extra_fields)

        # user.password = make_password(password)
        # user.save(using=self._db)
        if not extra_fields.get('no_password'):
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_user(self, username=None, phone_number=None, email=None, password=None, **extra_fields):
        # if username is None:
        #    if email:
        #        username =email.split('@',1)[0]
        #    if phone_number:
        #        username = random.choice('abcdefghijklmnopqrstuvwxyz') + str(phone_number)[-7:]
        #    while User.objects.filter(username=username).exists():
        #        username += str(random.randint(10, 99))

        # extra_fields.setdefault('is_staff', False)
        # extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, phone_number, email, password, False, False, **extra_fields)

    def create_superuser(self, username, phone_number, email, password, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)

        # if extra_fields.get('is_staff') is not True:
        #    raise ValueError('Superuser must have is_staff=True.')
        # if extra_fields.get('is_superuser') is not True:
        #    raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, phone_number, email, password, True, True, **extra_fields)

    def get_by_phone_number(self, phone_number):
        return self.get(**{'phone_number': phone_number})


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'),
        max_length=32,
        unique=True,
        help_text=_(
            'Required. 32 characters or fewer. Letters, digits and . _ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
            'validators': _('invalid'),
        },)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(
        _('email address'), unique=True, null=True, blank=True)
    phone_number = models.BigIntegerField(
        _('phone number'),
        unique=True,
        validators=[validators.RegexValidator(
            r'^989[0-3,9]\d{8}$', _('Enter a valid number phone'), 'invalid')],
        error_messages={
            'unique': _("A user with that phone number already exists."),
        },
        null=True, 
        blank=True
        )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    address = models.TextField(_('address'),blank=True,null=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_seen = models.DateTimeField(_('last senn date'), null=True)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name


    @property
    def is_loggein_user(self):
        return self.phone_number is not None or self.email is not None

    def save(self, *args, **kwargs):
        if self.email is not None and self.email.strip() == '':
            self.email = None
        super().save(*args, **kwargs)


"""class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    nick_name = models.CharField(verbose_name=_('nick name'),max_length=150,blank=True)
    avatar = models.ImageField(_('avatar'),blank=True,null=True)
    birthday = models.DateField(_('birthday'),null=True,blank=True)
    gender = models.BooleanField(_('gender'),help_text=_('female is False,male is True,null is unset'))
    province = models.ForeignKey(verbose_name=_('province'),to='Province',null=True, on_delete= models.SET_NULL)
    
    
    class Meta:
        db_table = "user_profiles"
        verbose_name = _('profile')
        verbose_name_plural = "user_profiles"
    @property
    def get_first_name(self):
        return self.user.first_name
        
    @property
    def get_last_name(self):
        return self.user.last_name
    
    @property
    def get_nickname(self):
        return self.nick_name if self.nick_name else self.user.username
    
    def __str__(self):
        return self.user.first_name
"""


class Device(models.Model):
    WEB = 1
    IOS = 2
    ANDROID = 3
    DEVICE_TYPE_CHOICE = (
        (WEB, 'web'),
        (IOS, 'ios'),
        (ANDROID, 'android'),
    )

    user = models.ForeignKey(
        User, related_name='devices', on_delete=models.CASCADE)
    device_uuid = models.UUIDField(_('Device UUID'), null=True)
    last_login = models.DateTimeField(_('last login date'), null=True)
    device_type = models.PositiveSmallIntegerField(
        choices=DEVICE_TYPE_CHOICE, default=WEB)
    device_os = models.CharField(_('device os'), max_length=20, blank=True)
    device_model = models.CharField(
        _('device model'), max_length=50, blank=True)
    app_version = models.CharField(_('app version'), max_length=20, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Devices'
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')
        unique_together = ('user', 'device_uuid')


class Province(models.Model):
    name = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

