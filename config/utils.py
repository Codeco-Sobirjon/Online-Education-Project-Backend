from django.db import models
from rest_framework import serializers


class CustomIDField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 6
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add:
            last_instance = model_instance.__class__.objects.order_by('-id').first()
            if last_instance:
                value = '{:05}'.format(int(last_instance.id) + 1)
            else:
                value = '00001'
            setattr(model_instance, self.attname, value)
        return super().pre_save(model_instance, add)


class CustomAutoField(models.PositiveIntegerField):

    def __init__(self, *args, **kwargs):
        self.start_id = kwargs.pop('start_id', 10 ** 9 + 1)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add:
            last_instance = model_instance.__class__.objects.order_by('-id').first()
            if last_instance:
                value = max(int(last_instance.id) + 1, self.start_id)
            else:
                value = 10 ** 9 + 1
            setattr(model_instance, self.attname, value)
        return super().pre_save(model_instance, add)


class TimestampField(serializers.IntegerField):

    def to_representation(self, value) -> int:
        return int(value.timestamp())
