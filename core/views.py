"""Views."""
from drf_spectacular.utils import OpenApiExample, OpenApiResponse

from core.serializers import ResponseSerializer

SCHEMA_RESPONSE = OpenApiResponse(
    response=ResponseSerializer,
    examples=[
        OpenApiExample(
            "Success",
            value={
                "detail": "string",
            },
        ),
    ],
)
