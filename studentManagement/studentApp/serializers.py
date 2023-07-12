from rest_framework import serializers
from .models import *


def common_serializer(model, fields=[]):
    meta_model = model
    meta_fields = fields

    class Serializer(serializers.ModelSerializer):

        class Meta:
            model = meta_model
            fields = meta_fields

    return Serializer
