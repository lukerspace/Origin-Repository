// const signbtn = document.querySelector('#signbtn') //點選navbar的{{登入或註冊}}


// //點button之後
// // 設定選擇
// const sign = document.querySelector('.sign') //選擇第一個class，此處為section部分{{整個選單控制}}

// function PopUp(){
//     sign.classList.add('pop-up')//透過增加class讓css選擇顯示
//     signbtn.classList.add('show')
// }



// // // 設定關閉
// // const close_x = sign.querySelectorAll('.close') //關閉符號
// // function NoPopUp(){
// //     sign.classList.remove('pop-up')//透過移除class讓css隱藏
// //     signbtn.classList.remove('active')
// // }


// // const signtext = document.querySelectorAll('.sign-container')
// // //選取登入以及註冊欄位內容部分，兩個都選
// // function Switch(){
// //     signtext.forEach(container=>{
// //         container.classList.toggle('show')
// //     })
// // }


// // 呼叫函數
// signbtn.addEventListener('click', PopUp)

// // close_x.forEach(btn => {
// //     btn.addEventListener('click',NoPopUp)
// // })

// // sign.addEventListener('click', event => {
// //     if(event.path[0] === sign){
// //         NoPopUp()
// //     }
// // })
// // signtext.forEach(container => {
// //     const changeBtn = container.querySelector('p')
// //     changeBtn.addEventListener('click', Switch())
// // })

const toSignBtn = document.querySelector('#to-sign-btn')
const signoutBtn = document.querySelector('#signout-btn')
const signBg = document.querySelector('.sign-bg')
const signCloseBtns = signBg.querySelectorAll('.close-btn')
const signContainers = document.querySelectorAll('.sign-container')

let signinCookie
//檢查是否有登入，若有login cookie秀出signoutBtn
function signinCheck(){
    signinCookie = document.cookie.indexOf('signin=')
    if(signinCookie == -1){
        toSignBtn.classList.add('show')
        signoutBtn.classList.remove('show')
    }
    else{ 
        toSignBtn.classList.remove('show')
        signoutBtn.classList.add('show')
    }
}
//進入頁面後先檢查使用者有沒有登入
signinCheck()

//秀出登入、註冊欄位
function popUpSignField(){
    signBg.classList.add('pop-up')
    toSignBtn.classList.add('active')
}
// 離開登入、註冊欄位
function cancelPopUpSignField(){
    signBg.classList.remove('pop-up')
    toSignBtn.classList.remove('active')
}
//變換登入、註冊欄位
function changeSignContainer(){
    signContainers.forEach(container=>{
        container.classList.toggle('show')
    })
}

toSignBtn.addEventListener('click', popUpSignField)

signCloseBtns.forEach(btn => {
    btn.addEventListener('click',cancelPopUpSignField)
})

//點選旁邊透明部分，也會離開登入｜註冊欄位
signBg.addEventListener('click', e => {
    if(e.path[0] === signBg){
        cancelPopUpSignField()
    }
})

signContainers.forEach(container => {
    const changeBtn = container.querySelector('p')
    changeBtn.addEventListener('click', changeSignContainer)
})


// 登入、註冊功能
const signupForm = document.querySelector('#signup')
const signinForm = document.querySelector('#signin')
const url = '/api/user'

// 註冊
function signup(e){
    e.preventDefault()
    const data = {
        name : this.querySelector('input[name="name"]').value,
        email : this.querySelector('input[name="email"]').value,
        password : this.querySelector('input[name="password"]').value 
    }
    fetch(url, {
        method: 'POST',
        body: JSON.stringify(data), // data can be `string` or {object}!
        headers: new Headers({
          'Content-Type': 'application/json'
        })
    })
    .then(res => res.json())
    //看response結果
    .then(data => console.log(data))
}


// 登入
function signin(e){
    e.preventDefault()
    const data = {
        email : this.querySelector('input[name="email"]').value,
        password : this.querySelector('input[name="password"]').value 
    }
    fetch(url, {
        method: 'PATCH',
        body: JSON.stringify(data), // data can be `string` or {object}!
        headers: new Headers({
          'Content-Type': 'application/json'
        })
    })
    .then(res => res.json())
    .then(data => {
        //如果有成功登入，回到原本頁面並將「註冊｜登入」按鈕改為「登出」按鈕
        if(data.ok === true){
            cancelPopUpSignField()
            signinCheck()
            toSignBtn.classList.remove('show')
            signoutBtn.classList.add('show')
            alert("登入成功！歡迎")
            //booking頁面更新用
            try{ getUserData() }catch(e){}
        }else{
            alert(data.message)
        }
    })
}

signupForm.addEventListener('submit', signup)
signinForm.addEventListener('submit', signin)


//登出
function signout(){
    fetch(url, {
        method: 'DELETE'
    })
    .then(() => {
        signinCheck()
        //booking頁面更新用
        try{ getUserData() }catch(e){}
    })
}
signoutBtn.addEventListener('click', signout)