// 做spoiler alert
function makeSpoilersAlert(placeNeedToAntiSpoilers, review) {
  let alert = document.createElement("p");
  alert.textContent = "There are spoilers in this review!";
  alert.classList.add("spoilerAlertText");
  let spoilerAlert = document.createElement("a");
  spoilerAlert.textContent = "I don't mind, let me read.";
  spoilerAlert.classList.add("spoilerAlert");

  placeNeedToAntiSpoilers.append(alert);
  placeNeedToAntiSpoilers.append(spoilerAlert);
  spoilerAlert.addEventListener("click", function (e) {
    e.preventDefault();
    hide(alert);
    hide(spoilerAlert);
    placeNeedToAntiSpoilers.textContent = review;
  });
}

// watchlist functions 填入動作以及api地址
// 給右邊的watchlist和Like rate用
async function smallActionFunc(action, api) {
  let userData = await getUserData();
  let userId = userData["userId"];
  let data = {
    movieId: movieId,
    userId: userId,
  };
  let watchlistAction = await sendDataToBackend(action, data, api);
  if (watchlistAction === true) {
    window.location.reload();
  }
}
// /api/user_profile/user_review_state/<user_id>/<review_id></review_id>
// check if user likes this review
async function checkUserReviewState(userId, reviewId) {
  let userReviewState = await fetch(
    `/api/user_profile/user_review_state/${userId}/${reviewId}`
  );
  userReviewState = await userReviewState.json();
  console.log(userReviewState.data);
  userReviewState = userReviewState.data;
  let ifReviewLikes = userReviewState["userLikes"];
  console.log(ifReviewLikes);
  if (ifReviewLikes) {
    show(deleteLikesReviewBt);
  } else {
    show(likesReviewBt);
  }
}

// check if user add this movie to watchlist or likes
async function checkUserMovieStates(userId, movieId) {
  let userMovieStates = await fetch(
    `/api/user_profile/user_movie_state/${userId}/${movieId}`
  );
  userMovieStates = await userMovieStates.json();
  userMovieStates = userMovieStates.data;
  let ifMovielist = userMovieStates["userWatchlist"];
  let ifMovieLikes = userMovieStates["userLikes"];
  if (ifMovielist) {
    show(removeWatchlistBtPlace);
    console.log(removeWatchlistBtPlace);
  }
  if (!ifMovielist) {
    show(watchlistBtPlace);
    console.log(watchlistBtPlace);
  }
  if (ifMovieLikes) {
    show(removeLikeBtPlace);
    console.log(removeLikeBtPlace);
  }
  if (!ifMovieLikes) {
    show(likeBtPlace);
    console.log(likeBtPlace);
  }
}

// 轉換分數成星星
function rateToStars(rate) {
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
