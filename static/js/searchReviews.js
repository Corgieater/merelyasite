"use strict";

let frame = document.querySelector(".frame");
// other colletions
let movieCollectionsBt = document.querySelector(
  ".otherCollections > li:nth-child(2) > a"
);
let reviewsCollectionsBt = document.querySelector(
  ".otherCollections > li:nth-child(3) > a"
);
let directorsCollectionsBt = document.querySelector(
  ".otherCollections > li:nth-child(4) > a"
);
let actorsCollectionsBt = document.querySelector(
  ".otherCollections > li:nth-child(5) > a"
);

let keyword = cutUserInputInMiddle("s=", "&");

movieCollectionsBt.href = `/search?keyword=${keyword}&page=1`;
reviewsCollectionsBt.href = `/search/reviews?reviews=${keyword}&page=1`;
directorsCollectionsBt.href = `/search/director?director=${keyword}&page=1`;
actorsCollectionsBt.href = `/search/actor?actor=${keyword}&page=1`;

// 做資料
async function renderDataInfo() {
  let data = await getData();
  if (data === undefined) {
    makeMessage(frame, "There is no such keyword, please check it again");
  } else {
    let userInput = data[1];
    makeShowRow(data, userInput);
  }
}

// 先打API去要資料 多頁用
async function getData() {
  let userInputAndPage = cutUserInputAtLast("s=");
  let req = await fetch(`/api/search/reviews?reviews=${userInputAndPage}`);
  const res = await req.json();
  if (res.data) {
    return [res, userInputAndPage];
  } else {
    return res.message;
  }
}

async function makeShowRow(data, userInputAndPage) {
  // 沒東西就不用做了
  makePageTags(
    "search/reviews?reviews=",
    userInputAndPage,
    data[0]["totalPages"]
  );
  if (typeof data === "string") {
    makeMessage(frame, data);
  } else {
    let showPlace = document.querySelector(".showPlace");
    data = data[0]["data"].data;
    for (let i = 0; i < data.length; i++) {
      let li = document.createElement("li");
      let movieId = data[i]["movieId"];
      let movieTitle = data[i]["movieTitle"];
      let review = data[i]["review"];
      let reviewId = data[i]["reviewId"];
      let reviewUserName = data[i]["reviewUserName"];
      let spoilers = data[i]["spoilers"];
      let year = data[i]["year"];
      let movieTitleForHref = movieTitle.replaceAll(" ", "+");
      let userNameForHref = reviewUserName.replaceAll(" ", "+");

      let reviewPageHref = `/user_profile/${userNameForHref}/reviews/films/${movieTitleForHref}/${reviewId}`;
      let userPageHref = `/user_profile/${userNameForHref}`;

      let reviewerImg = data[i]["reviewUserImgId"];
      if (reviewerImg === null) {
        reviewerImg = "/static/images/user.png";
      } else {
        reviewerImg = `https://dwn6ych98b9pm.cloudfront.net/userPic/${reviewerImg}.jpg`;
      }
      let content = `
      <section>
      <a href="${reviewPageHref}">
      <img src="https://dwn6ych98b9pm.cloudfront.net/moviePos/img${movieId}.jpg">
      </a>
      </section>

      <section>
        <section class="flex">
          <a href="${reviewPageHref}"><h3>${movieTitle}</h3></a>
          <a href="">${year}</a>
        </section>
        <section class='reviewBody'>
        <img src="${reviewerImg}">
          <a href="${userPageHref}">${reviewUserName}</a>
          <p class='reviewPlace'></p>
        </section>
      </section>
      `;

      li.classList.add("flex");
      li.innerHTML = content;
      showPlace.append(li);

      // 防雷
      let reviewPlaces = document.querySelectorAll(".reviewPlace");
      if (spoilers) {
        makeSpoilersAlert(reviewPlaces[i], review);
      } else {
        reviewPlaces[i].textContent = review;
      }
    }
  }
}

renderDataInfo();

function isEllipsisActive(e) {
  return e.offsetHeight < e.scrollHeight;
}
