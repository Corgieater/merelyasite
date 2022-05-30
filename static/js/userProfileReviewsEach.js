"use strict";
// 一些表單用的資料
let filmId = null;
let lastTimeLogMessage = null;
let lastTimeSpoilers = null;
let lastTimeWatched = null;
let watchedDate = document.querySelector(
  '.reviewBox > section > input[type="date"]'
);
// // 查詢用

// 把這邊處理成一個功能丟到public? 等後續有差不多的東西再做
let uncleanUrlForReviewId = cutUserInputAtLast("/films");
let uncleanUrlForMovieName = cutUserInputAtLast("/reviews");
let userName = cutUserInputInMiddle("e/", "/r");
// 拿最後一個/然後找reviewID
let indexOfLastSlash = uncleanUrlForReviewId.lastIndexOf("/");
let reviewId = uncleanUrlForReviewId.slice(indexOfLastSlash + 1);
// 切MovieName超麻煩
let indexOfStartMovieName = uncleanUrlForMovieName.indexOf("s/");
let endIndexOfMovieName = uncleanUrlForMovieName.lastIndexOf("/");
let movieName = uncleanUrlForMovieName.substring(
  indexOfStartMovieName + 2,
  endIndexOfMovieName
);

// 頁面區
let poster = document.querySelector(".posterPlace > img");
let title = document.querySelector(
  ".textPlace > div > section:nth-child(1) > section > h2 > a"
);
let year = document.querySelector(
  ".textPlace > div > section:nth-child(1) > section > p > a"
);
let lastTimeStarPlace = document.querySelector(
  ".textPlace > div > section:nth-child(1) > section:nth-child(2) > section"
);
let lastTimeWatchPlace = document.querySelector(
  ".textPlace > div > section:nth-child(1) > section:nth-child(2) > p"
);

// action區
let rateBtsWrap = document.querySelector(".rate");
let rateBts = document.querySelectorAll("input[type='radio']");
let cancelBt = document.querySelector(".cancelBt");
let editBt = document.querySelector(
  ".textPlace > div > section.actionBox > ul > li:nth-child(1) > a"
);
let reviewAgainBt = document.querySelector(
  ".textPlace > div > section.actionBox > ul > li:nth-child(3) > a"
);
let averageRatePlace = document.querySelector(
  ".actionBox > ul > li:nth-child(5)"
);
averageRatePlace.title = "";
let addListBt = document.querySelector(".actionBox > ul > li:nth-child(2) > a");

// review區
let reviewBox = document.querySelector(".reviewBox");
let dateCheckBox = document.querySelector("#watched");
let spoilersCheckBox = document.querySelector("#spoilers");
let dateInputPlace = document.querySelector("#watchedDay");
let messagePlace = document.querySelector(".reviewBox > section:nth-child(2)");

let editSaveBt = document.querySelector(".editSaveBt");
let reviewAgainSaveBt = document.querySelector(".reviewAgainSaveBt");
let saveBtForOthers = document.querySelector(".saveBtForOthers");
let closeBt = document.querySelector(".closeBt");

let reviewTitle = document.querySelector(
  ".reviewBox > section:nth-child(2) > h2"
);
let reviewPoster = document.querySelector(
  ".reviewBox > section:nth-child(1) > img"
);
let userLogPlace = document.querySelector("#review");
let deleteReviewBt = document.querySelector(".deleteReviewBt");

// 沒登入就把reviewBox的東西都藏起來吧
// 這邊變成要檢查如果不是該ID的人就不要給他改東西?
async function showProperReviewBox() {
  // 看有沒有登入
  const userIsLogged = await checkIfLogged();
  let isPageBelongsToLoggedUser = false;
  console.log(userIsLogged);
  let actionBox = document.querySelector(".actionBox > ul");
  // 沒登入接下來都不用看了
  if (!userIsLogged) {
    console.log("no user logged");
    actionBox.style.height = "200px";
    let li = document.createElement("li");
    let p = document.createElement("p");
    p.textContent = "Log in to review or rate";
    li.append(p);
    p.style.cursor = "pointer";
    p.addEventListener("click", function (e) {
      e.preventDefault();
      hideOrShow(logInPlace);
    });
    actionBox.insertBefore(li, averageRatePlace);
  } else {
    // 有登入可以show starts rates wrap
    show(editBt);
    show(rateBtsWrap);
    show(addListBt);
    isPageBelongsToLoggedUser = await checkUserForPages(
      userName.replaceAll("+", " ")
    );
    console.log(isPageBelongsToLoggedUser);

    // page not belongs to logged user
    if (isPageBelongsToLoggedUser === false) {
      editBt.textContent = "Write a review";
      // 這邊要打API去查這user是有沒有寫過這電影的評論
      show(reviewAgainBt);
      cancelBt.style.bottom = "90px";
    }
    if (isPageBelongsToLoggedUser) {
      // 屬於頁面使用者所以會有 reviewAgainBt要改一下cancelBt位置
      cancelBt.style.bottom = "90px";
      show(reviewAgainBt);
    }
  }
}

