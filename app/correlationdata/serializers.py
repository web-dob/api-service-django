from dataclasses import field
from statistics import mode
from rest_framework import serializers
from .models import UserCorrelationData


class DataListSerializer(serializers.ModelSerializer):
    correlation = serializers.SerializerMethodField('get_correlation_data')

    def get_correlation_data(self, obj):
        correlation_data = {}
        correlation_data.update(value = obj.value, p_value = obj.p_value)
        return correlation_data

    class Meta:
        model = UserCorrelationData
        fields = ("user_id", "x_data_type", "y_data_type", "correlation")
