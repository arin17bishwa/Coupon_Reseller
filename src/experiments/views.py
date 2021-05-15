from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
import sqlite3, os
from rest_framework import serializers
from django.core.serializers import serialize
from django.http import JsonResponse
# Create your views here.


def pin_api(request,pin,*args,**kwargs):

    conn = sqlite3.connect(os.path.join(settings.BASE_DIR, 'experiments','oxygen_database'))
    cur = conn.cursor()
    cur.execute('SELECT * FROM PIN_CODE_CITY_LAT_LONG WHERE ZIP_CD= ? ', (pin,))
    rows = cur.fetchall()
    # print(rows)
    cur.close()
    return JsonResponse(data=rows,safe=False)
