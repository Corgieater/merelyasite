"use strict";

// 給要headers的功能打API用
async function sendDataToBackend(method, data, address) {
  const req = await fetch(address, {
    method: method,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  console.log(data);
  const res = await req.json();
  console.log(res);
  if (res.ok) {
    return true;
  } else if (res.message) {
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

// 從href拿使用者輸入值
function cutUserInput(target) {
  let href = window.location.href;
  let shift = target.length;
  let userInputIndex = href.indexOf(target) + shift;
  let userInput = href.slice(userInputIndex);
  return userInput;
}

// 特別用來建名字中有空格的a link
function makeAlinkAndAppend(area, iterableData) {
  for (let info of iterableData) {
    let href = info.replaceAll(" ", "-");
    let a = document.createElement("a");
    a.href = `/director/${href}`;
    a.textContent = info;
    area.append(a);
  }
}

// 拿使用者資料 no use:(
// async function getUserData() {
//   const req = await fetch("/api/user");
//   const res = await req.json();
//   return res;
// }
