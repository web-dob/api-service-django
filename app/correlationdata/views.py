# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import render
from .models import *
from .functions import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions


def main(request):
    context = {}
    return render(request, 'base.html', context)


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
