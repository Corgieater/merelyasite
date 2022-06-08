"use strict";
let isMouseHover = false;
// 查詢用

// 字樣相關
let welcomePlace = document.querySelector(".welcomePlace");
// for little text around rows
let dynamicTextForNews = document.querySelector(".dynamicTextForNews");
let dynamicTextForNews2 = document.querySelector(".dynamicTextForNews2");
// reviews friends like
let dynamicTextForLikeReviews = document.querySelector(
  ".dynamicTextForLikeReviews"
);

// who logged and have friends
let newFromFriendsPlace = document.querySelector(".newFromFriendsPlace");
let reviewsWIthFriendsPlace = document.querySelector(
  ".reviewsWIthFriendsPlace"
);
// who no log or no friends
let justReviewdPlace = document.querySelector(".justReviewdPlace");
let popularThisWeekPlace = document.querySelector(".popularThisWeekPlace");

// check if user login
async function checkUserLogin() {
  let userData = await getUserData();
  if (userData.data !== null) {
    let userName = userData["userName"];
    let userId = userData["userId"];
    makeNewsFromFriends(userName);
    showReviewsFriendsLikeOrOtherPeopleLike(userId);
  } else {
    showSignUpLink(welcomePlace);
    makeNews();
    show(popularThisWeekPlace);
    showReviewsFriendsLikeOrOtherPeopleLike();
  }
}
// PEOPLE WHO NOT LOGIN
function showSignUpLink(welcomePlace) {
  let a = document.createElement("a");
  a.textContent = "Join us on Movie Notes!";
  a.href = "#";
  a.addEventListener("click", function (e) {
    e.preventDefault();
    show(mask);
    show(signUpPlace);
  });
  a.addEventListener("mouseover", function () {
    a.style.color = "darkcyan";
  });
  a.addEventListener("mouseout", function () {
    a.style.color = "antiquewhite";
  });
  welcomePlace.append(a);
}

// make news
async function makeNews() {
  let newReviews = await getNewReviewed();
  let totalReviews = newReviews.data["totalReviews"];
  newReviews = newReviews.data.data;
  // for sign up
  dynamicTextForNews.textContent = "JUST REVIEWED...";
  dynamicTextForNews2.textContent = `${totalReviews} films watched`;
  show(dynamicTextForNews);
  show(dynamicTextForNews2);
  for (let review of newReviews) {
    let li = document.createElement("li");
    let reviewedUserName = review["userName"];
    let reviewMovieTitle = review["reviewMovie"];
    let reviewMovieId = review["reviewMovieId"];
    let reviewId = review["reviewId"];
    let reviewedUserNameForHref = reviewedUserName.replaceAll(" ", "+");
    let reviewdMovieNameForHref = reviewMovieTitle.replaceAll(" ", "+");
    ("/user_profile/test/reviews/films/Pulp+Fiction/88");
    let content = `
    <a href="/user_profile/${reviewedUserNameForHref}/reviews/films/${reviewdMovieNameForHref}/${reviewId}">
      <img
        src="https://dwn6ych98b9pm.cloudfront.net/moviePos/img${reviewMovieId}.jpg"
        alt=""
      />
    </a>
    `;
    li.innerHTML = content;
    justReviewdPlace.append(li);
    justReviewdPlace.classList.add("fade");
  }
}

async function makePopularMoviesShow() {
  let popularMovies = await getMostPopularMoviesThisWeek();
  popularMovies = popularMovies.data.data;
  for (let movie of popularMovies) {
    let movidId = movie["movieId"];
    let totalLikes = movie["totalLikes"];
    let li = document.createElement("li");
    let content = `
    <a href="/film/${movidId}">
    <section class="imgPlace">
    <div class='posterMask hide'>
    <img src="../static/images/goldHeart.svg">
    <p>${totalLikes}<p>
    </div>
      <img
        src="https://dwn6ych98b9pm.cloudfront.net/moviePos/img${movidId}.jpg"
        alt=""
      />
    </section>
  </a>
    `;
    li.innerHTML = content;
    popularThisWeekPlace.append(li);
  }
  let posterMask = document.querySelectorAll(".posterMask");
  let popularPosters = document.querySelectorAll(".popularThisWeekPlace > li");

  for (let i = 0; i < popularPosters.length; i++) {
    popularPosters[i].addEventListener(
      "mouseover",
      function () {
        isMouseHover = true;
        show(posterMask[i]);
      },
      false
    );
    popularPosters[i].addEventListener(
      "mouseleave",
      function () {
        isMouseHover = false;
        hide(posterMask[i]);
      },
      false
    );
  }
}

makePopularMoviesShow();
// PEOPLE WHO LOGGED
// get news from friends
async function getNewsFromFriends() {
  let req = await fetch(`/api/user/follows/reviews`);
  const res = await req.json();
  return res;
}

