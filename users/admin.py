from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BayouUser

@admin.register(BayouUser)
class BayouUserAdmin(UserAdmin):
    model = BayouUser

    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {
            "fields": (
                "profile_picture",
                "short_bio",
                "phone_number",
                "favorite_artist",
                "liked_songs",
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra Info", {
            "fields": (
                "profile_picture",
                "short_bio",
                "phone_number",
                "favorite_artist",
            )
        }),
    )