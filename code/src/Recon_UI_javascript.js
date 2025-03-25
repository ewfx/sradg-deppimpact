
let url = "http://127.0.0.3:8000/fetchnchecklatest"; 
let url_analyze = "http://127.0.0.3:8000/analyze"; 
let url_analyze_latest = "http://127.0.0.3:8000/analyze_latest"; 
let url_rag_prompt = "http://127.0.0.3:8000/get_llm_response"


function callRecon(){
    showSiteLoader();
    fetch(url, {headers: {'Access-Control-Allow-Origin':'*'}})
    .then(resp => resp.json())
        .then(res => {
            console.log(res)
            let recontable = document.getElementById("recontable");
            recontable.innerHTML = '<tr id="table_header"></tr>'
            getHeaders(res.values[0])
            let k = res.values.length
            for(let r of res.values){
                recontable.innerHTML += (convertResToTableRows(r, k));
                k--;
            }
            hideSiteLoader();
        })
        .catch( err =>{
            console.log("Err: ", err );
            hideSiteLoader();
        })

}

function analyze(){
    showSiteLoader();
    fetch(url_analyze, {headers: {'Access-Control-Allow-Origin':'*'}})
    .then(resp => resp.json())
        .then(res => {
            console.log(res)
            let recontable = document.getElementById("recontable");
            recontable.innerHTML = '<tr id="table_header"></tr>'
            getHeaders(res.values[0])
            let k = res.values.length
            for(let r of res.values){
                recontable.innerHTML += (convertResToTableRows(r, k));
                k--;
            }
            hideSiteLoader()
        })
        .catch( err =>{
            hideSiteLoader()
            console.log("Err: ", err );
        })
}

function analyze_latest(){
    showSiteLoader();
    fetch(url_analyze_latest, {headers: {'Access-Control-Allow-Origin':'*'}})
    .then(resp => resp.json())
        .then(res => {
            console.log(res)
            let recontable = document.getElementById("recontable");
            recontable.innerHTML = '<tr id="table_header"></tr>'
            getHeaders(res.values[0])
            let k = res.values.length
            for(let r of res.values){
                recontable.innerHTML += (convertResToTableRows(r, k));
                k--;
            }
            hideSiteLoader()
        })
        .catch( err =>{
            hideSiteLoader()
            console.log("Err: ", err );
        })
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

function getHeaders(jsonVal)
{
    let ele = document.getElementById("table_header");
    txt = "<th>SlNo.</th>";
    for(let key of Object.keys(jsonVal))
        txt += ("<th>"+key+"</th>")
    ele.innerHTML = txt 
}

function convertResToTableRows(jsonVal, k)
{
    let txt = "<tr><td>"+k+"</td>";
    for(let key of Object.keys(jsonVal))
        txt += ("<td>"+jsonVal[key]+"</td>")
    txt += "</tr>";
    return txt;
}





function callReconTable(){
    
    callRecon(); 
}

function hideSiteLoader(){
    document.getElementById("site_loader").style.display = "none";
}


function showSiteLoader(){
    document.getElementById("site_loader").style.display = "block";
}