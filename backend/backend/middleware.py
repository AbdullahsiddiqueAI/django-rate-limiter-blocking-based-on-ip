from django.core.cache import cache
from django.http import JsonResponse
from RateLimiting.models import IPBlock, RateLimitRule
import logging

logger = logging.getLogger(__name__)

class DynamicIPRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)
        logger.info(f"Client IP: {ip}")

        # Check if the IP is blocked
        if IPBlock.objects.filter(ip_address=ip).exists():
            return JsonResponse({"error": "Access blocked for this IP"}, status=403)

        # Get the path
        path = request.path
        logger.info(f"Requested Path: {path}")

        # Check for a rate limit rule specific to this IP and path
        rate_limit_rule = RateLimitRule.objects.filter(ip_address=ip, path=path).first()

        if rate_limit_rule:
            rate_limit_result = self.apply_rate_limit(ip, path, rate_limit_rule)
            if isinstance(rate_limit_result, JsonResponse):  # Rate limit exceeded
                return rate_limit_result

            remaining, total_requests = rate_limit_result
            response = self.get_response(request)

            # Add headers to track rate-limiting information
            if response.status_code == 200:
                response["X-RateLimit-Remaining"] = remaining
                response["X-RateLimit-Total"] = total_requests

            return response

        return self.get_response(request)

    def apply_rate_limit(self, ip, path, rule):
        """
        Applies rate limiting for the given IP and path.
        Returns the remaining requests and total request count as a tuple,
        or a JsonResponse if the rate limit is exceeded.
        """
        key = f"rate_limit_{ip}_{path}"  # Create a unique cache key for this IP and path
        request_count = cache.get(key, 0)

        if request_count >= rule.max_requests:
            logger.warning(f"Rate limit exceeded for IP {ip} on path {path}")
            return JsonResponse({
                "error": "Rate limit exceeded. Try again later.",
                "requests_made": request_count,
                "max_requests": rule.max_requests
            }, status=429)

        # Increment the request count and update the cache
        cache.set(key, request_count + 1, timeout=rule.window_seconds)
        remaining = rule.max_requests - (request_count + 1)
        return remaining, request_count + 1

    def get_client_ip(self, request):
        """
        Retrieves the real client IP address from the request.
        Handles forwarded headers and falls back to REMOTE_ADDR.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        logger.info(f"Determined Client IP: {ip}")
        return ip
