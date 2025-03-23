#conda activate hack2025
#cd C:\Users\ProgsNeedNoSpace\MinicondaEnvs\hack2025\sradg-deppimpact\code\src
#uvicorn sys2:app --host 127.0.0.2

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import datetime

path = "sys2.csv"

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
    return {"mssg": "Hello2"}

@app.get("/addvalue")
async def AddValue():
    values = {
        "datetime": datetime.datetime.now() ,
        "col1": 1, 
        "col2": 10, 
        "col3": 20
        } #make configurable
     
    appendFileCsv(values)
    return {"mssg": "Added2"}; 

@app.get("/getalldetails")
async def GetAllDetails():
    df = pd.read_csv(path)
    df = df[::-1]
    return {"values": df.to_dict("records")}


@app.get("/getlatestdetail")
async def GetLatestDetail():   
    df = pd.read_csv(path)
    return df.tail(1).to_dict("records")


def appendFileCsv(values):
    df = pd.read_csv(path, index_col=False)
    df = pd.concat([df, pd.DataFrame([values])], ignore_index= False)    
    df.to_csv(path, index=False)


def appendFile(txt):
    file = open(path,'a')
    file.write(txt)
    file.write("\n")
    file.close()


def createJson(cols, values):
    dictVal = {}
    for idx in range(0, len(cols)):
        dictVal[cols[idx]] = values[idx]
    return dictVal