// 更新評分按鈕
// 打開評論區 - 編輯或更新上次的評分
editBt.addEventListener("click", async function (e) {
  e.preventDefault();
  let isPageBelongsToLoggedUser = await checkUserForPages(
    userName.replaceAll("+", " ")
  );
  if (isPageBelongsToLoggedUser) {
    // 因為跟review again共用空間 按鈕要分出來
    userLogPlace.value = lastTimeLogMessage;
    hideOrShow(reviewBox);
    show(mask);
    show(editSaveBt);
    hide(reviewAgainSaveBt);
    // 看上次spoiler是不是true
    spoilersCheckBox.checked = lastTimeSpoilers;
    console.log(lastTimeSpoilers);
    // 上次看過東西就要維持一樣
    if (lastTimeWatched) {
      dateCheckBox.checked = true;
      dateCheckBox.value = lastTimeWatched;
      show(dateInputPlace);
      lastTimeWatched = turnDatabaseDateToStringDate(lastTimeWatched);
      watchedDate.value = lastTimeWatched;
    }
  } else if (isPageBelongsToLoggedUser === false) {
    hideOrShow(reviewBox);
    show(mask);
    hide(reviewAgainSaveBt);
    show(saveBtForOthers);
    userLogPlace.value = "";
    spoilersCheckBox.disabled = true;
    spoilersCheckBox.checked = false;
    dateCheckBox.checked = false;
    hide(watchedDate);
    watchedDate.value = "";
    hide(deleteReviewBt);
  }
  editSaveBt.addEventListener("click", async function () {
    console.log("update");
    updateReviewFunc();
  });
  saveBtForOthers.addEventListener("click", async function () {
    console.log("save review for others");
    saveReviewForOthers();
  });
});
// 打開評論區 - 再寫一次評論
reviewAgainBt.addEventListener("click", function (e) {
  e.preventDefault();
  // 因為跟EDIT共用空間 按鈕要分出來
  hideOrShow(reviewBox);
  show(mask);
  show(reviewAgainSaveBt);
  hide(editSaveBt);
  userLogPlace.value = "";
  spoilersCheckBox.disabled = true;
  spoilersCheckBox.checked = false;
  dateCheckBox.checked = false;
  hide(watchedDate);
  watchedDate.value = "";
  hide(deleteReviewBt);
  reviewAgainSaveBt.addEventListener("click", async function () {
    console.log("review again");
    reviewAgainFunc();
  });
});

// 如果userLog有東西才給用spoilerBt
userLogPlace.addEventListener("input", function () {
  if (userLogPlace.value !== "") {
    spoilersCheckBox.disabled = false;
  } else {
    spoilersCheckBox.disabled = true;
  }
});

// 顯示日期按鈕
dateCheckBox.addEventListener("click", function () {
  hideOrShow(dateInputPlace);
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
    e.preventDefault();
    let rate = e.target.value;
    const req = await fetch("/api/user");
    const res = await req.json();
    let id = res["userId"];
    if (id !== undefined) {
      let data = {
        rate: rate,
        userId: id,
        filmId: filmId,
      };
      let ratingMessage = await sendDataToBackend("PATCH", data, "/api/rate");
      if (ratingMessage === true) {
        window.location.reload();
      } else {
        makeMessage(averageRatePlace, ratingMessage);
      }
    }
  });
});

