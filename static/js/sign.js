// 若api中有data=客戶資料API則顯示登出
// 若api中無data=NULL則顯示登入
fetch(`${window.origin}/api/user`)
.then(res => res.json())
.then(data => {
    if(data.data){
        document.getElementById('logOut').classList.remove('hide');
    }
    else{
        document.getElementById('logInSignUp').classList.remove('hide');
    }
})
.catch(err => {
    console.log(`fetch error : ${err}`)
})


// ============ pop up modal ================
// 點取navigator的資料顯示
const logInSignUp = document.getElementById('logInSignUp');

// 切換選單列表
const signUpLink = document.getElementById('signUpLink');
const logInLink = document.getElementById('logInLink');


// 得到選單列表
const logIn = document.getElementById('logIn');
const signUp = document.getElementById('signUp');


// 顯示登入訊息
const signUpMessage = document.getElementById('signUpMessage');
const logInMessage = document.getElementById('logInMessage');
const inputFields = document.querySelectorAll('.form-control input');

// =========================================================================

// 函數區
// 基礎功能:
// 提示字元消失，顯示登入介面，隱藏介面，顯示狀況，移除狀況
function clearMessage(element){
    element.classList.remove('error');
    element.classList.remove('success');
    element.textContent = '';
}
function slideIn(element){
    element.classList.add('slide-in');
} 
function hide(element){
    element.classList.remove('slide-in');
    element.classList.remove('show');
    // clear existed input
    const allInput = element.querySelectorAll('input');
    for (let input of allInput){
        input.value='';
    }
}
function show(element){
    element.classList.add('show');
    document.body.addEventListener('click',(evt)=>{
        if( !evt.target.closest('li#logInSignUp') && !evt.target.closest ('div.pop-up-modal')){
            hide(element);
            clearMessage(element.querySelector('span'));
        }
    })
}
//顯示小提醒
function emptyFieldReminder(inputField, message){
    const formControl = inputField.parentElement;
    formControl.classList.add('error');
    const errorMessage = formControl.querySelector('small');
    errorMessage.textContent = message;
}

//去除小提醒
//
function removeEmptyFieldReminder(){
    for(let inputField of inputFields){
            if(inputField.parentElement.classList.contains('error')){
                inputField.parentElement.classList.remove('error');
            }
    }
}



// 以下事件處理，函數處理
//點下顯示視窗
logInSignUp.addEventListener('click', (e) => {
    e.preventDefault;
    slideIn(logIn);
    show(logIn);
})

//點下切換註冊介面
signUpLink.addEventListener('click', () => {
    clearMessage(logInMessage);
    hide(logIn);
    removeEmptyFieldReminder();
    show(signUp);
})

//點下切換至登入介面
logInLink.addEventListener('click', () => {
    clearMessage(signUpMessage);
    hide(signUp);
    removeEmptyFieldReminder();
    show(logIn);
})
//關閉選單列表
const logInClose = document.getElementById('logInClose');
const signUpClose = document.getElementById('signUpClose');
logInClose.addEventListener('click', ()=>{hide(logIn)})
signUpClose.addEventListener('click', ()=>{hide(signUp)})
// const logInSuccessClose = document.getElementById('logInSuccessClose');
// const logOutSuccessClose = document.getElementById('logOutSuccessClose');

// logInSuccessClose.addEventListener('click', ()=>{hide(logInSuccess)})
// signUpClose.addEventListener('click', ()=>{hide(logOutSuccess)})


// ======================================================================
//選取欄位，登入以及註冊介面

const signupForm = document.querySelector('#signUpForm')
const signinForm = document.querySelector('#logInForm')
const userAPI = `${window.origin}/api/user`
// ==========================================================================
// 登入功能LOGIN
const logInForm = document.getElementById('logInForm');
logInForm.addEventListener('submit', evt => {
    evt.preventDefault();

    const logInEmail = document.getElementById('logInEmail');
    const logInPassword = document.getElementById('logInPassword');

    const email = logInEmail.value.trim();
    const password = logInPassword.value.trim();

    if(email ==='' || password ===''){
        if(email ===''){
            emptyFieldReminder(logInEmail,"電子信箱欄位不得為空白")
        } 
        if(password ===''){
            emptyFieldReminder(logInPassword,"密碼欄位不得為空白")
        }   
    }
    else{

        const requestBody = JSON.stringify({
            email: email,
            password: password
        });
    
        let responseStatus;
    
        fetch(`${window.origin}/api/user`,{
            method:'PATCH',
            headers: new Headers({ 
                'Content-Type': 'application/json'
            }),
            body: requestBody
        })
        .then(res => {
            responseStatus = res.status;
            return res.json();
        })
        .then(data => {
            if(data.ok){
                hide(logIn);
                alert("成功登入")
                // slideIn(logInSuccess);
                // show(logInSuccess);
                setTimeout(() =>{
                    location.reload();
                },300)
            }
            else if (data.error){
                logInMessage.classList.add('error');
                logInMessage.textContent = "帳號或密碼錯誤"; 
            //     error_type = data.message.split(':')[0];
            //     showMessage(error_type, logInMessage);
            }
            else if(data.error && responseStatus === 500){
                logInMessage.classList.add('error');
                logInMessage.textContent = "很抱歉，伺服器出現錯誤"; 
            }
        })
        .catch(err => {
            console.log(`fetch error : ${err}`)
        })
    }
})



