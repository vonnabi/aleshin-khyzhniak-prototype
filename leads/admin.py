from django.contrib import admin
from django.db.models import Q

from .models import Lead, PracticeAccess

admin.site.site_header = "Заявки — Альошин, Хижняк та Партнери"
admin.site.site_title = "Заявки"
admin.site.index_title = "Облік заявок"


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "id", "created_at", "name", "contact", "practice", "status",
        "source", "assigned_to", "is_repeat",
    )
    list_display_links = ("id", "name")
    list_editable = ("status", "assigned_to")
    list_filter = ("status", "practice", "utm_source", "assigned_to", "created_at")
    search_fields = ("name", "contact", "message", "note")
    date_hierarchy = "created_at"
    list_per_page = 50
    readonly_fields = (
        "created_at", "updated_at", "page", "landing", "referrer", "utm_source",
        "utm_medium", "utm_campaign", "utm_content", "utm_term", "gclid", "fbclid",
        "duplicate_of",
    )
    fieldsets = (
        ("Звернення", {"fields": ("name", "contact", "message", "created_at")}),
        ("Робота із заявкою", {"fields": ("practice", "status", "assigned_to", "note")}),
        ("Договір та оплата", {"fields": ("contract_date", "contract_amount", "paid_amount")}),
        ("Джерело", {
            "classes": ("collapse",),
            "fields": (
                "page", "landing", "referrer", "utm_source", "utm_medium",
                "utm_campaign", "utm_content", "utm_term", "gclid", "fbclid",
                "duplicate_of", "updated_at",
            ),
        }),
    )

    @admin.display(description="джерело")
    def source(self, obj):
        return obj.source

    @admin.display(description="повтор", boolean=True)
    def is_repeat(self, obj):
        return bool(obj.duplicate_of_id)

    def get_queryset(self, request):
        """Адвокатська таємниця: без окремого права видно лише свої практики."""
        queryset = super().get_queryset(request)
        user = request.user
        if user.is_superuser or user.has_perm("leads.view_all_leads"):
            return queryset
        practices = list(user.practice_access.values_list("practice", flat=True))
        return queryset.filter(Q(practice__in=practices) | Q(assigned_to=user))


@admin.register(PracticeAccess)
class PracticeAccessAdmin(admin.ModelAdmin):
    list_display = ("user", "practice")
    list_filter = ("practice",)
