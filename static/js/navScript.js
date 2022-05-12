"use strict";
let currentUserId = null;
// nav按鈕
const googleBt = document.querySelector("#googleSignin");
let signUpBt = document.querySelector(".signUpPlace > a");
let logInBt = document.querySelector(".logInPlace > button");
let logOutBt = document.querySelector("nav > ul > li:nth-child(6)");
let profileBt = document.querySelector("nav > ul > li:nth-child(1)");
let searchFormBt = document.querySelector(".searchForm > a");

// 打開特定區域用的按鈕
const signUpPlaceBt = document.querySelector("nav > ul > li:nth-child(3) > a");
const logInPlaceBt = document.querySelector("nav > ul > li:nth-child(2) > a");

// 區域
let signUpPlace = document.querySelector(".signUpPlace");
let logInPlace = document.querySelector(".logInPlace");

// 區域toggle
signUpPlaceBt.addEventListener("click", function () {
  hideOrShow(signUpPlace);
});

logInPlaceBt.addEventListener("click", function () {
  hideOrShow(logInPlace);
});

// 申請帳號和登入
// 申請帳號
signUpBt.addEventListener("click", async function () {
  // 拿資料丟API
  let email = document.querySelector(".signUpPlace>input[type='email']").value;
  let password = document.querySelector(
    ".signUpPlace>input[type='password']"
  ).value;
  let name = document.querySelector(".signUpPlace>input[type='text']").value;
  console.log(email, password, name);

  let data = {
    email: email,
    password: password,
    name: name,
  };

  let returnMessage = await sendDataToBackend("POST", data, "/api/user");
  if (returnMessage === true) {
    window.location.reload();
  } else {
    makeMessage(signUpPlace, returnMessage);
  }
});

// 登入相關
logInBt.addEventListener("click", async function () {
  const email = document.querySelector(".logInPlace>input[type='email']").value;
  const password = document.querySelector(
    ".logInPlace>input[type='password']"
  ).value;
  deleteMessage();
  let data = {
    email: email,
    password: password,
  };

  let returnMessage = await sendDataToBackend("PATCH", data, "/api/user");
  if (returnMessage !== true) {
    makeMessage(logInPlace, returnMessage);
  } else {
    window.location.reload();
  }
});

// 檢查登入與否然後變動Nav
async function checkIfLogged() {
  const req = await fetch("/api/user");
  const res = await req.json();
  if (res.userName) {
    profileBt.firstChild.textContent = res.userName;
    changingNav();
    console.log(res);
    currentUserId = res["userId"];
    // userData = res;
    // return res;
  }
}

// 登出
logOutBt.addEventListener("click", logOut);
async function logOut(e) {
  e.preventDefault();
  const req = await fetch("/api/user", {
    method: "DELETE",
  });
  window.location.reload();
}

let dataForShowrow = {};
// 搜尋
searchFormBt.addEventListener("click", async function (e) {
  e.preventDefault();
  let userInput = document.querySelector("#userInput");
  if (userInput.value === "") {
    userInput.focus();
  } else {
    window.location.replace(
      `/search?keyword=${userInput.value.replaceAll(" ", "+")}&page=1`
    );
  }
});

// 小功能
// 變動nav然後重整
function changingNav() {
  hideOrShow(signUpPlaceBt);
  hideOrShow(logInPlaceBt);
  hideOrShow(profileBt);
  hideOrShow(logOutBt);
  window.location.reload;
}

checkIfLogged();
