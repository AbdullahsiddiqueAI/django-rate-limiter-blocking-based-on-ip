from django.contrib import admin
from .models import IPBlock, RateLimitRule, RequestLog


@admin.register(IPBlock)
class IPBlockAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "reason", "created_at")
    search_fields = ("ip_address",)
    list_filter = ("created_at",)


@admin.register(RateLimitRule)
class RateLimitRuleAdmin(admin.ModelAdmin):
    list_display = ("path", "max_requests", "window_seconds")
    search_fields = ("path",)
    list_filter = ("window_seconds",)


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "path", "request_count", "last_request_at")
    search_fields = ("ip_address", "path")
    list_filter = ("last_request_at",)
