"""Throttling."""

import time

from django.core.cache import cache as default_cache
from django.core.cache import caches
from django.core.exceptions import ImproperlyConfigured
from rest_framework.settings import api_settings

from .utils import get_ident

CACHE_FORMAT = "throttle_%(scope)s_%(ident)s_%(path)s_%(method)s"


class ResponseRateThrottle:
    if "throttle" in caches:
        cache = caches["throttle"]
    else:
        cache = default_cache

    timer = time.time
    THROTTLE_RATES = api_settings.DEFAULT_THROTTLE_RATES

    def __init__(self):
        if not getattr(self, "rate", None):
            self.rate = self.get_rate()

        self.num_requests, self.duration = self.parse_rate(self.rate)

    def get_cache_key(self, request):
        """Get Cache Key."""

        return CACHE_FORMAT % {
            "scope": self.scope,
            "ident": get_ident(request),
            "path": request.path,
            "method": str(request.META["REQUEST_METHOD"]),
        }

    def get_rate(self):
        """Determine the string representation of the allowed request rate."""
        if not getattr(self, "scope", None):
            msg = (
                "You must set either `.scope` for '%s' throttle"
                % self.__class__.__name__
            )
            raise ImproperlyConfigured(msg)

        try:
            return self.THROTTLE_RATES[self.scope]
        except KeyError:
            msg = "No default throttle rate set for '%s' scope" % self.scope
            raise ImproperlyConfigured(msg)

    def parse_rate(self, rate):
        """Given the request rate string, return a two tuple of:

        <allowed number of requests>, <period of time in seconds>
        """
        if rate is None:
            return (None, None)

        num, period = rate.split("/")
        num_requests = int(num)
        duration = {"s": 1, "m": 60, "h": 3600, "d": 86400}[period[0]]
        return (num_requests, duration)

    def wait(self):
        """Returns the recommended next request time in seconds."""
        if self.history:
            remaining_duration = self.duration - (self.now - self.history[-1])
        else:
            remaining_duration = self.duration

        available_requests = self.num_requests - len(self.history) + 1
        if available_requests <= 0:
            return None

        return remaining_duration / float(available_requests)

    def allow_request(self, request, view):
        """Allow Request."""
        if self.rate is None:
            return True

        self.key = self.get_cache_key(request)
        if self.key is None:
            return True

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        if len(self.history) >= self.num_requests:
            return False

        return True

    def allow_response(self, request, response):
        """Allow Response."""
        if self.is_allow_response(request, response):
            return True

        if self.rate is None:
            return True

        self.key = self.get_cache_key(request)
        if self.key is None:
            return True

        self.now = self.timer()
        self.history = self.cache.get(self.key, [])

        # Drop any requests from the history which have now passed the
        # throttle duration
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()

        if len(self.history) >= self.num_requests:
            return False

        self.history.insert(0, self.now)
        self.cache.set(self.key, self.history, self.duration)

        return True

    def is_allow_response(self, request, response):
        """Is Allow Response."""
        status_code = response.status_code
        if status_code < 200 or status_code >= 300:
            return False

        return True


class AnonResponseRateThrottle(ResponseRateThrottle):
    scope = "anon"