// 顯示之前的評分星星
async function showPreviousRate(rate) {
  if (rate === null) {
    hide(cancelBt);
  } else {
    rate = rate;
    show(cancelBt);
  }

  switch (rate) {
    case "0.5": {
      let star = document.querySelector("#rating1");
      star.checked = true;
      break;
    }
    case "1.0": {
      let star = document.querySelector("#rating2");
      star.checked = true;
      break;
    }
    case "1.5": {
      let star = document.querySelector("#rating3");
      star.checked = true;
      break;
    }
    case "2.0": {
      let star = document.querySelector("#rating4");
      star.checked = true;
      break;
    }
    case "2.5": {
      let star = document.querySelector("#rating5");
      star.checked = true;
      break;
    }
    case "3.0": {
      let star = document.querySelector("#rating6");
      star.checked = true;
      break;
    }
    case "3.5": {
      let star = document.querySelector("#rating7");
      star.checked = true;
      break;
    }
    case "4.0": {
      let star = document.querySelector("#rating8");
      star.checked = true;
      break;
    }
    case "4.5": {
      let star = document.querySelector("#rating9");
      star.checked = true;
      break;
    }
    case "5.0": {
      let star = document.querySelector("#rating10");
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
  let deleteRatingMessage = await sendDataToBackend(
    "DELETE",
    data,
    "/api/rate"
  );
  if (deleteRatingMessage === true) {
    hide(cancelBt);
    window.location.reload();
  } else {
    console.log(deleteRatingMessage, "deleteRatingMessage");
    makeMessage(averageRatePlace, deleteRatingMessage);
  }
});

// 拿review資料
async function getReview() {
  const req = await fetch(
    `/api/user_profile/${userName}/reviews/films/${movieName}/${reviewId}`
  );
  const res = await req.json();
  console.log("get review", res);
  return res;
}

// 顯示電影資料
async function showFilmInfo() {
  let data = await getReview();
  let isPageBelongsToLoggedUser = false;
  isPageBelongsToLoggedUser = await checkUserForPages(
    userName.replaceAll("+", " ")
  );

  let userReview = document.querySelector(".userReview > p");
  data = data["data"];
  filmId = data["movieId"];
  let filmTitle = data["movieTitle"];
  reviewTitle.textContent = filmTitle;
  let filmReview = data["movieReview"];
  let filmYear = data["movieYear"];
  let filmRate = data["movieRate"];
  let filmSpoiler = data["spoiler"];
  let filmWatchedDate = data["watchedDate"];
  let filmReviewDate = data["reviewDate"];

  if (filmWatchedDate === null) {
    filmWatchedDate = filmReviewDate;
  }
  lastTimeWatched = filmWatchedDate;
  lastTimeLogMessage = filmReview;
  userReview.textContent = filmReview;
  lastTimeSpoilers = filmSpoiler;
  poster.src = `https://dwn6ych98b9pm.cloudfront.net/moviePos/img${filmId}.jpg`;
  reviewPoster.src = `https://dwn6ych98b9pm.cloudfront.net/moviePos/img${filmId}.jpg`;
  title.textContent = filmTitle;
  title.href = `/film/${filmId}`;
  year.textContent = filmYear;
  year.href = `/year?year=${filmYear}`;
  if (isPageBelongsToLoggedUser) {
    show(rateBtsWrap);
  } else if (isPageBelongsToLoggedUser === false) {
    show(rateBtsWrap);
  }

  lastTimeWatchPlace.textContent = `Watched on 
  ${filmWatchedDate.substring(0, 16)}`;

  // make starts
  if (filmRate !== null) {
    if (filmRate !== "0.5") {
      let fullStarRate = parseInt(filmRate);
      for (let j = 0; j < fullStarRate; j++) {
        let img = document.createElement("img");
        img.src = "/static/images/star.png";
        lastTimeStarPlace.append(img);
      }
    }
    let halfStarRate = filmRate.toString().search(".5");
    if (halfStarRate !== -1) {
      let img = document.createElement("img");
      img.src = "/static/images/half_star.png";
      lastTimeStarPlace.append(img);
    }
  }
  getAverageRate();
  if (isPageBelongsToLoggedUser) {
    showPreviousRate(filmRate);
  }
}

deleteReviewBt.addEventListener("click", async function (e) {
  e.preventDefault();
  console.log("delete");
  const req = await fetch(
    `/api/user_profile/${userName}/reviews/films/${movieName}/${reviewId}`,
    {
      method: "DELETE",
    }
  );
  const res = await req.json();
  if (res.ok) {
    window.location.replace(`/user_profile/${userName}/reviews?page=1`);
  } else {
    makeMessage(messagePlace, res.message);
  }
});

// 小功能
// 轉換資料庫送來的日期資料
function turnDatabaseDateToStringDate(dabataseDate) {
  let newDate = new Date(dabataseDate);
  let year = newDate.getFullYear();
  let month = newDate.getMonth() + 1;
  if (month < 10) {
    month = `0${month}`;
  }
  let date = newDate.getDate();
  if (date < 10) {
    date = `0${date}`;
  }
  newDate = `${year}-${month}-${date}`;
  return newDate;
}

// 下面要修 但我沒時間= =
// 更新按鈕裡的功能
async function updateReviewFunc() {
  let spoilers = false;
  deleteMessage();
  if (userLogPlace.value === "") {
    makeMessage(messagePlace, "Type something, please");
  } else {
    watchedDate.value.replaceAll("-", "/");
    if (watchedDate.value === "") {
      watchedDate.value = null;
    }
    if (spoilersCheckBox.checked === true) {
      spoilers = true;
    }
    let data = {
      movieReview: userLogPlace.value,
      watchedDate: watchedDate.value,
      spoilers: spoilers,
    };
    console.log("for update review", data);
    let reviewUpdateMessage = await sendDataToBackend(
      "PATCH",
      data,
      `/api/user_profile/${userName}/reviews/films/${movieName}/${reviewId}`
    );
    if (reviewUpdateMessage === true) {
      window.location.reload();
    } else {
      makeMessage(messagePlace, reviewUpdateMessage);
    }
  }
}

// save review for other func
async function saveReviewForOthers() {
  console.log("not page master 555");
  let spoilers = false;
  let loggedUser = await getUserData();
  deleteMessage();
  if (userLogPlace.value === "") {
    makeMessage(messagePlace, "Type something, please");
  } else {
    watchedDate.value.replaceAll("-", "/");
    if (watchedDate.value === "") {
      watchedDate.value = null;
    }
    if (spoilersCheckBox.checked === true) {
      spoilers = true;
    }
    // 不是page擁有者

    let today = makeDateString();
    let data = {
      movieReview: userLogPlace.value,
      filmId: filmId,
      currentDate: today,
      watchedDate: watchedDate.value,
      userId: loggedUser["userId"],
      spoilers: spoilers,
      reviewId: reviewId,
    };
    console.log("for update review", data);
    let reviewUpdateMessage = await sendDataToBackend(
      "PATCH",
      data,
      `/api/review`
    );
    if (reviewUpdateMessage === true) {
      window.location.reload();
    } else {
      makeMessage(messagePlace, reviewUpdateMessage);
    }
  }
}

// 再寫一次的功能
async function reviewAgainFunc() {
  let spoilers = false;
  deleteMessage();
  if (userLogPlace.value === "") {
    makeMessage(messagePlace, "Type something, please");
  } else {
    watchedDate.value.replaceAll("-", "/");
    let today = makeDateString();
    if (watchedDate.value === "") {
      watchedDate.value = null;
    }
    if (spoilersCheckBox.checked === true) {
      spoilers = true;
    }

    let data = {
      movieReview: userLogPlace.value,
      filmId: null,
      currentDate: today,
      watchedDate: watchedDate.value,
      userId: null,
      spoilers: spoilers,
      reviewId: reviewId,
      from: "userProfileReviewAgain",
    };
    console.log("for review again", data);

    let reviewUpdateMessage = await sendDataToBackend(
      "PATCH",
      data,
      "/api/review"
    );
    if (reviewUpdateMessage === true) {
      window.location.reload();
    } else {
      makeMessage(messagePlace, reviewUpdateMessage);
    }
  }
}

// 拿電影均分
async function getAverageRate() {
  let data = {
    filmId: filmId,
  };
  console.log(data);
  let averageRate = await sendDataToBackend("POST", data, "/api/average-rate");
  console.log(averageRate, 156154);
  let mouseTextPlace = document.querySelector(".mouseTextPlace");
  if (averageRate !== undefined && averageRate["average"] !== null) {
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

showProperReviewBox();
showFilmInfo();
