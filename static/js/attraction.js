const gallery = document.getElementById('slide');
const progressor = document.getElementById('selector');

//取得物件
let attraction_data = {};
async function GetData(){
    const url_Id = window.location.pathname.split('/').pop(); 
    //receive the last one element; 
    //split"" & split /\s/ tab and other whitespace character & /\s+/ multiple times;
    const r = await fetch(`/api/attraction/${url_Id}`)
    //將取得的資料得到json格式
    const data = await r.json();  
    attraction_data = data['data'];
    // console.log(attraction_data)
};


function img_func(){
    let image_attraction = attraction_data['images'];  
    //取得物件照片url網址以及製作div選單
    //透過createElement製作html標籤並且將src以及css變化導入標籤
    //預設class為hide隱藏以及show使用，並透過appendChild將所有圖片丟入整個section 
    
    //FOREACH製作所有的IMG_SRC透過CSS隱藏
    image_attraction.forEach( img_url => {
    
    
    //下排選單製作(將所有DIV導入SECTION SELECTION_BARLIST)
        const selector = document.createElement('div');
        selector.classList.add('indicator');
        progressor.appendChild(selector);
    
    //上排圖片輪播(將所有圖片URL導入 gallery)
        const image = document.createElement('img');
        image.src = img_url;
        image.classList.add('hide')
        gallery.appendChild(image);//每個圖片都顯示在gallery中
        //後臺審視
        // console.log(image)
    })
    gallery.firstElementChild.classList.remove('hide');
    progressor.firstElementChild.classList.add('show');
}


function text_func(){
    let name = document.getElementById('name');
    let mrt = document.getElementById('mrt');
    let transport = document.getElementById('transport');
    let description = document.getElementById('description');
    let category = document.getElementById('category');
    let address = document.getElementById('address');
    

// innertext 將資料導入text section
    name.innerText = attraction_data['name'];
    category.innerText = attraction_data['category'];
    mrt.innerText = attraction_data['mrt'] ? ` at ${attraction_data['mrt']}`: "";
    description.innerText = attraction_data['description'];
    address.innerText = attraction_data['address'];
    transport.innerText = attraction_data['transport'];
};

// 過去日子失效
function date_func(){
    let now = new Date();
    let ym = now.toISOString();
    let nowaday = ym.split('T')[0];
    let bookingDate = document.getElementById('bookingDate');
    bookingDate.setAttribute('min', nowaday);
}




//將section物件找出旗下有多少children，並增加事件處理
let prev = document.getElementById('prev');
let next = document.getElementById('next');


//設計控制流程
let img_handler = gallery.children;//取得圖片SECTION中所有物件
let progress_handler = progressor.children;//取得文字SECTION部分中所有物件

// console.log(img_handler)
// console.log(progress_handler)
let img_index = 0;

prev.addEventListener('click',() => {
    let num = img_handler.length;
    img_handler[img_index].classList.add('hide');
    progress_handler[img_index].classList.remove('show');
    if (img_index > 0){
        img_index--;
    }//若不是第一個，返回第一個
    else{
        img_index = num - 1;
    }//若是第一個，返回最後一張
    img_handler[img_index].classList.remove('hide');
    progress_handler[img_index].classList.add('show');
})

next.addEventListener('click',() => {
    //流程控制:點下按鈕後
    //將selection_bar的index取消show，將下一個增加show
    //同時將現在的圖片隱藏，並將下一個圖片的隱藏取消

    let num = img_handler.length;

    img_handler[img_index].classList.add('hide');//圖片隱藏
    progress_handler[img_index].classList.remove('show');//隱藏
    
    if (img_index < num - 1){
        img_index++;
    }
    else{
        img_index = 0;
        //若到最後一張，自動返回第一張
    }
    img_handler[img_index].classList.remove('hide'); //下一個圖片取消隱藏
    progress_handler[img_index].classList.add('show'); //下一個取消隱藏
})

let morning = document.getElementById('morning');
let night = document.getElementById('afternoon');
let price = document.getElementById('price')
let timeSwitch = document.getElementById('timeSwitch');

function price_func(){
    if(morning.checked){
        price.innerText = "新台幣2000 元"
    }
    else if(night.checked){         
        price.innerText = "新台幣2500 元"
    }
}
timeSwitch.addEventListener('change',price_func)


//載入圖案外掛
const loader = document.getElementById('loader');
for(let image of img_handler){
    
    image.addEventListener('load', () => {
        loader.hidden = true;
    })
}


async function main(){
    await GetData();
    img_func();
    text_func();
    date_func();
}


main();

