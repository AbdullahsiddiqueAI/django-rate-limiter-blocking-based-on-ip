from django.http import JsonResponse
from django.core.cache import cache

def request_status_view(request):
    # ip = request.META.get("REMOTE_ADDR")
    ip = request.META.get("REMOTE_ADDR")
    # return ip
    path = request.path

    # Calculate the request count
    key = f"rate_limit_{ip}_{path}"
    request_count = cache.get(key, 0)

    return JsonResponse({
        "ip": ip,
        "requests_made": request_count,
        "message": "Request status retrieved successfully."
    })
