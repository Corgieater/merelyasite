"use strict";
// 查詢用

// 字樣相關
let welcomePlace = document.querySelector(".welcomePlace");
let dynamicTextForNews = document.querySelector(".dynamicTextForNews");

let newFromFriendsPlace = document.querySelector(".newFromFriendsPlace");
let justReviewdPlace = document.querySelector(".justReviewdPlace");

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
async function getNewReviewed() {
  let req = await fetch(`/api/get_latest_reviews/`);
  const res = await req.json();
  console.log(res);
  return res;
}

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
  show(dynamicTextForNews);
}

// make news
async function makeNews() {
  let data = await getNewReviewed();
  data = data.data.data;
  // for sign up
  dynamicTextForNews.textContent = "JUST REVIEWED...";
  for (let info of data) {
    let li = document.createElement("li");
    let reviewedUserName = info["userName"];
    let reviewMovieTitle = info["reviewMovie"];
    let reviewMovieId = info["reviewMovieId"];
    let reviewId = info["reviewId"];
    let reviewedUserNameForHref = reviewedUserName.replaceAll(" ", "+");
    let reviewdMovieNameForHref = reviewMovieTitle.replaceAll(" ", "+");
    ("http://localhost:3000/user_profile/test/reviews/films/Pulp+Fiction/88");
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

checkUserLogin();
