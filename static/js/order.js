let username;

/* user name */
function getUser() {
   const src = '/api/user';
   fetch(src)
      .then(response => response.json())
      .then(result => {
         const userData = result.data;

         if (userData) {
            username = userData.name;

            getOrder();
         } else {
            parent.location.href = '/';
         }
      })
      .catch(error => console.log(error));
}

getUser();

function getOrder() {
   const url = new URLSearchParams(window.location.search);
   const orderNumber = url.get('number');

   if (!orderNumber || !url) {
      parent.location.href = '/';
      return;
   }

   const src = `/api/order/${orderNumber}`;
   fetch(src)
      .then(response => response.json())
      .then(result => {
         const orderData = result.data;

         createDetermine(orderData);
      })
      .catch(error => console.log(error));
}

function createDetermine(orderData) {
   if (orderData == null) {
      const welcomeElement = document.getElementsByClassName('welcome')[0];
      welcomeElement.innerText = `${username}，您好：`;

      const orderInformationElement = document.getElementsByClassName('order-information')[0];

      removeAllChildNodes(orderInformationElement);

      const noResultElement = document.createElement('div');
      const noResultContent = document.createTextNode('搜尋不到該訂單');
      noResultElement.appendChild(noResultContent);
      orderInformationElement.appendChild(noResultContent);

      return;
   } else if (orderData.status === 1) {
      const welcomeElement = document.getElementsByClassName('welcome')[0];
      welcomeElement.innerText = `${username}，您好：`;

      const orderInformationElement = document.getElementsByClassName('order-information')[0];

      removeAllChildNodes(orderInformationElement);

      const orderNumberElement = document.createElement('div');
      orderNumberElement.classList.add('order-number');
      const orderNumber = orderData.number;

      const paymentElment = document.createElement('span');

      const paymentMessage = `(付款失敗)`;
      paymentElment.innerText = paymentMessage;
      paymentElment.style.color = '#FF9224';

      const orderNumberContent = document.createTextNode(`訂單編號：${orderNumber}`);
      orderNumberElement.appendChild(orderNumberContent);
      orderNumberElement.appendChild(paymentElment);
      orderInformationElement.appendChild(orderNumberElement);
      return;
   } else {
      createAPIElement(orderData);
   }
}

function createAPIElement(orderData) {
   const welcomeElement = document.getElementsByClassName('welcome')[0];
   welcomeElement.innerText = `${username}，感謝您的購買！您的訂單資訊如下：`;

   const orderNumberElement = document.getElementsByClassName('order-number')[0];
   const attractionImageElement = document.getElementsByClassName('attraction-image')[0];
   const attractionNameElement = document.getElementsByClassName('name')[0];
   const dateElement = document.getElementsByClassName('date')[0];
   const timeElement = document.getElementsByClassName('time')[0];
   const feeElement = document.getElementsByClassName('fee')[0];
   const addressElement = document.getElementsByClassName('address')[0];
   const contactNameElement = document.getElementsByClassName('contact-name')[0];
   const contactEmailElement = document.getElementsByClassName('contact-email')[0];
   const contactPhoneElement = document.getElementsByClassName('contact-phone')[0];
      
   const orderNumber = orderData.number;
   const price = orderData.price;

   const attractionName = orderData.trip.attraction.name;
   const address = orderData.trip.attraction.address;
   const image = orderData.trip.attraction.image;

   const date = orderData.trip.date;
   const time = orderData.trip.time;

   const contactName = orderData.contact.name;
   const contactEmail = orderData.contact.email;
   const contactPhone = orderData.contact.phone;

   let actualTime;
   if (time === 'morning') {
      actualTime = '早上 9 點到下午 4 點';
   }
   if (time === 'afternoon') {
      actualTime = '下午 2 點到晚上 9 點';
   }

   let orderNumberContent = document.createTextNode(`訂單編號：${orderNumber}`);
   orderNumberElement.appendChild(orderNumberContent);

   let imageElement = document.createElement('img');
   imageElement.src = image;
   attractionImageElement.appendChild(imageElement);

   let nameContent = document.createTextNode(`台北一日遊：${attractionName}`);
   attractionNameElement.appendChild(nameContent);

   let dateContent = document.createTextNode(date);
   dateElement.appendChild(dateContent);

   let timeContent = document.createTextNode(actualTime);
   timeElement.appendChild(timeContent);

   let feeContent = document.createTextNode(`新台幣 ${price} 元`);
   feeElement.appendChild(feeContent);

   let addressContent = document.createTextNode(address);
   addressElement.appendChild(addressContent);

   let contactNameContent = document.createTextNode(contactName);
   contactNameElement.appendChild(contactNameContent);

   let contactEmailContent = document.createTextNode(contactEmail);
   contactEmailElement.appendChild(contactEmailContent);

   let contactPhoneContent = document.createTextNode(contactPhone);
   contactPhoneElement.appendChild(contactPhoneContent);
}

function removeAllChildNodes(parent) {
   while (parent.firstChild) {
      parent.removeChild(parent.firstChild);
   }
}