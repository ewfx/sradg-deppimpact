#conda activate hack2025
#cd C:\Users\ProgsNeedNoSpace\MinicondaEnvs\hack2025\sradg-deppimpact\code\src
#uvicorn recon:app --host 127.0.0.3

from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import datetime

path = "recon.csv"

path1 = "sys1.csv"
url1 = "http://127.0.0.1:8000/getlatestdetail"

path2 = "sys2.csv"
url2 = "http://127.0.0.2:8000/getlatestdetail"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"mssg": "hi"}

@app.get("/fetchnchecklatest")
async def fetchnchecklatest():
    keys = ["col1", "col2", "col3"]  #make configurable
    txt = ""

    

    contents1 = requests.get(url1)
    d1 = contents1.json()
    contents2 = requests.get(url2)
    d2 = contents2.json()

    if(len(d1)==0 or len(d2)==0): 
        return { "err": "no records in either sys1 count:"+str(len(d1))+" or sys2 count:"+str(len(d2))}

    d1 = d1[0]
    d2 = d2[0]
    print(d1)
    print(d2)

    df = pd.read_csv(path, index_col=False)

    dictVal = { "datetime": datetime.datetime.now()}
    for k_idx in range(0, len(keys)):
        key = keys[k_idx]
        k = keys[k_idx]
        if( (key in d1.keys()) and (key in d2.keys()) ):
            dictVal["sys1__"+k] = d1[k]
            dictVal["sys2__"+k] = d2[k]
            dictVal["res__"+k] = (d1[k] == d2[k])
            print("sys1__"+k)
    
    
    df = pd.concat([df, pd.DataFrame([dictVal])], ignore_index= False)
    
    df.to_csv(path, index=False)
    return {"values": df.to_dict("records")}

def appendFile(txt):
    file = open(path,'a')
    file.write(txt)
    file.write("\n")
    file.close()

#formula change
#rounding factopr
#currency diff
#not updated values 