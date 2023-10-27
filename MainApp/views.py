import os
from django.http import FileResponse
from django.shortcuts import render
import pandas as pd
from django.core.files.storage import FileSystemStorage
import asyncio
import json
from asgiref.sync import async_to_sync

@async_to_sync
async def filter_by_timeframe(candles, timeframe=1):
# This function will return timeframe for candles
            data = pd.DataFrame(candles)
            # print(data)
            data["DATETIME"] = pd.to_datetime(data["DATE"].astype(str) + " " + data["TIME"], format="%Y%m%d %H:%M")
            data.set_index("DATETIME", inplace=True)
            timeframe_data = data.resample(f"{timeframe}T").agg(
                {
                    "BANKNIFTY": "first",
                    "OPEN": "first",
                    "HIGH": "max",
                    "LOW": "min",
                    "CLOSE": "last",
                    "VOLUME": "sum",
                }
            )
            return timeframe_data
@async_to_sync
async def file_to_save(json_data):
    # this function will save timefram data into media folder (fs)
    fs = FileSystemStorage(location="media")
    file_name='timeframe_file.json'
    try:
        with fs.open(file_name,'w') as f:
            f.write(json_data)
        file_path=os.path.join("media",file_name)
    except Exception as e:
        print('failed', e)
    return file_name

def csv_importer(request):
    if request.method == "POST":
        csv_file = request.FILES["csv_file"]
        timeframe = int(request.POST.get("timeframe", 1))
        file_path=''

        # check if csv file or not
        if csv_file.name.endswith(".csv"):
            global fs
            fs = FileSystemStorage(location="media")
            file = fs.save(csv_file.name, csv_file)
            file_path = os.path.join("media", file)
        # create candle dataset
        df = pd.read_csv(file_path, low_memory=False)
        candles = []
        for _, row in df.iterrows():
            candles.append(row)
            
        # used asyncio function for to avoid log loading @decoratr used we cant use 'await' here
        timeframe_data = filter_by_timeframe(candles, timeframe)
        # print(timeframe_data.head())
        #json_data = json.loads(timeframe_data)
        json_data = timeframe_data.to_json(orient='records', date_format='iso')
        json_file= file_to_save(json_data)
        
        response= FileResponse(fs.open(json_file, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{json_file}"'
        return response
        
    return render(request, "index.html")

