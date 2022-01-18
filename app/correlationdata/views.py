# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .serializers import *
import pandas as pd
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions


def convert_float(val):
    try:
        if isinstance(val, float):
            return val
        else:
            return '-'
    except Exception:
        return '-'


def main(request):
    context = {}
    return render(request, 'base.html', context)


def set_calculate(data):
    context = {}
    try:
        x_data = pd.json_normalize(data['data']['x'])
        x_data.rename(columns=({
          'date': f"date_{data['data']['x_data_type']}",
          'value': f"value_{data['data']['x_data_type']}"
        }), inplace=True)    
        """Преобразуем все не float значения к виду '-'"""
        x_data[f"value_{data['data']['x_data_type']}"] = x_data[f"value_{data['data']['x_data_type']}"].apply(convert_float)
        """Удалим строки с '-', т.к. они содержат невалидные данные"""
        x_data = x_data.loc[x_data[f"value_{data['data']['x_data_type']}"] != '-']

        y_data = pd.json_normalize(data['data']['y'])
        y_data.rename(columns=({
          'date': f"date_{data['data']['y_data_type']}",
          'value': f"value_{data['data']['y_data_type']}"
        }), inplace=True)
        """Преобразуем все не float значения к виду '-'"""
        y_data[f"value_{data['data']['y_data_type']}"] = y_data[f"value_{data['data']['y_data_type']}"].apply(convert_float)

        """Удалим строки с '-', т.к. они содержат невалидные данные"""
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

        """Коэффициент корреляции по Пирсону"""
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


class CalculateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        data = request.data
        print(request.data) 
        print(f'\ndata\n{data}')     
        rez = set_calculate(data)

        print(f'\nrez\n{rez}')
        if rez.get('ok'):
            return Response(status=200)
        else:
            return Response(status=404)


class CorrelationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        x_data_type = self.request.query_params.get('x_data_type')
        y_data_type= self.request.query_params.get('y_data_type')
        user_id= self.request.query_params.get('user_id')

        data = UserCorrelationData.objects.filter(
            user_id = user_id,
            x_data_type = x_data_type,
            y_data_type = y_data_type
        )
        if not data:
            raise Http404
        serializer = DataListSerializer(data, many=True)
        return Response(serializer.data)
