"use strict";
let userNameAngPage = cutUserInputAtLast("e/");
let userName = cutUserInputInMiddle("e/", "/r");
let page = cutUserInputAtLast("e=");
let userProfileWatchlistBt = document.querySelector(".userProfileWatchlistBt");
let userProfileHomeBt = document.querySelector(".userProfileHomeBt");
let userProfileLikesBt = document.querySelector(".userProfileLikesBt");

// user profile nav bar
userProfileWatchlistBt.href = `/user_profile/${userName}/watchlist?page=1`;
userProfileHomeBt.href = `/user_profile/${userName}`;
userProfileLikesBt.href = `/user_profile/${userName}/likes`;

async function getLatestFiveReviews() {
  const req = await fetch(`/api/get_reviews_by_page/${userNameAngPage}`);
  const res = await req.json();
  console.log("resdata", res);
  return res;
}

async function showRecentlyReviews() {
  let data = await getLatestFiveReviews();
  let reviewdPlace = document.querySelector(".reviewdPlace");
  let pageBelongsToLoggedUser = await checkUserForPages(
    userName.replaceAll("+", " ")
  );

  for (let i = 0; i < data["data"].length; i++) {
    let li = document.createElement("li");
    li.classList.add("flex");
    let info = data["data"][i];
    let watchedDay = info["watchedDay"];
    let reviewDay = info["reviewDay"];
    let date = null;
    const movieId = info["movieId"];
    let filmTitle = info["filmTitle"];
    let filmTitleForHref = filmTitle.replaceAll(" ", "+");

    const review = info["review"];
    const reviewId = info["reviewId"];
    const spoilers = info["spoilers"];
    // 把後面的時間切掉
    if (watchedDay !== null) {
      date = `Watched on ${watchedDay.substring(0, 16)}`;
    } else {
      // 如果使用者沒填watched day 就拿填表日期來用
      date = `Reviewd on ${reviewDay.substring(0, 16)}`;
    }
    const reviewPage = `/user_profile/${userName}/reviews/films/${filmTitleForHref}/${reviewId}`;
    let content = `
      <div>
      <img
        src="https://dwn6ych98b9pm.cloudfront.net/moviePos/img${movieId}.jpg"
        alt="img"
      />
    </div>
    <div class='reviewBody'>
    <section class='flex'>
      <a href="${reviewPage}">${filmTitle}</a>
      <p>${info["filmYear"]}</p>
    </section>
      <section class="starPlace"></section>
      <p>${date}</p>
      <p class="reviewText"></p>;
    </div>
      `;
    li.innerHTML = content;

    reviewdPlace.append(li);
    let reviewText = document.querySelectorAll(".reviewText")[i];

    // 不是page擁有者就要防spoiler
    if (spoilers && pageBelongsToLoggedUser === false) {
      makeSpoilersAlert(reviewText, review);
    } else {
      reviewText.textContent = review;
    }
  }
  makePageTags("user_profile/", userNameAngPage, data["totalPages"]);
}
showRecentlyReviews();
