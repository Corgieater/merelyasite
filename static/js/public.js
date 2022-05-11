"use strict";
// 顯示或隱藏區域
function hideOrShow(element) {
  element.classList.toggle("hide");
}

// 做訊息貼在選定區域
function makeMessage(place, message) {
  let p = document.createElement("p");
  p.textContent = message;
  p.classList.add("warning");
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
