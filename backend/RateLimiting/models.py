from django.db import models

class IPBlock(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_address


class RateLimitRule(models.Model):
    ip_address = models.GenericIPAddressField(null=True,blank=True)  # The specific IP to apply the rule
    path = models.CharField(max_length=255)  # The API route (e.g., /api/some-endpoint/)
    max_requests = models.PositiveIntegerField(default=10)  # Maximum allowed requests
    window_seconds = models.PositiveIntegerField(default=60)  # Time window in seconds

    class Meta:
        unique_together = ('ip_address', 'path')  # Ensure unique rules per IP and path

    def __str__(self):
        return f"{self.ip_address} - {self.path} - {self.max_requests} reqs in {self.window_seconds}s"

class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    path = models.CharField(max_length=255)  # API route accessed
    request_count = models.PositiveIntegerField(default=1)  # Increment with each request
    last_request_at = models.DateTimeField(auto_now=True)  # Update on every request

    def __str__(self):
        return f"{self.ip_address} - {self.path}"
