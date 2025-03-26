#conda activate hack2025
#cd F:\hack2025\sradg-deppimpact\code\src
#uvicorn sys1:app --host 127.0.0.1

from fastapi import FastAPI
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import datetime

from langchain_groq import ChatGroq

from langchain_experimental.agents.agent_toolkits import create_csv_agent

groq_api = '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'

path = "sys1.csv"
path_qa = "sys1_qa.csv"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def main():
    return {"mssg": "Hello1"}

@app.get("/addvalue")
def AddValue():
    values = {
        "datetime": datetime.datetime.now() ,
        "col1": 1, 
        "col2": 10, 
        "col3": 20
        } #make configurable
     
    appendFileCsv(values)
    return {"mssg": "Added1"}; 

@app.get("/getalldetails")
def GetAllDetails():
    df = pd.read_csv(path)
    df = df.iloc[::-1]
    return {"values": df.to_dict("records")}


@app.get("/getlatestdetail")
def GetLatestDetail():   
    df = pd.read_csv(path)
    return df.tail(1).to_dict("records")


class get_llm_response_Item(BaseModel):
    query: str

@app.post("/get_llm_response")
def get_llm_response(get_llm_response_item: get_llm_response_Item):    
    #print( get_llm_response_item.query)
    df_qa = pd.read_csv(path_qa)
    try:
        response = ask_llm(get_llm_response_item.query)
    except:
        response = "No response found. Please try again."
    jsonVal_qa = {"question": get_llm_response_item.query,"answer": response}
    df_qa = pd.concat([df_qa, pd.DataFrame([jsonVal_qa])])
    df_qa.to_csv(path_qa, index=False)
    #return {"values": [{"question":  get_llm_response_item.query, "answer": get_llm_response_item.query}]}
    return {"values": df_qa.to_dict("records")}


def ask_llm(qry):
    llm = ChatGroq(temperature=0, model="llama3-70b-8192", api_key=groq_api)    
    agent = create_csv_agent(llm, path, verbose=False, allow_dangerous_code=True)
    return agent.invoke(qry)['output']


def appendFileCsv(values):
    df = pd.read_csv(path, index_col=False)
    df = pd.concat([df, pd.DataFrame([values])], ignore_index= False)    
    df.to_csv(path, index=False)


def appendFile():
    file = open(path,'a')
    
    file.write("\n")
    file.close()



def createJson(cols, values):
    dictVal = {}
    for idx in range(0, len(cols)):
        dictVal[cols[idx]] = values[idx]
    return dictVal