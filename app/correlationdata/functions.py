# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
from .models import *


def convert_float(val):
    try:
        if isinstance(val, float):
            return val
        else:
            return '-'
    except Exception:
        return '-'


def set_calculate(data):
    context = {}
    try:
        x_data = pd.json_normalize(data['data']['x'])
        x_data.rename(columns=({
          'date': f"date_{data['data']['x_data_type']}",
          'value': f"value_{data['data']['x_data_type']}"
        }), inplace=True)    
        #Преобразуем все не float значения к виду '-'
        x_data[f"value_{data['data']['x_data_type']}"] = x_data[f"value_{data['data']['x_data_type']}"].apply(convert_float)
        #Удалим строки с '-', т.к. они содержат невалидные данные
        x_data = x_data.loc[x_data[f"value_{data['data']['x_data_type']}"] != '-']

        y_data = pd.json_normalize(data['data']['y'])
        y_data.rename(columns=({
          'date': f"date_{data['data']['y_data_type']}",
          'value': f"value_{data['data']['y_data_type']}"
        }), inplace=True)
        #Преобразуем все не float значения к виду '-'
        y_data[f"value_{data['data']['y_data_type']}"] = y_data[f"value_{data['data']['y_data_type']}"].apply(convert_float)

        #Удалим строки с '-', т.к. они содержат невалидные данные
        y_data = y_data.loc[y_data[f"value_{data['data']['y_data_type']}"] != '-']   

        df = x_data.merge(
          y_data,
          left_on=f"date_{data['data']['x_data_type']}", 
          right_on=f"date_{data['data']['y_data_type']}",
          how='outer').dropna()

        df.drop(columns=[f"date_{data['data']['y_data_type']}"], axis=1, inplace=True)
        df.rename(columns=({
            f"date_{data['data']['x_data_type']}": "date",
            f"value_{data['data']['x_data_type']}": data['data']['x_data_type'],
            f"value_{data['data']['y_data_type']}": data['data']['y_data_type']}),
            inplace=True)

        #Коэффициент корреляции по Пирсону
        corr = df[data['data']['x_data_type']].astype('float64').corr(df[data['data']['y_data_type']].astype('float64'))

        
        try:
            ucordata = UserCorrelationData.objects.get(
                user_id = data['user_id'], 
                x_data_type = data['data']['x_data_type'],
                y_data_type = data['data']['y_data_type']
            )
            ucordata.value = 0
            ucordata.p_value = corr
            ucordata.save()
        except ObjectDoesNotExist:
            newucordata = UserCorrelationData()
            newucordata.user_id = data['user_id']
            newucordata.x_data_type = data['data']['x_data_type']
            newucordata.y_data_type = data['data']['y_data_type']
            newucordata.value = 0
            newucordata.p_value = corr
            newucordata.save()

        context['ok'] = 'Data loaded'
    except Exception as err:
        context['error'] = err
    return context