from django.contrib import admin

from internal.models import ImprovedModelAdmin

from .models import User


@admin.register(User)
class UserAdmin(ImprovedModelAdmin):
    def show_groups(self, obj):
        groups = []
        for group in obj.groups.all():
            groups.append(group.name)
        return ",".join(groups)

    search_fields = ("id", "email", "first_name", "last_name")
    list_display = (
        "id",
        "is_active",
        "email",
        "first_name",
        "last_name",
        "show_groups",
    )
