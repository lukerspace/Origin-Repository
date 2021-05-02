//取得主業架構框框
let Main = document.getElementById('mains');
//取得main的主要頁面
let ip = "54.254.130.122"


//5. 將每個參數的欄位狀況，設計進去html的架構之中
//<article>
//  <a>整個api連結內容
//      <img>圖片api中取得圖片
//      <div>整個文字方塊    
//          <div>上層簡介
//              <p>捷運站
//              <p>旅遊類別
//          </div>
//          <p>下層景點標題
//      </div> 
//  </a>
//將page_list的json內容寫入attr_url超連結每個區塊之中。
//再將整體超連結{{標籤為a (attr_url)}} 丟進box中，box為整個attraction方塊
//回傳box

//createElement預設項目
let nextPage = 0;
let section;
let keyword = null;

function CreateItems(attraction){

    let box = document.createElement('article');
    box.classList.add('itembox');

    let attr_url = document.createElement('a');
    attr_url.href = `http://${ip}:3000/api/attraction/${attraction.id}`
    attr_url.setAttribute('target', '_blank');
    
    let attr_img = document.createElement('img');
    attr_img.src = attraction.images[0]
    attr_img.addEventListener('load',CheckPoint);

    //6. 製作attractionbox載入資料及照片時，每12個須紀錄換頁動作
    //執行CheckPoint函數，完成12個attraction寫入後，將load_next改成true載入下一頁
    //並且透過load_next的變化流程控制，下12個資料的寫入
    
    //{{7-1}}關鍵字流程如上
    //關鍵字設定
    let attr_text = document.createElement('div');
    attr_text.classList.add('textbox');
    
    let attr_title = document.createElement('p');
    attr_title.classList.add('title');
    attr_title.textContent = attraction.name;
    
    let attr_info = document.createElement('div');
    attr_info.classList.add('info');
    
    let attr_mrt = document.createElement('p');
    attr_mrt.classList.add('attraction-mrt');
    attr_mrt.textContent = attraction.mrt;
    
    let attr_type = document.createElement('p');
    attr_type.classList.add('attraction-category');
    attr_type.textContent = attraction.category;
   
    attr_info.appendChild(attr_mrt);
    attr_info.appendChild(attr_type);
    
    attr_text.appendChild(attr_info);
    attr_text.appendChild(attr_title);
    
    attr_url.appendChild(attr_img);
    attr_url.appendChild(attr_text);

    
    box.appendChild(attr_url);
    console.log(box);
    
    return box;
}


// 2.利用LoadData從api取得資料串列。
// 若是沒有關鍵字，即是查找keyword= null。並且若是有下一頁，將nextPage更新至下一頁。
// 並呼叫ShowData() 函數。

// 4-1 {{關鍵字設定}}
// 透過input的keyword及函數預設的nextpage=0匯入GetPata(0,keyword)
async function LoadData(keyword=null){
    if(nextPage !== null){
        nextPage = await GetData(nextPage,keyword);
        ShowData();}
}

// 3.將我的預設=0的nextPage導入GetData(pageNumber)中 {{此處函數output會更新nextPage}}
// 並且此函數目的為取得page_list的頁面arry資料及nextPage的更新。

async function GetData(pageNumber, keyword=null){
    let url;
    if(keyword){
        url = `http://${ip}:3000/api/attractions?page=${pageNumber}&keyword=${keyword}`;
    
        //5-1此部分為查找關鍵字以及頁數預設page=0    
        //5-1 得到資料API中的KEYWORD資料
    }else{
        url = `http://${ip}:3000/api/attractions?page=${pageNumber}`;
    }
    //此部分為首頁頁數
    let response = await fetch(url);
    let data = await response.json();
    nextPage = data.nextPage;
    page_list = data.data;
    // console.log(page_list)
    console.log("next page:",nextPage)
    return nextPage;
}
// 4. 透過showdata確認本頁資料個數，並且產生出attractionbox

// 將本頁面資料長度確認，並將本頁面，每一個{{單一資料}} LOAD 進我的CreateItems函數中 
// 並且將我的整體attractionBox丟進 INDEX.HTML中的預設區域。
// 預設initiator=0

//{{6-1}} 透過關鍵字搜索得到的API匯入CREATEITEMS函數中

let initiator = 0;

function ShowData(){
    initiator = 0;
    section = page_list.length;
    if(section){
        for(let attr of page_list){
            let attractionBox = CreateItems(attr);
            Main.appendChild(attractionBox);
        }
    }
    else if(!(Main.firstChild)){
        let message = document.createElement('h1');
        message.textContent = "未找到符合關鍵字的景點";
        Main.appendChild(message);
    }
}



//6. 檢查是否所有單一頁面資料都已經成功LOAD並且決定是否要LOAD下一頁的資料
let load_next = false;
function CheckPoint(){
    initiator++;
    if(initiator === section && nextPage !== null){
        console.log(initiator,"attractions are already loaded")
        load_next = true;
    }
}

// 初始1.呼叫call LoadData() keyword預設為null


LoadData(); 

//7. infinite scroll設定
//若(( window視窗本身的高度+cursor垂直方向的scroll >=  視窗body下緣-700pixel )) 且本業資料已經下載完成
//則進入LoadData() 此時若無keyword預設，keywoed仍然為null且nextPage更新至下一頁
//進入GetData(nextPage,keyword=null)

if(nextPage !== null){
    window.addEventListener('scroll',()=>{if((window.innerHeight + window.scrollY) >= (document.body.getBoundingClientRect().bottom - 700) && load_next){
            LoadData(keyword);
            load_next = false;
        }
    })
}

// 關鍵字設定流程
// 取得INDEX.HTML關鍵字ID
const SearchForm= document.getElementById('SearchForm');
const SearchKeyword = document.getElementById('SearchKey');
//1-1.將前端關鍵字表單送出送出，先拒絕預設跳出整理
//並且呼叫RemoveAll將屏幕更新
//3-1 KEYWORD更新，並且將nextPage更新成預設=0
//並且將INPUT中的內容匯入至LoadData(keyword)

SearchForm.addEventListener('submit',(event)=>{
    event.preventDefault();
    RemoveAll();
    nextPage = 0;
    keyword = SearchKeyword.value;
    LoadData(keyword);    
})
//2-1 將屏幕上內容去除
function RemoveAll(){
    while(Main.firstChild){Main.removeChild(Main.lastChild);}
}








