import uuid
from enum import IntEnum

from django.contrib import admin
from django.db import models
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget


class ImprovedModelAdmin(admin.ModelAdmin):
    formfield_overrides = {JSONField: {"widget": JSONEditorWidget}}
    list_per_page = 25


class EnumChoicesBase(IntEnum):
    """Enum was used as choices of Game.status because explicit is better than implicit"""

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text="UUID",
    )
    created_at = models.DateTimeField(
        "Criado em",
        auto_now_add=True,
        editable=False,
        help_text="Data de criação",
        db_index=True,
    )
    updated_at = models.DateTimeField(
        "Atualizado em",
        auto_now=True,
        help_text="Data de atualização",
        db_index=True,
    )

    def __repr__(self):
        cls = self.__class__.__name__
        fields = [
            f"{field.name}={field.value_from_object(self)}"
            for field in self._meta.fields
            if field.name not in ["created_at", "updated_at"]
            and field.value_from_object(self)
        ]
        return f"<{cls} {','.join(fields)}>"

    def __str__(self):
        return self.__repr__()

    class Meta:
        abstract = True


def empty_object():
    return {}


def empty_list():
    return []