// make news from friends
async function makeNewsFromFriends(userName) {
  let data = await getNewsFromFriends();
  let h2 = document.createElement("h2");
  if (data.data) {
    h2.textContent = `Hi ${userName}. Your friends have been watching...`;
    welcomePlace.append(h2);
    data = data.data.data;
    show(dynamicTextForNews);
    dynamicTextForNews.textContent = "NEW REVIEWS FROM FRIENDS";
    for (let info of data) {
      let li = document.createElement("li");
      let followingName = info["followUserName"];
      let followingReviewDate = info["reviewDate"].substring(0, 16);
      let followingNameForHref = info["followUserName"].replaceAll(" ", "+");
      let reviewdMovieNameForHref = info["movieTitle"].replaceAll(" ", "+");
      let reviewId = info["reviewId"];
      let reviewerImgId = info["reviewerImgId"];

      if (reviewerImgId === null) {
        reviewerImgId = "../static/images/user.png";
      } else {
        reviewerImgId = `https://dwn6ych98b9pm.cloudfront.net/userPic/${reviewerImgId}.jpg`;
      }

      let content = `
    <a href="/user_profile/${followingNameForHref}/reviews/films/${reviewdMovieNameForHref}/${reviewId}">
    <section class="headPlace">
      <section class="imgPlace">
        <img
          src=https://dwn6ych98b9pm.cloudfront.net/moviePos/img${info["movieId"]}.jpg
          alt="image"
        />
      </section>
      
      <section class="namePlace flex">
      <img class='userPic' src="${reviewerImgId}">
      ${followingName}
      </section>
    </section>
    <section class="footPlace flex">
      <section class="datePlace">${followingReviewDate}</section>
    </section>
    </a>
    `;
      li.innerHTML = content;
      newFromFriendsPlace.append(li);
    }
  } else {
    // 沒朋友就秀沒帳號的人的東西
    h2.textContent = `Hi ${userName}. Here’s what we’ve been watching…`;
    welcomePlace.append(h2);
    makeNews();
    show(popularThisWeekPlace);
  }
}

// show friends like reviews *4 or other people like if no firends
async function showReviewsFriendsLikeOrOtherPeopleLike(currentUserId = null) {
  let reviewFriendsLike = null;
  let reviewFriendsLikeLen = 0;
  let userData = await getUserData();
  let userName = userData["userName"];
  if (currentUserId !== null) {
    let req = await fetch(
      `/api/${currentUserId}/get_following_latest_like_reviews/`
    );
    let res = await req.json();
    reviewFriendsLike = res.data.data;
    reviewFriendsLikeLen = reviewFriendsLike.length;
    dynamicTextForLikeReviews.textContent = "REVIEWS YOUR FRIENDS LIKE";
  }
  if (reviewFriendsLikeLen === 0 || currentUserId === null) {
    // no friends
    let req = await fetch(`/api/most_popular_reviews/`);
    let res = await req.json();
    reviewFriendsLike = res.data.data;
    dynamicTextForLikeReviews.textContent = "MOST POPULAR REVIEWS";
  }
  for (let i = 0; i < reviewFriendsLike.length; i++) {
    let movieId = reviewFriendsLike[i]["movieId"];
    let movieTitle = reviewFriendsLike[i]["movieTitle"];
    let reviewer = reviewFriendsLike[i]["reviewer"];
    let review = reviewFriendsLike[i]["review"];
    let reviewId = reviewFriendsLike[i]["reviewId"];
    let spoilers = reviewFriendsLike[i]["spoilers"];
    // reviewers photo
    let reviewerImgId = reviewFriendsLike[i]["reviewerImgId"];
    reviewerImgId = reviewFriendsLike[i]["reviewerImgId"];

    if (reviewerImgId === null) {
      reviewerImgId = "../static/images/user.png";
    } else {
      reviewerImgId = `https://dwn6ych98b9pm.cloudfront.net/userPic/${reviewerImgId}.jpg`;
    }

    let reviewerNameForUrl = reviewer.replaceAll(" ", "+");
    let movieTitleForUrl = review.replaceAll(" ", "+");
    let reviewUrl = `/user_profile/${reviewerNameForUrl}/reviews/films/${movieTitleForUrl}/${reviewId}`;
    let li = document.createElement("li");
    let content = `
    <section class="flex">
    <img src="https://dwn6ych98b9pm.cloudfront.net/moviePos/img${movieId}.jpg" />
    <section class="likeReviewNamePlace flex">
      <section class='flex'>
      <img class='userPic' src="${reviewerImgId}">
      <a href="/user_profile/${reviewer}">${reviewer}</a>
      </section>
      <a href="${reviewUrl}">${movieTitle}</a>
    </section>
  </section>
  <section class="likeReviewPlace">
  </section>
    `;
    li.innerHTML = content;
    reviewsWIthFriendsPlace.append(li);
    let reviewP = document.createElement("p");
    reviewP.textContent = review;
    let likeReviewPlaces = document.querySelectorAll(".likeReviewPlace");
    if (spoilers && userName !== reviewer) {
      likeReviewPlaces[i].append(reviewP);
      reviewP.classList.add("hide");
      let alert = document.createElement("p");
      alert.textContent = "There are spoilers in this review!";
      let spoilerAlert = document.createElement("a");
      spoilerAlert.textContent = "I don't mind, let me read.";
      spoilerAlert.href = "#";
      likeReviewPlaces[i].append(alert);
      likeReviewPlaces[i].append(spoilerAlert);
      spoilerAlert.addEventListener("click", function (e) {
        e.preventDefault();
        reviewP.classList.remove("hide");
        alert.classList.add("hide");
        spoilerAlert.classList.add("hide");
      });
    } else {
      likeReviewPlaces[i].append(reviewP);
    }
    show(reviewsWIthFriendsPlace);
    show(dynamicTextForLikeReviews);
  }
}

// some func for people do not follow or no login
async function getMostPopularMoviesThisWeek() {
  const req = await fetch("/api/get_most_popular_movies_this_week/");
  const res = await req.json();
  return res;
}

async function getNewReviewed() {
  let req = await fetch(`/api/get_latest_reviews/`);
  const res = await req.json();
  return res;
}

// function addEventToPosters() {
//   console.log(popularPosters);
// }

checkUserLogin();
