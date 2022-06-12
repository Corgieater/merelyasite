"use strict";
let userNameAngPage = cutUserInputAtLast("_profile/");
let userName = cutUserInputInMiddle("file/", "/like");
let page = cutUserInputAtLast("e=");
let userProfileWatchlistBt = document.querySelector(".userProfileWatchlistBt");
let userProfileHomeBt = document.querySelector(".userProfileHomeBt");
let userProfileLikesBt = document.querySelector(".userProfileLikesBt");

// user profile nav bar
userProfileWatchlistBt.href = `/user_profile/${userName}/watchlist?page=1`;
userProfileHomeBt.href = `/user_profile/${userName}`;
userProfileLikesBt.href = `/user_profile/${userName}/likes`;

async function getReviewsUserLikes() {
  const req = await fetch(`/api/user_profile/${userNameAngPage}`);
  const res = await req.json();
  return res;
}

async function showReviewsUserLikes() {
  let data = await getReviewsUserLikes();
  makePageTags("user_profile/", userNameAngPage, data.data["totalPages"]);
  let reviewPlace = document.querySelector(".reviewdPlace");
  let pageBelongsToLoggedUser = await checkUserForPages(
    userName.replaceAll("+", " ")
  );
  data = data.data.data;
  for (let i = 0; i < data.length; i++) {
    let li = document.createElement("li");
    li.classList.add("flex");
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
    let reviewDay = data[i]["reviewDate"];
    let spoilers = data[i]["spoilers"];
    let year = data[i]["year"];

    // 把後面的時間切掉
    reviewDay = `Reviewd on ${reviewDay.substring(0, 16)}`;
    const reviewUrl = `/user_profile/${reviewerNameForUrl}/reviews/films/${movieTitleForUrl}/${reviewId}`;
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
      <p>${reviewDay}</p>
    </section>
    <p class="reviewText"></p>
    </div>
      `;
    li.innerHTML = content;
    li.classList.add("flex");
    reviewPlace.append(li);
    // 如果不是此user profile page擁有者 防雷
    let reviewTexts = document.querySelectorAll(".reviewText");
    if (spoilers && !pageBelongsToLoggedUser) {
      makeSpoilersAlert(reviewTexts[i], review);
    } else {
      reviewTexts[i].textContent = review;
    }
  }
  makePageTags("user_profile/", userNameAngPage, data["totalPages"]);
}

showReviewsUserLikes();
