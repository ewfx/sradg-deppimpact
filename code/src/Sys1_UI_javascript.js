
let url1 = "http://127.0.0.1:8000/getalldetails"; 
let url1_1 = "http://127.0.0.1:8000/addvalue"; 
let url_rag_prompt = "http://127.0.0.1:8000/get_llm_response"


function callSys1(){
    
    fetch(url1, {headers: {'Access-Control-Allow-Origin':'*'}})
    .then(resp => resp.json())
        .then(res => {
            console.log(res.values)
            let sys1table = document.getElementById("sys1table");
            sys1table.innerHTML = '<tr id="table_header"></tr>'
            getHeaders(res.values[0]);
            for(let r of res.values)
                sys1table.innerHTML += (convertResToTableRows(r));
        })
        .catch( err =>{
            console.log("Err: ", err );
        })

}

function addValue1(){
    
    fetch(url1_1, {headers: {'Access-Control-Allow-Origin':'*'}})
    .then(resp => resp.json())
        .then(res => {
            callSys1();
        })
        .catch( err =>{
            console.log("Err: ", err );
        })

}

function getHeaders(jsonVal)
{
    let ele = document.getElementById("table_header");
    txt = "";
    for(let key of Object.keys(jsonVal))
        txt += ("<th>"+key+"</th>")
    ele.innerHTML = txt 
}

function convertResToTableRows(jsonVal)
{
    console.log(Object.keys(jsonVal))
    let txt = "<tr>";
    for(let key of Object.keys(jsonVal))
        txt += ("<td>"+jsonVal[key]+"</td>")
    txt += "</tr>";
    return txt;
}


function rag_prompt(){

    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const raw = JSON.stringify({
        "query": document.getElementById("rag_prompt_input").value
    });

    const requestOptions = {
        method: "POST",
        headers: myHeaders,
        body: raw
    };
    document.getElementById("load").style.display = "block";
    fetch(url_rag_prompt, requestOptions) 
        
        .then(resp => resp.json())
        .then(res => {
            console.log(res)
            let recontable = document.getElementById("rag_prompt_display");
            recontable.innerHTML = '<div>'
            
            for(let r of res.values){
                recontable.innerHTML += "<div class='qq'>"+r.question+"</div>";
                recontable.innerHTML += "<div class='aa'>"+r.answer+"</div>";
            }
            recontable.innerHTML += '</div>'
            
            document.getElementById("load").style.display = "none";
            
        })
        .catch( err =>{
            
            document.getElementById("load").style.display = "none";
            console.log("Err: ", err );
        })
}


callSys1();
