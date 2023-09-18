"""Middleware."""
import time

from core.throttling import ResponseRateThrottle
from core.utils import LOGGER


class AllInOneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        LOGGER.info(f"Start: {str(request.path)}")
        LOGGER.info(f"Request Method: {str(request.META['REQUEST_METHOD'])}")

        # get response and duration
        start_time = time.time()
        response = self.get_response(request)

        # view_func
        if hasattr(request, "resolver_match") and hasattr(
            request.resolver_match, "func"
        ):
            view_func = request.resolver_match.func
            if hasattr(view_func, "view_class"):
                self.view_class = view_func.view_class
            else:
                self.view_class = None

        # throttling
        self.throttling(request, response)

        LOGGER.info(f"Response: [{str(response.status_code)}] {response.reason_phrase}")
        LOGGER.info(f"Duration: {time.time() - start_time}")
        LOGGER.info(f"End: {str(request.path)}")

        return response

    def throttling(self, request, response):
        class_names = [
            type(response_throttle_class).__name__
            for response_throttle_class in self.get_response_throttle_classes()
            if not response_throttle_class.allow_response(request, response)
        ]

        if class_names and LOGGER:
            for name in class_names:
                LOGGER.warn(f"Throttling: {name}")

    def get_response_throttle_classes(self):
        if hasattr(self.view_class, "throttle_classes"):
            return [
                throttle_class()
                for throttle_class in self.view_class.throttle_classes
                if issubclass(throttle_class, ResponseRateThrottle)
            ]
        return []