// function signin(e){
//     e.preventDefault()
//     const data = {
//         email : this.querySelector('input[name="email"]').value,
//         password : this.querySelector('input[name="password"]').value 
//     }
//     fetch(userAPI, {
//         method: 'PATCH',
//         body: JSON.stringify(data),
//         // 可為物件或文字
        
//         headers: new Headers({
//             'Content-Type': 'application/json',
//             'Accept': 'application/json'
//         })   
//     })

//     .then(res => res.json())
//     .then(data => {
//         console.log(data)
//         //如果有成功登入，回到原本頁面並將「註冊｜登入」按鈕改為「登出」按鈕
//         if(data.ok === true){
//             // cancelPopUpSignField()
//             signinCheck()
//             // toSignBtn.classList.remove('show')
//             // signoutBtn.classList.add('show')
//             alert("登入成功！歡迎")
//             //頁面更新用
//             try{ getUserData() }catch(e){}
//             // try{ getBookingData() }catch(e){}
//             // try{ fetchOrderAPI() }catch(e){}
//         }else{
//             alert("登入失敗")
//             // const message = this.querySelector('.message')
//             // message.innerText = data.message
//         }
//     })
// }

// =================================================================================
// // 註冊
const signUpForm = document.getElementById('signUpForm');
signUpForm.addEventListener('submit', evt => {
    evt.preventDefault();

    const signUpName = document.getElementById('signUpName');
    const signUpEmail = document.getElementById('signUpEmail');
    const signUpPassword = document.getElementById('signUpPassword');

    const name = signUpName.value.trim();
    const email = signUpEmail.value.trim();
    const password = signUpPassword.value.trim();

    if(name ==='' || email ==='' || password ===''){
        if(name ===''){
            emptyFieldReminder(signUpName,"姓名欄位不得為空白")
        } 
        if(email ===''){
            emptyFieldReminder(signUpEmail,"電子信箱欄位不得為空白")
        } 
        if(password ===''){
            emptyFieldReminder(signUpPassword,"密碼欄位不得為空白")
        }   
    }
    else{
        const requestBody = JSON.stringify({
            name: name,
            email: email,
            password: password
        });
    
        let responseStatus;
    
        fetch(`${window.origin}/api/user`,{
            method:'POST',
            headers: new Headers({ 
                'Content-Type': 'application/json'
            }),
            body: requestBody
        })
        .then(res => {
            responseStatus = res.status;
            return res.json();
        })
        .then(data => {
            if(data.ok){
                signUpMessage.classList.add('success');
                signUpMessage.textContent = "註冊成功"; 
                const logInLink = document.getElementById('logInLink');
                logInLink.textContent = "點此登入";
            }
            else if(data.error ){

                error_type = data.message.split(':')[0];
                console.log(error_type,data.message)
                signUpMessage.classList.add('error');
                signUpMessage.textContent = "註冊失敗，該emil已使用"; 
                // showMessage(error_type, signUpMessage);
            }
            else if(data.error && responseStatus === 500){
                signUpMessage.classList.add('error');
                signUpMessage.textContent = "很抱歉，伺服器出現錯誤"; 
            }
        })
        .catch(err => {
            console.log(`fetch error : ${err}`)
        })
    }
})

// function signup(e){
//     e.preventDefault()
//     const data = {
//         name : this.querySelector('input[name="name"]').value,
//         email : this.querySelector('input[name="email"]').value,
//         password : this.querySelector('input[name="password"]').value 
//     }
//     fetch(userAPI, {
//         method: 'POST',
//         body: JSON.stringify(data),
//         headers: new Headers({
//           'Content-Type': 'application/json'
//         })
//     })
//     .then(res => res.json())
//     //看response結果
//     .then(data => {
//         // const message = this.querySelector('.message')
//         if(data.ok){
//             alert("註冊成功")
//             // changeSignContainer()
//         }else{
//             alert("註冊失敗")
//             // message.innerText = data.message
//         }
//     })
// }

for(let inputField of inputFields){
    inputField.addEventListener('focus', ()=>{
        if(inputField.parentElement.classList.contains('error')){
            inputField.parentElement.classList.remove('error');
        }
    })
}

// ====================================================================================
// //登出

const signoutBtn = document.querySelector('#logOut');
function signout(){``
    fetch(userAPI, {
        method: 'DELETE'
    })
    .then(() => {
        signinCheck()
        alert("登出成功！")
        setTimeout(() =>{
                location.reload();
            },300)
        })
//         //頁面更新用
        try{ getUserData() }catch(e){}
        try{ getBookingData() }catch(e){}
//         try{ fetchOrderAPI() }catch(e){}
    
}
signoutBtn.addEventListener('click', signout)


// =====================================================================================
// //檢查是否有登入，若get user api有資料，秀出signoutBtn
function signinCheck(){
    fetch(userAPI)
        .then(res => res.json())
        .then(data => {
            if(data.data){
                console.log(data,"登入成功")
            }else{
                console.log(data,"登入失敗")
            }
        })
}
// //進入頁面後先檢查使用者有沒有登入
signinCheck()


// 不知用不用得到
const book=document.getElementById("schedule")



function schedule(){
    fetch(userAPI)
        .then(res => res.json())
        .then(data => {
            if(data.data){
                console.log("yo")
                location.href="/booking"
            }else{
                document.getElementById('logIn').classList.add('slide-in');
                document.getElementById('logIn').classList.add('show');
            }
        }
    )}

book.addEventListener("click",schedule)