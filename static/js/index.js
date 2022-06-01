"use strict";
// 查詢用

let newFromFriendsPlace = document.querySelector(".newFromFriendsPlace");
let welcomePlace = document.querySelector(".welcomePlace");

async function getNewsFromFriend() {
  let req = await fetch(`/api/user/follows/reviews`);
  const res = await req.json();
  console.log(res);
  if (res.data) {
    return res;
  } else {
    return res.message;
  }
}

async function make_news() {
  let data = await getNewsFromFriend();
  let userData = await getUserData();
  let newFromFriendWords = document.querySelector("body > div.wrap > h2.hide");
  welcomePlace.textContent = `Hi ${userData["userName"]}. Your friends have been watching...`;
  data = data.data.data;
  show(newFromFriendWords);
  for (let info of data) {
    let li = document.createElement("li");
    let followingName = info["followUserName"];
    let followingReviewDate = info["reviewDate"].substring(0, 16);
    let followingNameForHref = info["followUserName"].replaceAll(" ", "+");
    let reviewdMovieNameForHref = info["movieTitle"].replaceAll(" ", "+");
    console.log(followingNameForHref, reviewdMovieNameForHref);
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
}
make_news();
