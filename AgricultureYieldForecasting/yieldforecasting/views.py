import pandas as pd

from django.shortcuts import render

from yieldforecasting.appconstants import path1,path2
from yieldforecasting.forms import DataForm
from yieldforecasting.service import forecast, loaddata


def predict(request):
    data=loaddata()
    return render(request, 'predict.html', {"districts":data})

def predictAction(request):

    if request.method == "POST":

        dataForm = DataForm(request.POST)

        if dataForm.is_valid():

            District_Name = dataForm.cleaned_data["District_Name"]
            Season = dataForm.cleaned_data["Season"]
            Area = dataForm.cleaned_data["Area"]

            temperature = dataForm.cleaned_data["temperature"]
            humidity = dataForm.cleaned_data["humidity"]
            ph = dataForm.cleaned_data["ph"]
            rainfall = dataForm.cleaned_data["rainfall"]

            result=forecast(District_Name,Season,Area,temperature,humidity,ph,rainfall)

            output="Suggested Crop:"+str(result[0])+" and Predicted Yield:"+str(result[1])

            data = loaddata()
            return render(request, 'predict.html', {"output":output,"districts": data})

        else:
            return render(request, 'predict.html', {"error": "Invalid Data"})
    else:
        return render(request, 'predict.html', {"error": "Invalid Request"})