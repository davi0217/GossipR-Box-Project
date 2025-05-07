console.log("hello world");

let uniList=[];
let lenses=document.getElementById("lenses");


/* fetch("https://raw.githubusercontent.com/Hipo/university-domains-list/refs/heads/master/world_universities_and_domains.json")
    .then(response=>response.json())
    .then(function(data){
        uniList=data;
        console.log(data);
        console.log(uniList);

        for(let i=0;i<=5; i++){
            console.log(uniList[i]["country"]);
        }

        uniList.forEach(uni=>{
            if (uni["country"]=="Spain"){
                console.log(uni);
                let list=document.getElementById("uni-list");
                list.innerHTML+=`  <li>
                        <div class="uni-item">
                            <div class="uni-img">
                                <i class="fa-solid fa-school-circle-check"></i>
                            </div>
                            <div class="uni-info">
                                <h1>${uni["name"]}</h1>
                                <span>${uni["country"]}</span> <span>${uni["state-province"]!=null?uni["state-province"]:" "}</span>
                                <h4>${uni["domains"][0]}</h4>
                                <a href="${uni["web_pages"][0]}">Link to web</a>
                            </div>
                        </div>
                    </li>`
                
            }
        })
    }) */


if (lenses){
lenses.addEventListener("click", function(){
    let list=document.getElementById("uni-list");
    list.innerHTML="";
    fetch("https://raw.githubusercontent.com/Hipo/university-domains-list/refs/heads/master/world_universities_and_domains.json")
    .then(response=>response.json())
    .then(function(data){
        uniList=data;
        console.log(data);
        console.log(uniList);

        for(let i=0;i<=5; i++){
            console.log(uniList[i]["country"]);
        }

        uniList.forEach(uni=>{
            if (uni["country"]=="Spain" && uni["name"].toLowerCase().includes(document.getElementById("input-uni").value.toLowerCase()) ){
                console.log(uni);
                let list=document.getElementById("uni-list");
                list.innerHTML+=`  <li>
                        <div class="uni-item">
                            <div class="uni-img">
                                <i class="fa-solid fa-school-circle-check"></i>
                            </div>
                            <div class="uni-info">
                                <h1>${uni["name"]}</h1>
                                <span>${uni["country"]}</span> <span>${uni["state-province"]!=null?uni["state-province"]:" "}</span>
                                <h4>${uni["domains"][0]}</h4>
                                <a href="${uni["web_pages"][0]}">Link to web</a>
                            </div>
                        </div>
                    </li>`
                
            }
        })
    })
}) 
}

let uniSearcher=document.getElementById("university");
if (uniSearcher){

    uniSearcher.innerHTML="";
    fetch("https://raw.githubusercontent.com/Hipo/university-domains-list/refs/heads/master/world_universities_and_domains.json")
    .then(response=>response.json())
    .then(function(data){
        uniList=data;
        uniList.forEach(function(uni){
            if(uni["country"]=="Spain"){
            uniSearcher.innerHTML+=`
            <option>${uni["name"]}</option>
            `}
        })

      
})}
   
let keyWord=" ";
if(document.getElementById("news-filter")){
 keyWord=document.getElementById("news-filter").value?document.getElementById("news-filter").value:"Recycling";

}

let API_KEY_NEWS="eaf7c0d4ba764e0aaabe4ac3c5dd8e28";

index=0;

