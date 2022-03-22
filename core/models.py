from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from simple_history.models import HistoricalRecords

from internal.models import BaseModel

from .managers import UserManager


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        'E-mail', unique=True, help_text='E-mail do usuário'
    )
    first_name = models.CharField(
        'Nome', max_length=30, blank=True, help_text='Primeiro nome'
    )
    last_name = models.CharField(
        'Sobrenome', max_length=30, blank=True, help_text='Nome de família'
    )
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    is_active = models.BooleanField(
        'Usuário ativo?',
        default=True,
        help_text='Indica se o usuário está ativo ou não',
    )
    is_staff = models.BooleanField(
        'Equipe?', default=True, help_text='Faz parte da equipe da loja?'
    )
    is_superuser = models.BooleanField(
        'Adminstrador?',
        default=False,
        help_text='É um administrador do sistema?',
    )
    history = HistoricalRecords()
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    WRITE_FIELDS = [
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'is_superuser',
    ]

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name or 'Sem'

    @property
    def get_abbrv(self):
        try:
            return f'{self.first_name[0]}{self.last_name[0]}'
        except IndexError:
            return 'SN'

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def roles(self):
        roles = []
        if self.is_staff:
            roles.append('STAFF')

        if self.is_superuser:
            roles.append('ADMIN')

        return roles

    def __repr__(self):
        cls = self.__class__.__name__
        fields = [
            f'{field.name}={field.value_from_object(self)}'
            for field in self._meta.fields
            if field.name
            not in [
                'password',
                'last_login',
                'created_at',
                'updated_at',
                'date_joined',
            ]
            and field.value_from_object(self)
        ]
        return f"<{cls} {','.join(fields)}>"

    @property
    def serialize(self):
        return {
            'id': self.pk,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_joined': self.date_joined,
            'active': self.is_active,
            'name': self.get_full_name(),
            'short_name': self.get_short_name(),
            'abbrv': self.get_abbrv,
            'roles': self.roles,
        }

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        db_table = 'users'
