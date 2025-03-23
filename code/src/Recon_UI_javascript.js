
let url = "http://127.0.0.3:8000/fetchnchecklatest"; 


function callRecon_Headers(){
    fetch(url, {headers: {'Access-Control-Allow-Origin':'*'}})
        .then(resp => resp.json())
        .then(res => {
            console.log(res)
            let recontable = document.getElementById("recontable");
            recontable.innerHTML = getHeaders(res.values[0]);
        })
        .catch( err =>{
            console.log("Err: ", err );
        })
}

function callRecon(){
    
    fetch(url, {headers: {'Access-Control-Allow-Origin':'*'}})
    .then(resp => resp.json())
        .then(res => {
            console.log(res)
            let recontable = document.getElementById("recontable");
            for(let r of res.values)
                recontable.innerHTML += (convertResToTableRows(r));
        })
        .catch( err =>{
            console.log("Err: ", err );
        })

}


function getHeaders(jsonVal)
{
    let txt = "<tr>";
    for(let key of Object.keys(jsonVal))
        txt += ("<th>"+key+"</th>")
    txt += "</tr>";
    return txt;
}

function convertResToTableRows(jsonVal)
{
    let txt = "<tr>";
    for(let key of Object.keys(jsonVal))
        txt += ("<td>"+jsonVal[key]+"</td>")
    txt += "</tr>";
    return txt;
}

function callReconTable(){
    callRecon_Headers();
    callRecon(); 
}