"use strict";
let currentUserId = null;
let globalMessagePlace = document.querySelector(".globalMessagePlace");
let mask = document.querySelector(".mask");
// nav按鈕
let logInBt = document.querySelector(".logInPlace > button");
let logOutBt = document.querySelector("nav > ul > li:nth-child(5)");
let profileBt = document.querySelector("nav > ul > li:nth-child(1)");
let searchFormBt = document.querySelector(".searchForm > a");
let searchSelect = document.querySelector(".searchSelect");
let userProfileHref = document.querySelector("nav > ul > li:nth-child(1) > a");
const addMovieBt = document.querySelector(".addMovieBt");

// 申請帳號的按鈕
const googleBt = document.querySelector("#googleSignin");
let signUpBt = document.querySelector(".signUpBt");

// 打開特定區域用的按鈕
const signUpPlaceBt = document.querySelector("nav > ul > li:nth-child(3) > a");
const logInPlaceBt = document.querySelector("nav > ul > li:nth-child(2) > a");
let addMovieNavBt = document.querySelector(
  "body > header > nav > ul > li:nth-child(6) > a"
);

// 關閉特定區域用的按鈕
let addMovieCloseBt = document.querySelector(".addMovieCloseBt");
let signUpPlaceCloseBt = document.querySelector(".signUpPlaceCloseBt");

// 區域
let signUpPlace = document.querySelector(".signUpPlace");
let logInPlace = document.querySelector(".logInPlace");
let addMoviePlace = document.querySelector(".addMoviePlace");

// 區域toggle
signUpPlaceBt.addEventListener("click", function (e) {
  e.preventDefault();
  hideOrShow(signUpPlace);
  hideOrShow(mask);
});

logInPlaceBt.addEventListener("click", function () {
  hideOrShow(logInPlace);
});

addMovieNavBt.addEventListener("click", function (e) {
  e.preventDefault();
  hideOrShow(addMoviePlace);
  hideOrShow(mask);
});

// 關閉區域
signUpPlaceCloseBt.addEventListener("click", function (e) {
  e.preventDefault();
  hide(signUpPlace);
  hide(mask);
});

addMovieCloseBt.addEventListener("click", function (e) {
  e.preventDefault();
  hide(addMoviePlace);
  hide(mask);
});

// 申請帳號和登入
// 申請帳號
signUpBt.addEventListener("click", async function (e) {
  // 拿資料丟API
  console.log("hi");
  e.preventDefault();
  deleteMessage();
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
  console.log(data);
  let returnMessage = await sendDataToBackend("POST", data, "/api/user");
  if (returnMessage === true) {
    console.log("success");
    window.location.reload();
  } else {
    makeMessage(signUpPlace, returnMessage);
  }
});

// 登入相關
logInBt.addEventListener("click", async function (e) {
  e.preventDefault();
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
    let userName = res.userName.replaceAll(" ", "+");
    profileBt.firstChild.textContent = res.userName;
    // 把user profile button加上href
    userProfileHref.href = `/user_profile/${userName}`;
    currentUserId = res["userId"];
    changingNav();
    return true;
  } else {
    return false;
  }
}

// 登出
logOutBt.addEventListener("click", logOut);
async function logOut(e) {
  e.preventDefault();
  const req = await fetch("/api/user", {
    method: "DELETE",
  });
  window.location.replace("/");
}

let dataForShowrow = {};
// 搜尋  HERE
searchFormBt.addEventListener("click", async function (e) {
  e.preventDefault();
  let userOption = searchSelect.value;
  console.log(userOption);
  let userInput = document.querySelector("#userInput");
  let userInputForHref = userInput.value.replaceAll(" ", "+");

  let movieUrl = `/search?keyword=${userInputForHref}&page=1`;
  let directorUrl = `/search/director?director=${userInputForHref}&page=1`;
  let actorUrl = `/search/actor?actor=${userInputForHref}&page=1`;
  let genreUrl = `/search/genre?genre=${userInputForHref}&page=1`;
  if (userInput.value === "") {
    userInput.focus();
  } else {
    if (userOption === "movie") {
      window.location.replace(movieUrl);
    } else if (userOption === "director") {
      window.location.replace(directorUrl);
    } else if (userOption == "actor") {
      window.location.replace(actorUrl);
    } else if (userOption == "genre") {
      window.location.replace(genreUrl);
    }
  }
});

// 打API拿電影資料加入dababase
addMovieBt.addEventListener("click", async function () {
  deleteMessage();
  let userInputTitle = movieTitle.value;
  console.log(userInputTitle);
  let userInputYear = movieYear.value;
  const req = await fetch(
    `/api/addFilm?t=${userInputTitle}&y=${userInputYear}`
  );
  const res = await req.json();
  if (res.ok) {
    makeMessage(addMoviePlace, "It's done!", "good");
    userInputTitle = "";
    userInputYear = "";
  } else {
    makeMessage(addMoviePlace, res.message);
  }
});

// 小功能
// 有登入顯示profileBt和logOutBthide然後重整
function changingNav() {
  hide(signUpPlaceBt);
  hide(logInPlaceBt);
  show(profileBt);
  show(logOutBt);
  window.location.reload;
}

checkIfLogged();
getUserData();
