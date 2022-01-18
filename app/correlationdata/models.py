#-*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class UserCorrelationData(models.Model):
    class Meta:
        verbose_name = 'Данные корреляции'
        verbose_name_plural = 'Данные корреляции'

    user_id = models.PositiveIntegerField(verbose_name='ID юзера')
    x_data_type = models.CharField(max_length=512, verbose_name='Тип данных X')
    y_data_type = models.CharField(max_length=512, verbose_name='Тип данных Y')
    value = models.FloatField(verbose_name='Значение')
    p_value = models.FloatField(verbose_name='Коэффициент корреляции Пирсона')

    def __str__(self):
        return f"{self.user_id} - {self.x_data_type} - {self.y_data_type} - {self.value} - {self.p_value}"