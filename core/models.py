"""Database Models."""
import uuid

from django.db import models


# Create your models here.
class AbstractBaseModel(models.Model):
    """Base Model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ins_ts = models.DateTimeField(auto_now_add=True)
    ins_user_id = models.CharField(max_length=255)
    ins_prog_id = models.CharField(max_length=255)
    upd_ts = models.DateTimeField(auto_now=True)
    upd_user_id = models.CharField(max_length=255)
    upd_prog_id = models.CharField(max_length=255)

    class Meta:
        abstract = True
