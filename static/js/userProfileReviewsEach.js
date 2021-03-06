"use strict";
// 一些表單用的資料
let movieId = null;
let lastTimeLogMessage = null;
let lastTimeSpoilers = null;
let lastTimeWatched = null;
let watchedDate = document.querySelector(
  '.reviewBox > section > input[type="date"]'
);
// review likesBt
let likesReviewBt = document.querySelector(".likesReviewBt");
let deleteLikesReviewBt = document.querySelector(".deleteLikesReviewBt");
// // 查詢用
let uncleanUrlForReviewId = cutUserInputAtLast("/films");
let uncleanUrlForMovieName = cutUserInputAtLast("/reviews");
let pageMaster = cutUserInputInMiddle("e/", "/r");
let pageMasterWithNoPlus = pageMaster.replaceAll("+", " ");
// 拿最後一個/然後找reviewID
let indexOfLastSlash = uncleanUrlForReviewId.lastIndexOf("/");
let reviewId = uncleanUrlForReviewId.slice(indexOfLastSlash + 1);
// 切MovieName
let indexOfStartMovieName = uncleanUrlForMovieName.indexOf("s/");
let endIndexOfMovieName = uncleanUrlForMovieName.lastIndexOf("/");
let movieName = uncleanUrlForMovieName.substring(
  indexOfStartMovieName + 2,
  endIndexOfMovieName
);

// 頁面區
let poster = document.querySelector(".posterPlace > img");
let userNameTag = document.querySelector(".userNameTag");
let title = document.querySelector(
  ".textPlace > div > section:nth-child(1) > section > h2 > a"
);
let year = document.querySelector(
  ".textPlace > div > section:nth-child(1) > section > p"
);
let lastTimeStarPlace = document.querySelector(
  ".textPlace > div > section:nth-child(1) > section:nth-child(2) > section"
);
let lastTimeWatchPlace = document.querySelector(
  ".textPlace > div > section:nth-child(1) > section:nth-child(2) > p"
);

// action small action
let smallActionsPlace = document.querySelector(".smallActionsPlace");
// 裡面的區域
let likeBtPlace = document.querySelector(".likeBtPlace");
let removeLikeBtPlace = document.querySelector(".removeLikeBtPlace");
let watchlistBtPlace = document.querySelector(".watchlistBtPlace");
let removeWatchlistBtPlace = document.querySelector(".removeWatchlistBtPlace");
// 區域裡面的button
let likeBt = document.querySelector(".likeBt");
let removeLikeBt = document.querySelector(".removeLikeBt");
let watchlistBt = document.querySelector(".watchlistBt");
let removeWatchlistBt = document.querySelector(".removeWatchlistBt");

// action區
let rateBtsPlace = document.querySelector(".rateBtsPlace");
let rateBts = document.querySelectorAll(".rateBtsPlace >input");
let cancelBt = document.querySelector(".cancelBt");
let editBt = document.querySelector(
  ".textPlace > div > section.actionBox > ul > li:nth-child(2) > a"
);
let reviewAgainBt = document.querySelector(
  ".textPlace > div > section.actionBox > ul > li:nth-child(3) > a"
);
let averageRatePlace = document.querySelector(".averagePlace");
averageRatePlace.title = "";
// let addListBt = document.querySelector(".actionBox > ul > li:nth-child(3) > a");

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
async function showProperReviewBox() {
  // 看有沒有登入
  const userIsLogged = await checkIfLogged();
  let isPageBelongsToLoggedUser = false;
  isPageBelongsToLoggedUser = await checkUserForPages(pageMasterWithNoPlus);

  // 沒登入接下來都不用看了
  if (userIsLogged === true) {
    show(smallActionsPlace);
    show(rateBtsPlace);
    show(watchlistBt);
    show(removeWatchlistBt);
    show(editBt);
    if (isPageBelongsToLoggedUser === false) {
      editBt.textContent = "Write a review";
      // 這邊要打API去查這user是有沒有寫過這電影的評論
      cancelBt.style.bottom = "90px";
    }
    if (isPageBelongsToLoggedUser) {
      // 屬於頁面使用者所以會有 reviewAgainBt要改一下cancelBt位置
      cancelBt.style.bottom = "90px";
      show(reviewAgainBt);
    }
  } else {
    let actionBox = document.querySelector(".actionBox > ul");
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
    averageRate.title = "";
    actionBox.insertBefore(li, averageRate);
  }
}

