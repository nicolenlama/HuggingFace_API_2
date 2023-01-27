from django.shortcuts import render
from django.http import HttpResponse
import json

def dataRequest(request):
    
    from .api_obj import HF_API
    
    
    params = request.GET

    api_obj = HF_API(params)


    return HttpResponse(json.dumps(api_obj.response))