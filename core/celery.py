"""Celery."""

import time

from celery import Task
from django.conf import settings
from django_celery_results.models import TaskResult

from core.utils import LOGGER


class CeleryTask(Task):
    def before_start(self, task_id, args, kwargs):
        self.is_continue = not (
            hasattr(settings, "CELERY_TASK_ALWAYS_EAGER")
            and settings.CELERY_TASK_ALWAYS_EAGER is True
        )

        if not self.is_continue:
            return

        self.task_name = self.request.task
        self.task_id = task_id
        self.start_time = time.time()

        LOGGER.info(f"Start: {self.task_name}")
        LOGGER.info(f"Task ID: {self.task_id}")

    def on_success(self, retval, task_id, args, kwargs):
        if not self.is_continue:
            return

        self.log_end()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        if not self.is_continue:
            return

        LOGGER.error(f"Failure: {einfo}\n{exc}")
        self.log_end()

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        if (
            hasattr(settings, "CELERY_TASK_ALWAYS_EAGER")
            and settings.CELERY_TASK_ALWAYS_EAGER is False
        ):
            return

        LOGGER.warn(f"Retry: {einfo}\n{exc}")

    def log_end(self):
        task = TaskResult.objects.get(task_id=self.task_id)
        if hasattr(self, "update_task_args"):
            task.task_args = self.update_task_args

        else:
            task.task_args = None

        task.save()

        LOGGER.info(f"Duration: {time.time() - self.start_time}")
        LOGGER.info(f"End: {self.task_name}")
