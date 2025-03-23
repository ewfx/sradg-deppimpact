
let url2 = "http://127.0.0.2:8000/getalldetails";



function callSys2_Headers(){
    fetch(url2, {headers: {'Access-Control-Allow-Origin':'*'}})
        .then(resp => resp.json())
        .then(res => {
            let sys2table = document.getElementById("sys2table");
            sys2table.innerHTML = getHeaders(res.values[0]);
        })
        .catch( err =>{
            console.log("Err: ", err );
        })
}

function callSys2(){
    
    fetch(url2, {headers: {'Access-Control-Allow-Origin':'*'}})
    .then(resp => resp.json())
        .then(res => {
            console.log(res.values)
            let sys2table = document.getElementById("sys2table");
            for(let r of res.values)
                sys2table.innerHTML += (convertResToTableRows(r));
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


callSys2_Headers();
callSys2();