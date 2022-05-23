"use strict";
// 查詢用
let filmId = cutUserInputAtLast("m/");

// 頁面區
let poster = document.querySelector(".posterPlace > img");
let title = document.querySelector(".headArea > section :nth-child(1)");
let year = document.querySelector(".headArea > section :nth-child(2)");
let directors = document.querySelector(".directorsPlace");
let plot = document.querySelector(".plot > p");
let casts = document.querySelector(".casts");
let genres = document.querySelector(".genres");

// action區
let rateBtsWrap = document.querySelector(".rate");
let rateBts = document.querySelectorAll("input[type='radio']");
let cancelBt = document.querySelector(".cancelBt");
let reviewBt = document.querySelector(".actionBox>ul>li:nth-child(1)>a");
let averageRatePlace = document.querySelector(
  ".actionBox > ul > li:nth-child(4)"
);
let addListBt = document.querySelector(".actionBox > ul > li:nth-child(2) > a");

// review區
let reviewBox = document.querySelector(".reviewBox");
let dateCheckBox = document.querySelector(
  '.reviewBox > section:nth-child(2) > input[type="checkbox"]'
);
let dateInputPlace = document.querySelector("#watchedDay");
let saveBt = document.querySelector(".reviewBox > section > button");
let closeBt = document.querySelector(".closeBt");
let reviewTitle = document.querySelector(
  ".reviewBox > section:nth-child(2) > h2"
);
let reviewPoster = document.querySelector(
  ".reviewBox > section:nth-child(1) > img"
);

// 沒登入就把reviewBox的東西都藏起來吧
async function showProperReviewBox() {
  const userIsLogged = await checkIfLogged();
  console.log(userIsLogged);
  if (!userIsLogged) {
    hide(rateBtsWrap);
    hide(reviewBt);
    hide(addListBt);

    let actionBox = document.querySelector(".actionBox > ul");
    actionBox.style.height = "200px";
    let li = document.createElement("li");
    let p = document.createElement("p");
    p.textContent = "Log in to review or rate";
    li.append(p);
    p.style.cursor = "pointer";
    p.addEventListener("click", function () {
      hideOrShow(logInPlace);
    });
    let averageRate = document.querySelector(
      ".actionBox > ul > li:nth-child(4)"
    );
    averageRate.title = "hi";
    actionBox.insertBefore(li, averageRate);
  }
}

showProperReviewBox();

// 寫評分按鈕
// 打開評論區
reviewBt.addEventListener("click", function (e) {
  e.preventDefault();
  hideOrShow(reviewBox);
  show(mask);
});

// 顯示日期按鈕
dateCheckBox.addEventListener("click", function () {
  hideOrShow(dateInputPlace);
});

// 儲存評論
saveBt.addEventListener("click", async function () {
  let userLog = document.querySelector("textarea");
  let messagePlace = document.querySelector(
    ".reviewBox > section:nth-child(2)"
  );
  deleteMessage();
  if (userLog.value === "") {
    makeMessage(messagePlace, "Type something, please");
  } else {
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
      userReview: userLog.value,
      filmId: filmId,
      currentDate: today,
      watchedDate: watchedDate,
      userId: id,
    };
    sendDataToBackend("PATCH", data, "/api/review");
    hide(reviewBox);
    hide(mask);
    userLog.value = "";
  }
});

// 關閉評論區
closeBt.addEventListener("click", function (e) {
  e.preventDefault();
  hide(reviewBox);
  hide(mask);
});

// 評分星星 按評分會直送資料庫更新
rateBts.forEach((bt) => {
  bt.addEventListener("click", async function (e) {
    let rate = e.target.value;
    const req = await fetch("/api/user");
    const res = await req.json();
    let id = res["userId"];
    if (id !== undefined) {
      console.log("userid", id);
      let data = {
        rate: rate,
        userId: id,
        filmId: filmId,
      };
      sendDataToBackend("PATCH", data, "/api/rate");
      window.location.reload();
    }
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
  console.log("拿該使用者評分: 資料", data);
  let score = await sendDataToBackend("POST", data, "/api/rate");
  console.log("last time rate", score);
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

// 刪除評分
cancelBt.addEventListener("click", async function (e) {
  e.preventDefault();
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

// 拿電影均分
async function getAverageRate() {
  let data = {
    filmId: filmId,
  };
  let averageRate = await sendDataToBackend("POST", data, "/api/average-rate");
  let mouseTextPlace = document.querySelector(".mouseTextPlace");
  if (averageRate["average"] !== null) {
    averageRatePlace.textContent = `Average rate ${averageRate["average"]}`;
    averageRatePlace.style.cursor = "pointer";

    mouseTextPlace.textContent = `Based on ${averageRate["totalCount"]} ratings`;
    averageRatePlace.addEventListener("click", function () {
      hideOrShow(mouseTextPlace);
    });
  } else {
    averageRatePlace.textContent = `No one rated yet`;
  }
}

// 拿電影資料
async function getFilm() {
  const req = await fetch(`/api/film/${filmId}`);
  const res = await req.json();
  return res;
}

// 顯示電影資料
async function showFilmInfo() {
  let data = await getFilm();
  data = data["data"];
  console.log(data);
  let filmId = data["movieId"];
  let filmTitle = data["title"];
  reviewTitle.textContent = data["title"];
  let filmYear = data["year"];
  let filmDirectors = data["directors"];
  let filmPlot = data["story"];
  let filmStars = data["actors"];
  let filmGenres = data["genres"];
  poster.src = `https://dwn6ych98b9pm.cloudfront.net/posters/img${filmId}.jpg`;
  reviewPoster.src = `https://dwn6ych98b9pm.cloudfront.net/posters/img${filmId}.jpg`;
  title.textContent = filmTitle;
  year.textContent = filmYear;
  year.href = `/year?year=${filmYear}`;
  plot.textContent = filmPlot;
  makeAlinkAndAppend(directors, "/director/", filmDirectors);
  makeAlinkAndAppend(casts, `/actor?actor=`, filmStars);
  makeAlinkAndAppend(genres, "/genre?genre=", filmGenres);
}

showFilmInfo();
showPreviousRate();
getAverageRate();
