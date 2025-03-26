#conda activate hack2025
#cd F:\hack2025\sradg-deppimpact\code\src
#uvicorn recon:app --host 127.0.0.3

from fastapi import FastAPI
from pydantic import BaseModel

import requests
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import HTMLResponse

import pandas as pd
import datetime

import pandas as pd
from langchain_groq import ChatGroq

from langchain_experimental.agents.agent_toolkits import create_csv_agent

groq_api = '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'

path = "recon.csv"
path_qa = "recon_qa.csv"

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
def main():
    return {"mssg": "hi"}

@app.get("/fetchnchecklatest")
def fetchnchecklatest():
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
    df['datetime'] = pd.to_datetime(df['datetime'])

    dictVal = { "datetime": datetime.datetime.now(), "anomaly": "_", "comments": "_"}
    isAnyAnomaly = False
    for k_idx in range(0, len(keys)):
        key = keys[k_idx]
        k = keys[k_idx]
        if( (key in d1.keys()) and (key in d2.keys()) ):
            dictVal["sys1__"+k] = d1[k]
            dictVal["sys2__"+k] = d2[k]
            dictVal["diff__"+k] = d2[k] - d1[k]
            dictVal["res__"+k] = (d1[k] == d2[k])
            dictVal["anomaly__"+k] = "_"
            #resp = ask_llm("Based on historical data, is there an anomaly? Answer in yes or no.")
            #if "yes" in resp.lower():
            #    dictVal["anomaly__"+k] = True
            #    isAnyAnomaly = True
            #    resp2 = ask_llm("Based on historical data, why is there an anomaly?")
            #    dictVal["comments"] += ("For column "+ k + "- Reason: " + resp2 + ",")
            
            print("sys1__"+k)
    


    df = pd.concat([df, pd.DataFrame([dictVal])], ignore_index= False)
    df = df.sort_values(by=['datetime'], ascending=False)
    df.to_csv(path, index=False)
    return {"values": df.to_dict("records")}

@app.get("/analyze_latest")
def analyze_latest():
    df = pd.read_csv(path, index_col=False)
    
    #df = df.sort_values(by=['datetime'])
    keys = ['col1', 'col2', 'col3']  #make configurable

    row_idx = 0
    
    isAnyAnomaly = False
    for k_idx in range(0, len(keys)):
        key = keys[k_idx]
        k = keys[k_idx]
        
        resp = ask_llm("Based on historical data, is there an anomaly for the first row for column "+k+"? Answer in either yes or no.")
        df.at[row_idx, "anomaly__" + k] = resp
        if "yes" in resp.lower():
            #df.at[row_idx, "anomaly__"+k] = True
            isAnyAnomaly = True
        resp2 = ask_llm("Based on historical data, why is an anomaly present/absent for the first row for column "+k+"?" )
        df.at[row_idx,"comments"] = df.iloc[row_idx]["comments"] + ("For column "+ k + "- "+resp+"; Reason: " + resp2 + ",")
        
        print("sys1__"+k)
    
    df.at[row_idx, "anomaly"] = isAnyAnomaly

    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.sort_values(by=['datetime'], ascending=False)   
    df.to_csv(path, index=False)
    return {"values": df.to_dict("records")}

@app.get("/analyze")
def analyze():
    df = pd.read_csv(path, index_col=False)
    
    df = df.sort_values(by=['datetime'])
    cols = ['col1', 'col2', 'col3']  #make configurable

    #is there a pattern in the differences?
    #for pattern i need at least 3 data points

    for col in cols:
         df['diff__'+col] = pd.to_numeric(df['diff__'+col])
         for idx,r in df.iterrows():
            print("idx now:"+str(idx))
            if(idx <3): continue

            if df.iloc[idx]["res__"+col] == "True": continue  #ie. if Match then no anomaly check
            else:
                val = checkPattern(df.iloc[idx-2]["diff__"+col], df.iloc[idx-1]["diff__"+col], df.iloc[idx-0]["diff__"+col])
                print("idx:"+str(idx)+" val:"+str(val))
                df.at[idx, "anomaly__"+col] = val
                #df.iloc[idx]["anomaly__"+col] = val

                if val:
                    print(df.iloc[idx]["comments"])
                    df.at[idx, "comments"] = str(df.iloc[idx]["comments"]) + "non-contigous result diff for column:"+col

    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.sort_values(by=['datetime'], ascending=False)   
    df.to_csv(path, index=False)
    return {"values": df.to_dict("records")}

    # 
    #  

@app.get("/refresh")
def refresh():
    df = pd.read_csv(path, index_col=False)
    df = df[::-1]
    df = df.sort_values(by=['datetime'], ascending=False)    
    return {"values": df.to_dict("records")}


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

def appendFile(txt):
    file = open(path,'a')
    file.write(txt)
    file.write("\n")
    file.close()

def checkPattern(a, b, c):
    #delta of the delta should be same

    if(b-a != c-b): return True
    return False

#formula change
#rounding factopr
#currency diff
#not updated values 




@app.get("/ticket/{appId}/{recordId}")
def TicketSite(appId: str, recordId: str):


    html_content = '''
<html>
    <style>
        .label{
            padding: 5px;
            color: gray;
        }
        .input{
            width: 100%;
        }
    </style>
    <div style="width: 100%; height: 100%; background: linear-gradient(180deg, rgba(32,80,129,1) 50%, rgba(244, 245,247,1) 50%); overflow: auto;">
        <div style="position: relative; padding: 0px 40px 0px 40px; margin: auto; width: 400px; height: 600px; background-color: white; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); box-shadow: 2px 2px 2px 2px rgba(0,0,0,0.2);">
            <br/><br/>
            <div id="header"><h3>Raise new ticket</h3></div>
            <br/><br/>
            <div class="label">AppId</div>
            <div class="input"><input type="text" value="'''+ appId +'''"></div>
            <br/><br/>
            <div class="label">Record Id</div>
            <div class="input"><input type="text" value="''' +recordId + '''"></div>
            <br/><br/>  
            <div class="label">Reason for Error</div>
            <div class="input"><textarea rows="10" cols="50">This is an anomaly because ... </textarea></div>
            <button style="position: absolute; bottom: 50px; right: 50px;"  onclick="">Submit</button>
        </div>
    </div>

</html>
    '''
    return HTMLResponse(content=html_content, status_code=200)

