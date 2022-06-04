"use strict";
let isMouseHover = false;
// 查詢用

// 字樣相關
let welcomePlace = document.querySelector(".welcomePlace");
// for little text around rows
let dynamicTextForNews = document.querySelector(".dynamicTextForNews");
let dynamicTextForNews2 = document.querySelector(".dynamicTextForNews2");

// who logged and have friends
let newFromFriendsPlace = document.querySelector(".newFromFriendsPlace");
// who no log or no driends
let justReviewdPlace = document.querySelector(".justReviewdPlace");
let popularThisWeekPlace = document.querySelector(".popularThisWeekPlace");

// check if user login
async function checkUserLogin() {
  let userData = await getUserData();
  if (userData.data !== null) {
    let userName = userData["userName"];
    makeNewsFromFriends(userName);
  } else {
    showSignUpLink(welcomePlace);
    makeNews();
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
  }
}

async function makePopularMoviesShow() {
  let popularMovies = await getMostPopularThisWeek();
  popularMovies = popularMovies.data.data;
  console.log(popularMovies);
  // popularMovies = popularMovies.data;
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
  console.log(data);
  if (data.data) {
    h2.textContent = `Hi ${userName}. Your friends have been watching...`;
    welcomePlace.append(h2);
    data = data.data.data;
    show(dynamicTextForNews);
    dynamicTextForNews.textContent = "NEW FROM FRIENDS";
    for (let info of data) {
      let li = document.createElement("li");
      let followingName = info["followUserName"];
      let followingReviewDate = info["reviewDate"].substring(0, 16);
      let followingNameForHref = info["followUserName"].replaceAll(" ", "+");
      let reviewdMovieNameForHref = info["movieTitle"].replaceAll(" ", "+");
      let reviewId = info["reviewId"];
      let content = `
    <a href="/user_profile/${followingNameForHref}/reviews/films/${reviewdMovieNameForHref}/${reviewId}">
    <section class="headPlace">
      <section class="imgPlace">
        <img
          src=https://dwn6ych98b9pm.cloudfront.net/moviePos/img${info["movieId"]}.jpg
          alt="image"
        />
      </section>
      <section class="namePlace">${followingName}</section>
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
    h2.textContent = `Hi ${userName}. Here’s what we’ve been watching…`;
    welcomePlace.append(h2);
    makeNews();
  }
}

// some func for people do not follow or no login
async function getMostPopularThisWeek() {
  const req = await fetch("/api/get_most_popular_movies_this_week/");
  const res = await req.json();
  return res;
}

async function getNewReviewed() {
  let req = await fetch(`/api/get_latest_reviews/`);
  const res = await req.json();
  console.log(res);
  return res;
}

function addEventToPosters() {
  console.log(popularPosters);
}

checkUserLogin();
