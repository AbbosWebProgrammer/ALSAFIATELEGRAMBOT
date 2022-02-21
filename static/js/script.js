var changeselecetvalue=''
var order_id=-1
var disable_order_id=-1
function sendmessage(id){
    url = "/sendmessage/"
    fetch(
    url,{
    method:'POST',
    headers:{
        'Content-Type':'application/json',
        'X-CSRFToken':csrftoken,
    },
    body:JSON.stringify({'id':id})
    })
    .then((response)=>{
        response.json().then((data)=>{
              data=data.ordds
              text = ''
            for (i=0;i<data.length;i++){
                text += "<tr><th scope='row'>"+(i+1)+"</th><td>"+data[i].name_uz+"</td><td>"+data[i].name_ru+"</td><td>"+data[i].quantity+"</td><td>"+data[i].price+"</td><td>"+data[i].totalprice+"</td></tr>"
            }
            document.getElementById('modal_table_tbody').innerHTML = text
            
        })
    })

}





function onchangeselectvalue(chosen) {
    changeselecetvalue=chosen
    console.log(changeselecetvalue);
  }

function getorderstatus(id){
    order_id=id
    url = "/getorderstatus/"
    fetch(
    url,{
    method:'POST',
    headers:{
        'Content-Type':'application/json',
        'X-CSRFToken':csrftoken,
    },
    body:JSON.stringify({'id':id})
    })
    .then((response)=>{
        response.json().then((data)=>{
            data=data.status
            changeselecetvalue=data
            console.log(data)  
            text = ''
            for (i=0;i<data.length;i++){
                text += "<tr><th scope='row'>"+(i+1)+"</th><td>"+data[i].name_uz+"</td><td>"+data[i].name_ru+"</td><td>"+data[i].quantity+"</td><td>"+data[i].price+"</td><td>"+data[i].totalprice+"</td></tr>"
            }
            if (data==='CONFIRMED'){
                text+="<option class='bg-light-info text-info' selected='selected' value='CONFIRMED'> CONFIRMED</option><option class='bg-light-danger text-danger' value='REFUSAL'>REFUSAL</option><option class='bg-light-success text-success' value='FULFILLED'>FULFILLED</option><option class='bg-light-warning text-warning' value='PARTIALLY SHIPPED'>PARTIALLY SHIPPED</option>"
            }
            if (data==='REFUSAL'){
                text+="<option class='bg-light-info text-info' value='CONFIRMED'> CONFIRMED</option><option selected='selected' class='bg-light-danger text-danger' value='REFUSAL'>REFUSAL</option><option class='bg-light-success text-success' value='FULFILLED'>FULFILLED</option><option class='bg-light-warning text-warning' value='PARTIALLY SHIPPED'>PARTIALLY SHIPPED</option>"
            }
            if (data==='FULFILLED'){
                text+="<option class='bg-light-info text-info' value='CONFIRMED'> CONFIRMED</option><option class='bg-light-danger text-danger' value='REFUSAL'>REFUSAL</option><option selected='selected' class='bg-light-success text-success' value='FULFILLED'>FULFILLED</option><option class='bg-light-warning text-warning' value='PARTIALLY SHIPPED'>PARTIALLY SHIPPED</option>"
            }
            if (data==='PARTIALLY SHIPPED'){
                text+="<option class='bg-light-info text-info'  value='CONFIRMED'> CONFIRMED</option><option class='bg-light-danger text-danger' value='REFUSAL'>REFUSAL</option><option class='bg-light-success text-success' value='FULFILLED'>FULFILLED</option><option selected='selected' class='bg-light-warning text-warning' value='PARTIALLY SHIPPED'>PARTIALLY SHIPPED</option>"
            }
            document.getElementById('OrderStatusSelected').innerHTML = text
            
        })
    })

}
function changeorderstatus(){
    url = "/changeorderstatus/"
    fetch(
    url,{
    method:'POST',
    headers:{
        'Content-Type':'application/json',
        'X-CSRFToken':csrftoken,
    },
    body:JSON.stringify({'id':order_id,'status':changeselecetvalue})
    })
    .then((response)=>{
        response.json().then((data)=>{
            data=data.status
            console.log(data)  
            window.location.reload();
        })
    })

}


