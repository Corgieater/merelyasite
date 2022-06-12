"use strict";
let userName = cutUserInputInMiddle("file/", "/likes");
let userNameWithNoPlus = userName.replaceAll("+", " ");
let userProfileReviewsBt = document.querySelector(".userProfileReviewsBt");
let userProfileWatchlistBt = document.querySelector(".userProfileWatchlistBt");
let userProfileHomeBt = document.querySelector(".userProfileHomeBt");

let moviesUserLikesAllBt = document.querySelector(".moviesUserLikesAllBt");
let reviewsUserLikesAllBt = document.querySelector(".reviewsUserLikesAllBt");

userProfileReviewsBt.href = `/user_profile/${userName}/reviews?page=1`;
userProfileWatchlistBt.href = `/user_profile/${userName}/watchlist?page=1`;
userProfileHomeBt.href = `/user_profile/${userName}`;
moviesUserLikesAllBt.href = `/user_profile/${userName}/likes/allMovies?page=1`;
reviewsUserLikesAllBt.href = `/user_profile/${userName}/likes/allReviews?page=1`;
// movies user likes
let moviePosPlace = document.querySelector(".moviePosPlace");
let reviewPlace = document.querySelector(".reviewPlace");

async function getMoviesUserLikes() {
  let req = await fetch(`/api/user_profile/${userName}/likes/movies`);
  let res = await req.json();
  return res;
}

async function getReviewsUserLikes() {
  let req = await fetch(`/api/user_profile/${userName}/likes/reviews`);
  let res = await req.json();
  return res;
}
async function showMoviesUserLiks() {
  let data = await getMoviesUserLikes();
  if (data !== data.error) {
    data = data.data.data;
    for (let i = 0; i < data.length; i++) {
      let li = document.createElement("li");
      let movieId = data[i][0];
      let content = ` 
      <a href="/film/${movieId}">
      <img
        src="https://dwn6ych98b9pm.cloudfront.net/moviePos/img${movieId}.jpg"
        />
        </a>`;
      li.innerHTML = content;
      moviePosPlace.append(li);
    }
  }
}

async function showReviewsUserLikes() {
  let data = await getReviewsUserLikes();
  if (data !== data.error) {
    let currentUserData = await getUserData();
    let currentUserName = currentUserData["userName"];
    data = data.data.data;
    for (let i = 0; i < data.length; i++) {
      let li = document.createElement("li");
      let movieId = data[i]["movieId"];
      let movieTitle = data[i]["movieTitle"];
      let movieTitleForUrl = movieTitle.replaceAll(" ", "+");
      let review = data[i]["review"];
      let reviewId = data[i]["reviewId"];
      let reviewer = data[i]["reviewer"];
      let reviewerNameForUrl = reviewer.replaceAll(" ", "+");
      let reviewerImg = data[i]["reviewerImg"];
      if (reviewerImg === null) {
        reviewerImg = "/static/images/user.png";
      } else {
        reviewerImg = `https://dwn6ych98b9pm.cloudfront.net/userPic/${reviewerImg}.jpg`;
      }
      let spoilers = data[i]["spoilers"];
      let year = data[i]["year"];
      let reviewUrl = `/user_profile/${reviewerNameForUrl}/reviews/films/${movieTitleForUrl}/${reviewId}`;
      let reviewerProfileUrl = `/user_profile/${reviewerNameForUrl}`;
      let content = `
        <div>
        <img
          src="https://dwn6ych98b9pm.cloudfront.net/moviePos/img${movieId}.jpg"
          alt="img"
        />
        </div>
        <div class="reviewBody">
        <section class="flex">
          <a href="${reviewUrl}">${movieTitle}</a>
          <p>${year}</p>
        </section>
        <section class="flex">
          <img
            src="${reviewerImg}"
          />
          <a href="${reviewerProfileUrl}">${reviewer}</a>
        </section>
        <p class="reviewText"></p>
        </div>
        `;
      li.innerHTML = content;
      li.classList.add("flex");
      reviewPlace.append(li);

      // 如果不是此user profile page擁有者 防雷
      let reviewTexts = document.querySelectorAll(".reviewText");
      if (spoilers && userName.replaceAll("+", " ") !== currentUserName) {
        makeSpoilersAlert(reviewTexts[i], review);
      } else {
        reviewTexts[i].textContent = review;
      }
    }
  }
}

showMoviesUserLiks();
showReviewsUserLikes();
