from django.db import models


class TimeStampedModel(models.Model):
    """ TimeStampedModel definition"""
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # DB에 저장되지 않는 Model abstract
    class Meta:
        abstract = True