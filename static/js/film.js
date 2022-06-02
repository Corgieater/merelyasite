"use strict";
// 查詢用
let filmId = cutUserInputAtLast("m/");
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
let watchlistBtPlace = document.querySelector(".watchlistBtPlace");
let removeWatchlistBtPlace = document.querySelector(".removeWatchlistBtPlace");
let watchlistBt = document.querySelector(".watchlistBt");
let removeWatchlistBt = document.querySelector(".removeWatchlistBt");

// action區
let rate = document.querySelector(".rate");
let rateBts = document.querySelectorAll("input[type='radio']");
let cancelBt = document.querySelector(".cancelBt");
let reviewBt = document.querySelector(".actionBox>ul>li:nth-child(2)>a");
let addListBt = document.querySelector(".actionBox > ul > li:nth-child(3) > a");
let averageRatePlace = document.querySelector(
  ".actionBox > ul > li:nth-child(5)"
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
  console.log(userIsLogged);
  if (userIsLogged === true) {
    show(smallActionsPlace);
    show(rate);
    show(watchlistBt);
    show(removeWatchlistBt);
    show(reviewBt);
    show(addListBt);
  } else {
    let actionBox = document.querySelector(".actionBox > ul");
    // actionBox.style.height = "200px";
    let li = document.createElement("li");
    let p = document.createElement("p");
    let mouseTextPlace = document.querySelector(".mouseTextPlace");
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
    mouseTextPlace.style.top = "440px";
    actionBox.insertBefore(li, averageRate);
  }
}

showProperReviewBox();

// 加入待看清單
watchlistBt.addEventListener("click", async function (e) {
  e.preventDefault();
  let userData = await getUserData();
  let userId = userData["userId"];
  let data = {
    movieId: filmId,
    userId: userId,
  };
  let addToWatchlistMessage = await sendDataToBackend(
    "PATCH",
    data,
    "/api/user_profile/watchlist"
  );
  if (addToWatchlistMessage === true) {
    window.location.reload();
    makeMessage(
      globalMessagePlace,
      `${movieName} was added to your watchlist`,
      "good"
    );
  }
});

// delete from watchlist
removeWatchlistBt.addEventListener("click", async function (e) {
  e.preventDefault();
  let userData = await getUserData();
  let userId = userData["userId"];
  let data = {
    movieId: filmId,
    userId: userId,
  };
  let addToWatchlistMessage = await sendDataToBackend(
    "DELETE",
    data,
    "/api/user_profile/watchlist"
  );
  if (addToWatchlistMessage === true) {
    window.location.reload();
    makeMessage(
      globalMessagePlace,
      `${movieName} was removed from your watchlist`,
      "good"
    );
  }
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
  deleteMessage();
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
      filmId: filmId,
      currentDate: today,
      watchedDate: watchedDate.value,
      userId: id,
      spoilers: spoilers,
    };
    console.log("datatata", data);
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

// 拿該使用者對該電影的評分;
async function getUserRate() {
  const req = await fetch("/api/user");
  const res = await req.json();
  let id = res["userId"];
  let data = {
    filmId: filmId,
    userId: id,
  };
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

// 拿電影均分
async function getAverageRate() {
  let data = {
    filmId: filmId,
  };
  let averageRate = await sendDataToBackend("POST", data, "/api/average-rate");
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

// 拿電影資料
async function getFilm() {
  const req = await fetch(`/api/film/${filmId}`);
  const res = await req.json();
  console.log("getFIlm", res);
  return res;
}

// 顯示電影資料
async function showFilmInfo() {
  let data = await getFilm();
  // 拿一下user資料
  data = data["data"];
  let filmId = data["movieId"];
  let filmTitle = data["title"];
  movieName = filmTitle;
  let filmTagline = data["tagline"];
  reviewTitle.textContent = data["title"];
  let filmYear = data["year"];
  let filmDirectors = data["directors"];
  let filmPlot = data["story"];
  let filmStars = data["actors"];
  let filmGenres = data["genres"];
  poster.src = `https://dwn6ych98b9pm.cloudfront.net/moviePos/img${filmId}.jpg`;
  reviewPoster.src = `https://dwn6ych98b9pm.cloudfront.net/moviePos/img${filmId}.jpg`;
  title.textContent = filmTitle;
  year.textContent = filmYear;
  tagline.textContent = filmTagline;
  year.href = `/year?year=${filmYear}`;
  plot.textContent = filmPlot;
  makeAlinkAndAppend(directors, "/director?director=", filmDirectors);
  makeAlinkAndAppend(casts, `/actor?actor=`, filmStars);
  makeAlinkAndAppend(genres, "/genre?genre=", filmGenres);
}

// check if user add this movie to watchlist
async function checkIfMovieInWatchlist() {
  let userData = await getUserData();
  let userId = userData["userId"];
  let data = {
    movieId: filmId,
    userId: userId,
  };
  let movieInWatchlist = await sendDataToBackend(
    "POST",
    data,
    "/api/user_profile/watchlist"
  );
  console.log(movieInWatchlist);
  if (movieInWatchlist === true) {
    show(removeWatchlistBtPlace);
  } else {
    show(watchlistBtPlace);
  }
}

showFilmInfo();
showPreviousRate();
getAverageRate();
checkIfMovieInWatchlist();
