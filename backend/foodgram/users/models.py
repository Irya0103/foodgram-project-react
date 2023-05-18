from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, EmailField, TextField
from django.db.models import UniqueConstraint

from .validators import validate_username


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICERS = (
        (USER, 'пользователь'),
        (MODERATOR, 'модератор'),
        (ADMIN, 'администратор')
    )

    username = CharField(
        'Имя пользователя',
        help_text='Введите имя пользователя',
        max_length=settings.FIELD_LIMIT['username'],
        validators=[validate_username],
        unique=True
    )
    first_name = CharField(
        'Имя',
        help_text='Введите имя',
        max_length=settings.FIELD_LIMIT['first_name'],
        blank=True
    )
    last_name = CharField(
        'Фамилия',
        help_text='Введите фамилию',
        max_length=settings.FIELD_LIMIT['last_name'],
        blank=True
    )
    bio = TextField(
        'Описание пользователя',
        help_text='Введите описание пользователя',
        null=True,
        blank=True
    )
    email = EmailField(
        'Адрес электронной почты',
        help_text='Введите адрес электронной почты',
        unique=True,
        max_length=settings.FIELD_LIMIT['email']
    )
    role = CharField(
        'Права пользователя',
        help_text='Выбирите права пользователя',
        max_length=max(len(role) for _, role in ROLE_CHOICERS),
        choices=ROLE_CHOICERS,
        default=USER
    )
    confirmation_code = CharField(
        'Код подтверждения',
        help_text='Введите код подтверждения',
        max_length=settings.FIELD_LIMIT['confirmation_code'],
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_username_email'
            )
        ]
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscribe(models.Model):
    User = models.ForeignKey(
        User,
        related_name='subscriber',
        verbose_name='подписчик',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='subscribing',
        verbose_name='автор',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            UniqueConstraint(fields=['user', 'author'],
                             name='unique_subscription')
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
