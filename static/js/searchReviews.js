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
  let userInput = data[1];
  makeShowRow(data, userInput);
}

// 先打API去要資料 多頁用
async function getData() {
  let userInputAndPage = cutUserInputAtLast("s=");
  console.log(userInputAndPage);
  let req = await fetch(`/api/search/reviews?reviews=${userInputAndPage}`);
  console.log(`/api/search/reviews?reviews=${userInputAndPage}`);
  const res = await req.json();
  if (res.data) {
    return [res, userInputAndPage];
  } else {
    return res.message;
  }
}

async function makeShowRow(data, userInputAndPage) {
  // 沒東西就不用做了
  console.log(data);
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
    console.log(data);
    //   use for of for async func
    // (const info of data)
    for (let i = 0; i < data.length; i++) {
      // console.log(info);
      let li = document.createElement("li");
      let movieId = data[i]["movieId"];
      let movieTitle = data[i]["movieTitle"];
      let review = data[i]["review"];
      let reviewId = data[i]["reviewId"];
      let reviewUserId = data[i]["reviewUserId"];
      let reviewUserName = data[i]["reviewUserName"];
      let spoilers = data[i]["spoilers"];
      let year = data[i]["year"];
      let movieTitleForHref = movieTitle.replaceAll(" ", "+");
      let userNameForHref = reviewUserName.replaceAll(" ", "+");

      let reviewPageHref = `/user_profile/${userNameForHref}/reviews/films/${movieTitleForHref}/${reviewId}`;
      let userPageHref = `/user_profile/${userNameForHref}`;

      let content = `
      <section>
      <a href="${reviewPageHref}">
      <img src="https://dwn6ych98b9pm.cloudfront.net/moviePos/img${movieId}.jpg" alt="">
      </a>
      </section>

      <section>
        <section class="flex">
          <a href="${reviewPageHref}"><h3>${movieTitle}</h3></a>
          <a href="">${year}</a>
        </section>
        <section class='reviewBody'>
          <a href="${userPageHref}">${reviewUserName}</a>
          <p class='reviewPlace'>${review}</p>
        </section>
      </section>
      `;
      // IT WAS IN UP THERE
      //   <section>
      //   <a href="#">Like this review</a>
      //   <a href="#">10 likes</a>
      // </section>
      li.classList.add("flex");
      li.innerHTML = content;
      showPlace.append(li);
      let reviewPlaces = document.querySelectorAll(".reviewPlace");
      let reviewBodies = document.querySelectorAll(".reviewBody");
      if (spoilers) {
        // let reviewBodies = document.querySelectorAll(".reviewBody");
        // let reviewPlaces = document.querySelectorAll(".reviewPlace");
        let alert = document.createElement("p");
        reviewPlaces[i].classList.add("hide");
        alert.textContent = "There are spoilers in this review!";
        let spoilerAlert = document.createElement("a");
        spoilerAlert.textContent = "I don't mind, let me read.";
        spoilerAlert.href = "#";
        spoilerAlert.addEventListener("click", function (e) {
          e.preventDefault();
          reviewPlaces[i].classList.remove("hide");
          alert.classList.add("hide");
          spoilerAlert.classList.add("hide");
        });
        reviewBodies[i].insertBefore(spoilerAlert, reviewPlaces[i]);
        reviewBodies[i].insertBefore(alert, spoilerAlert);
      }
      // 本來是想做偵測有沒有ellipses然後加入a tag可以讓使用者點開
      // 但我現在沒心力
      // else {
      //   let ellipsisActive = isEllipsisActive(reviewPlaces[i]);
      //   if (ellipsisActive) {
      //     let a = document.createElement("a");
      //     a.href = "#";
      //     a.textContent = "more";
      //     a.style.color = "white";
      //     reviewBodies[i].append(a);
      //     a.addEventListener("click", function (e) {
      //       e.preventDefault();
      //       let dot = reviewPlaces[i].innerHTML.lastIndexOf("...");
      //       console.log(dot);
      //     });
      //   }
      // }
    }
    // let reviewPlaces = document.querySelectorAll(".reviewPlace");
    // let reviewBody = document.querySelector(".reviewBody");
    // if (spoilers) {
    //   console.log(reviewPlace);
    //   reviewPlace.classList.add("hide");
    //   let alert = document.createElement("p");
    //   alert.textContent = "There are spoilers in this review!";
    //   let spoilerAlert = document.createElement("a");
    //   spoilerAlert.textContent = "I don't mind, let me read.";
    //   spoilerAlert.href = "#";
    //   spoilerAlert.addEventListener("click", function (e) {
    //     e.preventDefault();
    //     reviewText.classList.remove("hide");
    //     alert.classList.add("hide");
    //     spoilerAlert.classList.add("hide");
    //   });
    //   reviewBody.insertBefore(spoilerAlert, reviewPlace);
    //   reviewBody.insertBefore(alert, spoilerAlert);
  }
}

renderDataInfo();

function isEllipsisActive(e) {
  return e.offsetHeight < e.scrollHeight;
}
