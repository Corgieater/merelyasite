"use strict";
// 查詢用
let movieId = cutUserInputAtLast("m/");
let movieName = null;

// 頁面區
let poster = document.querySelector(".posterPlace > img");
let title = document.querySelector(".headArea > section :nth-child(1)");
let year = document.querySelector(".headArea > section :nth-child(2)");
let tagline = document.querySelector(".headArea > section :nth-child(3)");
let directors = document.querySelector(".directorsPlace");
let plot = document.querySelector(".plot > p");
let casts = document.querySelector(".casts");
let genres = document.querySelector(".genres");

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
let rate = document.querySelector(".rate");
let rateBts = document.querySelectorAll("input[type='radio']");
let cancelBt = document.querySelector(".cancelBt");
let reviewBt = document.querySelector(".actionBox>ul>li:nth-child(2)>a");
let averageRatePlace = document.querySelector(
  ".actionBox > ul > li:nth-child(4)"
);
let userLogPlace = document.querySelector("#review");

// review區
let reviewBox = document.querySelector(".reviewBox");
let dateCheckBox = document.querySelector("#watched");
let spoilersCheckBox = document.querySelector("#spoilers");
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
  if (userIsLogged === true) {
    show(smallActionsPlace);
    show(rate);
    show(watchlistBt);
    show(removeWatchlistBt);
    show(reviewBt);
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
  // 有登入沒登入都可以秀
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

// 寫評分按鈕
// 打開評論區
reviewBt.addEventListener("click", function (e) {
  e.preventDefault();
  hideOrShow(reviewBox);
  show(mask);
  spoilersCheckBox.disabled = true;
  // 如果沒打心得不給勾spoiler
  userLogPlace.addEventListener("input", function () {
    if (userLogPlace.value !== "") {
      spoilersCheckBox.disabled = false;
    } else {
      spoilersCheckBox.disabled = true;
    }
  });
});

// 顯示日期按鈕
dateCheckBox.addEventListener("click", function () {
  hideOrShow(dateInputPlace);
});

// 儲存評論
saveBt.addEventListener("click", async function () {
  let messagePlace = document.querySelector(
    ".reviewBox > section:nth-child(2)"
  );
  // 有殘留的global message就刪掉
  deleteMessage();
  // 如果沒打字就不給存
  if (userLogPlace.value === "") {
    makeMessage(messagePlace, "Type something, please");
  } else {
    const req = await fetch("/api/user");
    const res = await req.json();

    let id = res["userId"];

    let watchedDate = document.querySelector(
      '.reviewBox > section > input[type="date"]'
    );
    let spoilers = false;

    watchedDate.value.replaceAll("-", "/");
    if (watchedDate.value === "") {
      watchedDate.value = null;
    }
    if (spoilersCheckBox.checked === true) {
      spoilers = true;
    }
    let today = makeDateString();
    let data = {
      movieReview: userLogPlace.value,
      movieId: movieId,
      currentDate: today,
      watchedDate: watchedDate.value,
      userId: id,
      spoilers: spoilers,
    };
    sendDataToBackend("PATCH", data, "/api/review");
    hide(reviewBox);
    hide(mask);
    userLogPlace.value = "";
    dateCheckBox.checked = false;
    watchedDate.value = "";
    spoilersCheckBox.checked = false;
    hide(watchedDate);
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
      let data = {
        rate: rate,
        userId: id,
        movieId: movieId,
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

// 拿該使用者對該電影的評分;
async function getUserRate() {
  const req = await fetch("/api/user");
  const res = await req.json();
  let userId = res["userId"];
  let userRate = await fetch(`/api/rate/${userId}/${movieId}`);
  userRate = await userRate.json();
  userRate = userRate.data.rate;

  return userRate;
}

// 顯示之前的評分星星
async function showPreviousRate() {
  let data = await getUserRate();
  let rate = null;
  if (data === null) {
    hide(cancelBt);
    return (rate = 0);
  } else {
    rate = data;
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

// 拿電影資料
async function getFilm() {
  const req = await fetch(`/api/film/${movieId}`);
  const res = await req.json();
  return res;
}

// 顯示電影資料
async function showFilmInfo() {
  let data = await getFilm();
  // 拿一下user資料
  data = data["data"];
  let movieId = data["movieId"];
  let filmTitle = data["title"];
  movieName = filmTitle;
  let filmTagline = data["tagline"];
  reviewTitle.textContent = data["title"];
  let filmYear = data["year"];
  let filmDirectors = data["directors"];
  let filmPlot = data["story"];
  let filmStars = data["actors"];
  let filmGenres = data["genres"];
  // 如果有登入就驗一下
  if (currentUserId) {
    checkUserMovieStates();
  }
  poster.src = `https://dwn6ych98b9pm.cloudfront.net/moviePos/img${movieId}.jpg`;
  reviewPoster.src = `https://dwn6ych98b9pm.cloudfront.net/moviePos/img${movieId}.jpg`;
  title.textContent = filmTitle;
  year.textContent = filmYear;
  tagline.textContent = filmTagline;
  year.href = `/year?year=${filmYear}`;
  plot.textContent = filmPlot;
  makeAlinkAndAppend(directors, "/director?director=", filmDirectors);
  makeAlinkAndAppend(casts, `/actor?actor=`, filmStars);
  makeAlinkAndAppend(genres, "/search/genre?genre=", filmGenres);
}

// check if user add this movie to watchlist or likes
async function checkUserMovieStates() {
  let userData = await getUserData();
  let userId = userData["userId"];
  let userMovieStates = await fetch(`/api/user_profile/user_movie_state/
  ${userId}/${movieId}`);
  userMovieStates = await userMovieStates.json();
  userMovieStates = userMovieStates.data;
  let ifMovielist = userMovieStates["userWatchlist"];
  let ifMovieLikes = userMovieStates["userLikes"];
  if (ifMovielist) {
    show(removeWatchlistBtPlace);
  }
  if (!ifMovielist) {
    show(watchlistBtPlace);
  }
  if (ifMovieLikes) {
    show(removeLikeBtPlace);
  }
  if (!ifMovieLikes) {
    show(likeBtPlace);
  }
}

// 拿電影均分
async function getAverageRate() {
  let data = {
    movieId: movieId,
  };
  let averageRate = await sendDataToBackend("POST", data, "/api/average-rate");
  if (averageRate !== undefined && averageRate["average"] !== null) {
    averageRatePlace.textContent = `Average rate ${averageRate["average"]}`;
    averageRatePlace.style.cursor = "pointer";
    averageRatePlace.title = `Based on ${averageRate["totalCount"]} ratings`;
  } else {
    averageRatePlace.textContent = `No one rated yet`;
  }
}

showFilmInfo();
showProperReviewBox();
showPreviousRate();
getAverageRate();