function getdisableorderid(chosen) {
    disable_order_id=chosen
    console.log(disable_order_id);
  }
function disableorder(){
    url = "/disableorder/"
    fetch(
    url,{
    method:'POST',
    headers:{
        'Content-Type':'application/json',
        'X-CSRFToken':csrftoken,
    },
    body:JSON.stringify({'id':disable_order_id})
    })
    .then((response)=>{
        response.json().then((data)=>{
            window.location.reload();
            
        })
    })

}


var websocket=new WebSocket('ws://127.0.0.1:8000/ws/real_data/')
websocket.onmessage=function(e){
    var data=JSON.parse(e.data);
    text = ''
    for (i=0;i<data.length;i++){

        text += "<tr><td>"+(i+1)+"</td><td>"+data[i].id+"</td><td>"+data[i].phone+"</td><td>"+data[i].name+"</td><td>"+data[i].username+"</td><td>"+data[i].sum+"</td>"
        if(data[i].status === "CONFIRMED"){
            text += "<td><div class='badge rounded-pill text-info bg-light-info p-2 text-uppercase px-3'><i class='bx bxs-circle align-middle me-1'></i>Confirmed</div></td>"
        }
        else if(ord.status === "REFUSAL"){
            text += "<td><div class='badge rounded-pill text-danger bg-light-danger p-2 text-uppercase px-3'><i class='bx bxs-circle align-middle me-1'></i>REFUSAL</div></td>"
        }
        else if(ord.status === "FULFILLED"){
            text += "<td><div class='badge rounded-pill text-success bg-light-success p-2 text-uppercase px-3'><i class='bx bxs-circle me-1'></i>FulFilled</div></td>"
        }
        else if(ord.status === "PARTIALLY SHIPPED"){
            text += "<td><div class='badge rounded-pill text-warning bg-light-warning p-2 text-uppercase px-3'><i class='bx bxs-circle align-middle me-1'></i>Partially shipped</div></td>"
        }
        text+="<td>"+data[i].day+"<br>"+data[i].time+"</td><td>"+data[i].region+"<br>"+data[i].district+"</td>"     
        if(data[i].payment_made===true){
            text+="<td><i class='fadeIn animated bx bx-check-circle text-success h4'></i></td>"
        } 
        else if(data[i].payment_made===false){
            text+="<td><i class='fadeIn animated bx bx-x-circle text-danger h4'></i></td>"
        } 
        text+="<td class='bg-warning'>"+data[i].payment_type+"</td>"
        text+="<td><button type='button' class='btn btn-primary btn-sm radius-30 px-4' data-bs-toggle='modal' data-bs-target='#EditModal' onclick='sendmessage("+data[i].id+")'>View Details</button></td>"
        text += "<td><div class='d-flex order-actions'>"
        text += "<button type='button' style='font-size: 18px;width: 34px;height: 34px;display: flex;align-items: center;justify-content: center;background: #f1f1f1;border: 1px solid #eeecec;text-align: center;border-radius: 20%;color: #2b2a2a;' data-bs-toggle='modal' data-bs-target='#EditOrderStatus' onclick='getorderstatus("+data[i].id+")'><i class='bx bxs-edit m-0' ></i></button>"
        text += "<button type='button' class='ms-3' style='font-size: 18px;width: 34px;height: 34px;display: flex;align-items: center;justify-content: center;background: #f1f1f1;border: 1px solid #eeecec;text-align: center;border-radius: 20%;color: #2b2a2a;' data-bs-toggle='modal' data-bs-target='#DisableOrder' onclick='getdisableorderid("+data[i].id+")' ><i class='bx bxs-trash'></i></button></div></td>"
        text += "</tr>"
    }
    document.getElementById('reattimedatachange').innerHTML = text
    
    // document.getElementById('').innerHTML = data.number
    // 
}














