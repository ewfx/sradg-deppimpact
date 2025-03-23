
let url1 = "http://127.0.0.1:8000/getalldetails"; 


function callSys1_Headers(){
    fetch(url1, {headers: {'Access-Control-Allow-Origin':'*'}})
        .then(resp => resp.json())
        .then(res => {
            let sys1table = document.getElementById("sys1table");
            sys1table.innerHTML = getHeaders(res.values[0]);
        })
        .catch( err =>{
            console.log("Err: ", err );
        })
}

function callSys1(){
    
    fetch(url1, {headers: {'Access-Control-Allow-Origin':'*'}})
    .then(resp => resp.json())
        .then(res => {
            console.log(res.values)
            let sys1table = document.getElementById("sys1table");
            for(let r of res.values)
                sys1table.innerHTML += (convertResToTableRows(r));
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
    console.log(Object.keys(jsonVal))
    let txt = "<tr>";
    for(let key of Object.keys(jsonVal))
        txt += ("<td>"+jsonVal[key]+"</td>")
    txt += "</tr>";
    return txt;
}

callSys1_Headers();
callSys1();
