"use strict";

// let userData = null;
// 頁面區
let poster = document.querySelector(".posterPlace > img");
let title = document.querySelector(".headArea > section :nth-child(1)");
let year = document.querySelector(".headArea > section :nth-child(2)");
let directors = document.querySelector(".headArea > section :nth-child(4)");
let plot = document.querySelector(".plot > p");
let casts = document.querySelector(".casts");
let genres = document.querySelector(".genres");

// action區
let rateBts = document.querySelectorAll("input[type='radio']");
let cancelBt = document.querySelector(".cancelBt");

// review區
let saveBt = document.querySelector(".reviewBox > section > button");
let reviewTitle = document.querySelector(
  ".reviewBox > section:nth-child(2) > h2"
);

// 查詢用
let filmId = cutUserInput("m/");

// 儲存評論
saveBt.addEventListener("click", async function () {
  let userLog = document.querySelector("textarea").value;
  console.log(userLog);
  const req = await fetch("/api/user");
  const res = await req.json();
  let id = res["userId"];
  let today = new Date();
  let dd = String(today.getDate()).padStart(2, "0");
  let mm = String(today.getMonth() + 1).padStart(2, "0");
  let yyyy = today.getFullYear();
  let watchedDate = document
    .querySelector('.reviewBox > section > input[type="date"]')
    .value.replaceAll("-", "/");
  if (watchedDate === "") {
    watchedDate = null;
  }
  console.log(watchedDate);
  today = yyyy + "/" + mm + "/" + dd;
  let data = {
    userReview: userLog,
    filmId: filmId,
    currentDate: today,
    watchedDate: watchedDate,
    userId: id,
  };
  sendDataToBackend("PATCH", data, "/api/review");
});

// 評分星星 按評分會直送資料庫更新
rateBts.forEach((bt) => {
  bt.addEventListener("click", async function (e) {
    let rate = e.target.value;
    console.log(rate);
    const req = await fetch("/api/user");
    const res = await req.json();
    let id = res["userId"];
    let data = {
      rate: rate,
      userId: id,
      filmId: filmId,
    };
    sendDataToBackend("PATCH", data, "/api/rate");
    window.location.reload();
  });
});

// 拿該使用者對該電影的評分;
async function getUserRate() {
  const req = await fetch("/api/user");
  const res = await req.json();
  let id = res["userId"];
  let data = {
    filmId: filmId,
    userId: id,
  };
  console.log(data);
  let score = await sendDataToBackend("POST", data, "/api/rate");
  return score;
}

// 顯示之前的評分星星
async function showPreviousRate() {
  let data = await getUserRate();
  let rate = null;
  if (data.rate === null) {
    hide(cancelBt);
    console.log(rate);
    return (rate = 0);
  } else {
    rate = data.rate;
    console.log(rate);
    show(cancelBt);
  }

  switch (rate) {
    case "0.5": {
      let star = document.querySelector("#rating1");
      console.log(0.5);
      star.checked = true;
      break;
    }
    case "1.0": {
      let star = document.querySelector("#rating2");
      console.log(1);
      star.checked = true;
      break;
    }
    case "1.5": {
      let star = document.querySelector("#rating3");
      console.log(1.5);
      star.checked = true;
      break;
    }
    case "2.0": {
      let star = document.querySelector("#rating4");
      console.log(2);
      star.checked = true;
      break;
    }
    case "2.5": {
      let star = document.querySelector("#rating5");
      console.log(2.5);
      star.checked = true;
      break;
    }
    case "3.0": {
      let star = document.querySelector("#rating6");
      console.log(3);
      star.checked = true;
      break;
    }
    case "3.5": {
      let star = document.querySelector("#rating7");
      console.log(3.5);
      star.checked = true;
      break;
    }
    case "4.0": {
      let star = document.querySelector("#rating8");
      console.log(4);
      star.checked = true;
      break;
    }
    case "4.5": {
      let star = document.querySelector("#rating9");
      console.log(4.5);
      star.checked = true;
      break;
    }
    case "5.0": {
      let star = document.querySelector("#rating10");
      console.log(5);
      star.checked = true;
      break;
    }
    default:
      break;
  }
}

// 去除評分
cancelBt.addEventListener("click", async function () {
  for (let bt of rateBts) {
    bt.checked = false;
  }
  const req = await fetch("/api/user");
  const res = await req.json();
  let id = res["userId"];
  let data = {
    filmId: filmId,
    userId: id,
  };
  sendDataToBackend("DELETE", data, "/api/rate");
  hide(cancelBt);
  window.location.reload();
});

// 拿電影資料
async function getFilm() {
  const filmId = cutUserInput("m/");
  const req = await fetch(`/api/film/${filmId}`);
  const res = await req.json();
  return res;
}

// 顯示電影資料
async function showFilmInfo() {
  let data = await getFilm();
  console.log(data);
  let filmId = data["id"];
  let filmTitle = data["title"];
  reviewTitle.textContent = data["title"];
  let filmYear = data["year"];
  let filmDirectors = data["directors"];
  let filmPlot = data["plot"];
  let filmStars = data["stars"];
  let filmGenres = data["genres"];
  poster.src = `https://d4u16azcwb6ha.cloudfront.net/posters/img${filmId}.jpg`;
  title.textContent = filmTitle;
  year.textContent = filmYear;
  plot.textContent = filmPlot;
  makeAlinkAndAppend(directors, filmDirectors);
  makeAlinkAndAppend(casts, filmStars);
  makeAlinkAndAppend(genres, filmGenres);
}

showFilmInfo();
showPreviousRate();

// 要做使用者均分
