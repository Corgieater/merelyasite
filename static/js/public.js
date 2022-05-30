"use strict";
let movieTitle = document.querySelector("#movieTitle");
let movieYear = document.querySelector("#movieYear");

// 給要headers的功能打API用
async function sendDataToBackend(method, data, address) {
  const req = await fetch(address, {
    method: method,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  console.log("send this to back", data, typeof data);
  const res = await req.json();
  console.log(res);
  if (res.ok) {
    console.log("res.ok", res.ok);
    return true;
  } else if (res.message) {
    console.log("res.message", res.message);
    return res.message;
  } else {
    return res.data;
  }
}

// 顯示或隱藏區域
function hide(element) {
  element.classList.add("hide");
}
function show(element) {
  element.classList.remove("hide");
}
function hideOrShow(element) {
  element.classList.toggle("hide");
}

// 做訊息貼在選定區域
function makeMessage(place, message, colorClass = "warning") {
  let p = document.createElement("p");
  p.textContent = message;
  p.classList.add(colorClass);
  p.classList.add("disposableMessage");
  place.append(p);
}

// 刪除版面訊息
function deleteMessage() {
  let message = document.querySelector(".disposableMessage");
  if (message) {
    message.remove();
  }
}

// 從href拿在最後的使用者的輸入值
function cutUserInputAtLast(target) {
  let href = window.location.href;
  let shift = target.length;
  let userInputIndex = href.indexOf(target) + shift;
  let userInput = href.slice(userInputIndex);
  return userInput;
}
// 從href拿要自己定位的使用者輸入值
function cutUserInputInMiddle(targetHead, targetTail) {
  let href = window.location.href;
  let shift = targetHead.length;
  let head = href.indexOf(targetHead);
  let tail = href.indexOf(targetTail);
  let userInput = href.slice(head + shift, tail);
  return userInput;
}

// 拿最後的數字
function cutDownLastNumber(url) {}

// 特別用來建名字中有空格的a link
function makeAlinkAndAppend(area, prefix, iterableData) {
  for (let info of iterableData) {
    let href = info.replaceAll(" ", "+");
    let a = document.createElement("a");
    a.href = prefix + href;
    a.textContent = info;
    area.append(a);
  }
}

// 拿使用者資料
async function getUserData() {
  const req = await fetch("/api/user");
  const res = await req.json();
  return res;
}

// 檢查現在loggin的user是不是該頁面的主人
async function checkUserForPages(pageMaster) {
  let loggedUser = await getUserData();
  loggedUser = loggedUser["userName"];
  console.log("now logged in", loggedUser["userName"]);
  console.log("page master", pageMaster);
  if (loggedUser !== pageMaster) {
    return false;
  } else {
    return true;
  }
}

// 做頁碼 先用成做13頁 不然有夠他媽多= =
async function makePageTags(pageAndQuery, userInputAndPage, totalPages) {
  console.log("makePageTagds", userInputAndPage);
  let pagesPlace = document.querySelector(".pagesPlace");
  // 這裡的問題 改一下
  if (totalPages >= 14) {
    totalPages = 14;
  }
  for (let i = 0; i < totalPages; i++) {
    // 找出要切哪
    let sliceIndex = userInputAndPage.indexOf("e=");
    // 切到底拿到除了page以外的querystring
    let querystringWithoutPage = userInputAndPage.slice(0, sliceIndex + 2);
    let a = document.createElement("a");
    a.href = `/${pageAndQuery}${querystringWithoutPage}${i + 1}`;
    a.textContent = i + 1;
    pagesPlace.append(a);
  }
}

// 做今天日期string
function makeDateString() {
  let today = new Date();
  let dd = String(today.getDate()).padStart(2, "0");
  let mm = String(today.getMonth() + 1).padStart(2, "0");
  let yyyy = today.getFullYear();
  today = yyyy + "/" + mm + "/" + dd;
  return today;
}