function callNew(){
    fetch(`https://newsapi.org/v2/everything?q=${keyWord}&apiKey=${API_KEY_NEWS}`)
    .then(response=>response.json())
    .then(function(data){
        
        newList=[];
        
        for(let i=0;i<5;i++){
            newList.push(data["articles"][i]);
        }


    let container=document.getElementById("news-block");
    function updateNew(){
    if (container){
            container.innerHTML=`
            <h1>Stay Informed: The Need for Awareness on Environmental Issues</h1>
            <p>In today’s fast-changing world, it’s crucial to stay informed about environmental news. <br>From climate change to the conservation of natural resources, the issues impacting our planet are more pressing than ever. <br><br><strong>The environment is at the heart of our future,</strong> <br>and understanding the latest developments is essential to making informed decisions.</p>
            
            <div class="news-container">
                <div class="arrow-left"><i class="fa-solid fa-arrow-left" id="arrow-left"></i></div>
                <div class="news-info">
                    <h1 >${newList[index]["title"]}</h1>
                    <h2>${newList[index]["description"]}</h2>
                    <p>${newList[index]["content"].split("[")[0]}</p>
                    <a href="${newList[index]["url"]}">Read more...</a>
                <div class="numbers-container">
                <ul class="numbers-list">
                    <li>
                        
                        ${index==0?"<p><strong>1</strong></p>":"<p>1</p>"}
                    </li>
                    <li>
                    ${index==1?"<p><strong>2</strong></p>":"<p>2</p>"}
                    </li>
                    <li>
                    ${index==2?"<p><strong>3</strong></p>":"<p>3</p>"}
                    </li>
                    <li>
                    ${index==3?"<p><strong>4</strong></p>":"<p>4</p>"}
                    </li>
                    <li>
                    ${index==4?"<p><strong>5</strong></p>":"<p>5</p>"}
                    </li>
                </ul>
            </div>
                    </div>
                 
                <div class="news-img-container">
                    <img src="${newList[index]["urlToImage"]}" alt="">
                </div>
                <div class="arrow-right"><i class="fa-solid fa-arrow-right" id="arrow-right"></i></div>
            </div>
            `
        }
    }

    updateNew();
   
    
    
    
    
    
})};


document.addEventListener("click", function(event){

    if (event.target.id=="arrow-left"){
    if (index==0){
        console.log("left clicked");
        index=4;
        callNew();
    }else{
        console.log("left clicked");
        index=index-1;
        callNew();
    }
}})

document.addEventListener("click", function(event){

    if (event.target.id=="arrow-right"){
    if (index==4){
       console.log("right-clicked");
        index=0;
        callNew();
    }else{
        console.log("right-clicked");
        index=index+1;
        callNew();
    }


}})

if(document.getElementById("news-filter")){

callNew();

}

if(document.getElementById("news-filter")){

document.getElementById("news-filter").onchange=function(){
    keyWord=document.getElementById("news-filter").value;
    index=0;
    callNew();
}}


let bottle=document.getElementById("bottle");
let box=document.getElementById("box");
let wine=document.getElementById("wine");
let bottleContainer=document.querySelector(".disclaimer-yellow");
let boxContainer=document.querySelector(".disclaimer-blue");
let wineContainer=document.querySelector(".disclaimer-green");

if(bottle){

bottle.addEventListener("mouseover", function(){
    bottleContainer.setAttribute("style","opacity:100%");
})
bottle.addEventListener("mouseout", function(){
    bottleContainer.setAttribute("style", "opacity:0%");
})
wine.addEventListener("mouseover", function(){
    wineContainer.setAttribute("style","opacity:100%");
})
wine.addEventListener("mouseout", function(){
    wineContainer.setAttribute("style", "opacity:0%");
})
box.addEventListener("mouseover", function(){
    boxContainer.setAttribute("style","opacity:100%");
})
box.addEventListener("mouseout", function(){
    boxContainer.setAttribute("style", "opacity:0%");
})
}

let commentText=document.querySelectorAll("#comment-container");

if(commentText){
commentText.forEach(function(comment,i){
    comment.addEventListener("mouseover", function(){
       document.querySelectorAll("#comment-text")[i].firstElementChild.setAttribute("style", "display:flex");
    })
})
commentText.forEach(function(comment,i){
    comment.addEventListener("mouseout", function(){
        document.querySelectorAll("#comment-text")[i].firstElementChild.setAttribute("style", "display:none");
     })
    })
}

function changeHeart(){
    const xhttp = new XMLHttpRequest();
    let comment=document.getElementById("comment-id");
    let com_id=comment.textContent;
    xhttp.onload=function(){
        let heart=document.getElementById("heart");
        if(heart){
            heart.innerHTML='<i class="fa-solid fa-heart" style="color: #fd0d0d;"></i>';
        }   
    }
    xhttp.open("POST", "http://127.0.0.1:5002/like/"+com_id);
    xhttp.send();
}
function deleteNotif(){
    const xhttp = new XMLHttpRequest();
    let notif=document.getElementById("notif-id");
    let notif_id=notif.textContent;
    xhttp.onload=function(){
        let message=document.getElementById("notif-message").parentElement;
        if(message){
            message.style.display="none";
        }   
    }
    xhttp.open("POST", "http://127.0.0.1:5002/delete-notif/"+notif_id);
    xhttp.send();
}
