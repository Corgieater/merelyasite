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