// small action func
// 加入movies likes
likeBt.addEventListener("click", async function (e) {
  e.preventDefault();
  smallActionFunc("PATCH", "/api/user_profile/likes/movie");
});

// delete from movies users likes
// delete from likes
removeLikeBtPlace.addEventListener("click", async function (e) {
  e.preventDefault();
  smallActionFunc("DELETE", "/api/user_profile/likes/movie");
});

// 加入待看清單
watchlistBt.addEventListener("click", async function (e) {
  e.preventDefault();
  smallActionFunc("PATCH", "/api/user_profile/watchlist");
});

// delete from watchlist
removeWatchlistBt.addEventListener("click", async function (e) {
  e.preventDefault();
  smallActionFunc("DELETE", "/api/user_profile/watchlist");
});

// 更新評分按鈕
// 打開評論區 - 編輯或更新上次的評分
editBt.addEventListener("click", async function (e) {
  e.preventDefault();
  let isPageBelongsToLoggedUser = await checkUserForPages(pageMasterWithNoPlus);
  if (isPageBelongsToLoggedUser) {
    // 因為跟review again共用空間 按鈕要分出來
    userLogPlace.value = lastTimeLogMessage;
    hideOrShow(reviewBox);
    show(mask);
    show(editSaveBt);
    hide(reviewAgainSaveBt);
    // 看上次spoiler是不是true
    spoilersCheckBox.checked = lastTimeSpoilers;
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
    updateReviewFunc();
  });
  saveBtForOthers.addEventListener("click", async function () {
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
    let loggedUserId = res["userId"];
    let data = {
      rate: rate,
      userId: loggedUserId,
      movieId: movieId,
    };

    // 送資料
    let ratingMessage = await sendDataToBackend("PATCH", data, "/api/rate");
    if (ratingMessage === true) {
      window.location.reload();
    } else {
      makeMessage(averageRatePlace, ratingMessage);
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
  rateToStars(rate);
}

// 刪除評分
cancelBt.addEventListener("click", async function (e) {
  e.preventDefault();
  for (let bt of rateBts) {
    bt.checked = false;
  }
  smallActionFunc("DELETE", "/api/rate");
});

// 拿review資料 拿PAGE MASTER的REVIEW
async function getReview() {
  const req = await fetch(
    `/api/user_profile/${pageMaster}/reviews/films/${movieName}/${reviewId}`
  );
  const res = await req.json();
  return res;
}

// 顯示電影資料/review
async function showFilmInfo() {
  let data = await getReview();
  let isPageBelongsToLoggedUser = false;
  isPageBelongsToLoggedUser = await checkUserForPages(pageMasterWithNoPlus);

  let userReview = document.querySelector(".userReview");
  data = data["data"];
  movieId = data["movieId"];
  // 順便檢查一下logger有沒有加這電影+review like 有userID的話
  if (currentUserId) {
    let userData = await getUserData();
    let userId = userData["userId"];
    checkUserMovieStates(userId, movieId);
    checkUserReviewState(userId, reviewId);
  }
  let filmTitle = data["movieTitle"];
  reviewTitle.textContent = filmTitle;
  let filmReview = data["movieReview"];
  userReview.textContent = filmReview;
  let filmYear = data["movieYear"];
  let filmUserRate = data["movieRate"];

  let filmSpoiler = data["spoiler"];
  let filmWatchedDate = data["watchedDate"];
  let filmReviewDate = data["reviewDate"];
  userNameTag.href = `/user_profile/${pageMaster}`;
  if (filmWatchedDate === null) {
    filmWatchedDate = filmReviewDate;
  }
  lastTimeWatched = filmWatchedDate;
  lastTimeLogMessage = filmReview;
  if (filmSpoiler && !isPageBelongsToLoggedUser) {
    let antiSpoilers = document.querySelector(".antiSpoilers");
    let antiSpoilersBt = document.querySelector(".antiSpoilers > a");
    show(antiSpoilers);
    antiSpoilersBt.addEventListener("click", function (e) {
      e.preventDefault();
      hide(antiSpoilers);
      show(userReview);
    });
  } else {
    show(userReview);
  }

  lastTimeSpoilers = filmSpoiler;
  poster.src = `https://dwn6ych98b9pm.cloudfront.net/moviePos/img${movieId}.jpg`;
  reviewPoster.src = `https://dwn6ych98b9pm.cloudfront.net/moviePos/img${movieId}.jpg`;
  title.textContent = filmTitle;
  title.href = `/film/${movieId}`;
  year.textContent = filmYear;
  year.href = `/year?year=${filmYear}`;

  lastTimeWatchPlace.textContent = `Watched on 
  ${filmWatchedDate.substring(0, 16)}`;

  // make starts 在review本區的小星星jpg
  // 因為是在看該PAGE所以小星星要照page master的評論跑
  if (filmUserRate !== null) {
    if (filmUserRate !== "0.5") {
      let fullStarRate = parseInt(filmUserRate);
      for (let j = 0; j < fullStarRate; j++) {
        let img = document.createElement("img");
        img.src = "/static/images/star.png";
        lastTimeStarPlace.append(img);
      }
    }
    let halfStarRate = filmUserRate.toString().search(".5");
    if (halfStarRate !== -1) {
      let img = document.createElement("img");
      img.src = "/static/images/half_star.png";
      lastTimeStarPlace.append(img);
    }
  }
  getAverageRate();
  // page master秀上次的評分星星
  if (isPageBelongsToLoggedUser) {
    showPreviousRate(filmUserRate);
  } else {
    // not page master show if this outsider had ratted
    let logger = await getUserData();
    let loggerId = logger["userId"];
    let loggerRate = await fetch(`/api/rate/${loggerId}/${movieId}`);
    loggerRate = await loggerRate.json();
    loggerRate = loggerRate.data.rate;
    showPreviousRate(loggerRate);
  }
}

deleteReviewBt.addEventListener("click", async function (e) {
  e.preventDefault();
  const req = await fetch(
    `/api/user_profile/${pageMaster}/reviews/films/${movieName}/${reviewId}`,
    {
      method: "DELETE",
    }
  );
  const res = await req.json();
  if (res.ok) {
    window.location.replace(`/user_profile/${pageMaster}/reviews?page=1`);
  } else {
    makeMessage(messagePlace, res.message);
  }
});

// like reviewbt
likesReviewBt.addEventListener("click", async function (e) {
  e.preventDefault();
  let userData = await getUserData();
  let userId = userData["userId"];
  let data = {
    reviewId: reviewId,
    userId: userId,
  };
  let likeThisReview = await sendDataToBackend(
    "PATCH",
    data,
    "/api/user_profile/likes/review"
  );
  if (likeThisReview === true) {
    window.location.reload();
  }
});

// delete like reviewbt
deleteLikesReviewBt.addEventListener("click", async function (e) {
  e.preventDefault();
  let userData = await getUserData();
  let userId = userData["userId"];
  let data = {
    reviewId: reviewId,
    userId: userId,
  };
  let deleteFromReviewLike = await sendDataToBackend(
    "DELETE",
    data,
    "/api/user_profile/likes/review"
  );
  if (deleteFromReviewLike === true) {
    window.location.reload();
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

// 更新review按鈕
async function updateReviewFunc() {
  let spoilers = false;
  let userData = await getUserData();
  let userName = userData["userName"];
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

//有登入沒登入都沒關係的功能
async function getAverageRate() {
  let data = {
    movieId: movieId,
  };
  let averageRate = await sendDataToBackend("POST", data, "/api/average_rate");
  if (averageRate !== undefined && averageRate["average"] !== null) {
    averageRatePlace.textContent = `Average rate ${averageRate["average"]}`;
    averageRatePlace.style.cursor = "pointer";
    averageRatePlace.title = `Based on ${averageRate["totalCount"]} ratings`;
  } else {
    averageRatePlace.textContent = `No one rated yet`;
  }
}

// 拿電影均分
async function getAverageRate() {
  let data = {
    movieId: movieId,
  };
  let averageRate = await sendDataToBackend("POST", data, "/api/average_rate");
  if (averageRate !== undefined && averageRate["average"] !== null) {
    averageRatePlace.textContent = `Average rate ${averageRate["average"]}`;
    averageRatePlace.style.cursor = "pointer";
    averageRatePlace.title = `Based on ${averageRate["totalCount"]} ratings`;
  } else {
    averageRatePlace.textContent = `No one rated yet`;
  }
}

// 登入才有

// 不是page擁有者的寫評論功能
async function saveReviewForOthers() {
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
      movieId: movieId,
      currentDate: today,
      watchedDate: watchedDate.value,
      userId: loggedUser["userId"],
      spoilers: spoilers,
      reviewId: reviewId,
    };

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

// page擁有者的再寫一次的功能
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
      movieId: null,
      currentDate: today,
      watchedDate: watchedDate.value,
      userId: null,
      spoilers: spoilers,
      reviewId: reviewId,
      from: "userProfileReviewAgain",
    };

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

showProperReviewBox();
showFilmInfo();
