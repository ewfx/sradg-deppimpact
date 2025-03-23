
let url2 = "http://127.0.0.2:8000/getalldetails";
let url2_1 = "http://127.0.0.2:8000/addvalue";



function callSys2(){
    
    fetch(url2, {headers: {'Access-Control-Allow-Origin':'*'}})
    .then(resp => resp.json())
        .then(res => {
            console.log(res.values)
            let sys2table = document.getElementById("sys2table");            
            sys2table.innerHTML = '<tr id="table_header"></tr>'
            getHeaders(res.values[0]);
            for(let r of res.values)
                sys2table.innerHTML += (convertResToTableRows(r));
        })
        .catch( err =>{
            console.log("Err: ", err );
        })

}

function addValue2(){
    
    fetch(url2_1, {headers: {'Access-Control-Allow-Origin':'*'}})
    .then(resp => resp.json())
        .then(res => {
            callSys2();
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
    let txt = "<tr>";
    for(let key of Object.keys(jsonVal))
        txt += ("<td>"+jsonVal[key]+"</td>")
    txt += "</tr>";
    return txt;
}


callSys2();