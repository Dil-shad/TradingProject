import os
from django.shortcuts import render
import pandas as pd
from django.core.files.storage import FileSystemStorage
import asyncio
import json
# Create your views here.

def csv_importer(request):
    if request.method == 'POST':
        csv_file=request.FILES['csv_file']
        timeframe=int(request.POST.get('timeframe',1))
        
        if csv_file.name.endswith('.csv'):
            fs=FileSystemStorage(location='media')
            file=fs.save(csv_file.name,csv_file)
            file_path=os.path.join('media', file)
        
        df=pd.read_csv(file_path,low_memory=False)
        candles=[]
        for index,row in df[:2].iterrows():
            candle=dict()
            candle[index]=row
            candles.append(candle)
        print(candles)
        
        async def filter_by_timeframe(candles,timeframe):
            candles["DATETIME"]=pd.to_datetime(candles["DATE"]+ '' + candles["TIME"],format='%Y%m%d %H:%M')
            candles["START_TIME"]=candles["DATE_TIME"]
            candles["END_TIME"]=candles["DATE_TIME"] + pd.to_timedelta(timeframe,unit='m')
            
            
            
            pass
            
    return render(request,"index.html")



