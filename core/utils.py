"""Utils."""
import logging

from django.conf import settings
from rest_framework.settings import api_settings

# logger
LOGGER = logging.getLogger(settings.CORE_LOGGER)


def get_ident(request):
    """Identify the machine making the request by parsing HTTP_X_FORWARDED_FOR
    if present and number of proxies is > 0.

    If not use all of HTTP_X_FORWARDED_FOR if it is available, if not
    use REMOTE_ADDR.
    """
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    remote_addr = request.META.get("REMOTE_ADDR")
    num_proxies = api_settings.NUM_PROXIES

    if num_proxies is not None:
        if num_proxies == 0 or xff is None:
            return remote_addr
        addrs = xff.split(",")
        client_addr = addrs[-min(num_proxies, len(addrs))]
        return client_addr.strip()

    return "".join(xff.split()) if xff else remote_addr
