"use strict";
// let frame = document.querySelector(".frame");
// // colletions
// let movieCollectionsBt = document.querySelector(
//   ".searchCollections > a:nth-child(1)"
// );
// let reviewsCollectionsBt = document.querySelector(
//   ".searchCollections > a:nth-child(2)"
// );
// let directorsCollectionsBt = document.querySelector(
//   ".searchCollections > a:nth-child(3)"
// );
// let actorsCollectionsBt = document.querySelector(
//   ".searchCollections > a:nth-child(4)"
// );
let userName = cutUserInputAtLast("e/");
let page = cutUserInputAtLast("e=");
console.log(userName, page);
// movieCollectionsBt.href = `/search?keyword=${keyword}&page=1`;
// reviewsCollectionsBt.href = `/review?${keyword}&page=1`;
// // review要考慮show什麼
// directorsCollectionsBt.href = `/search/director?director=${keyword}&page=1`;
// actorsCollectionsBt.href = `/search/actor?actor=${keyword}&page=1`;

async function getLatestFiveReviews() {
  // /api/get_reviews_by_page/<user_name>/reviews
  const req = await fetch(`/api/get_reviews_by_page/${userName}`);
  const res = await req.json();
  console.log("resdata", res);
  return res;
}

async function redirectIfNotLogin() {
  const userLoged = await checkIfLogged();
  if (!userLoged) {
    window.location.replace("/");
  }
}

async function showRecentlyReviews() {
  let data = await getLatestFiveReviews();
  let reviewdPlace = document.querySelector(".reviewdPlace");

  for (let i = 0; i < data["data"].length; i++) {
    let li = document.createElement("li");
    li.classList.add("flex");
    let info = data["data"][i];
    let watchedDay = info["watchedDay"];
    let reviewDay = info["reviewDay"];
    let date = null;
    const filmId = info["filmId"];
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
    const reviewPage = `/user_profile/${userName}/films/${filmTitleForHref}/${reviewId}`;
    let content = `
      <div>
      <img
        src="https://dwn6ych98b9pm.cloudfront.net/moviePos/img${filmId}.jpg"
        alt="img"
      />
    </div>
    <div class='reviewBody'>
      <a href="${reviewPage}">${filmTitle}</a>
      <a href="#">${info["filmYear"]}</a>
      <section class="starPlace"></section>
      <p>${date}</p>
      <p class='reviewText'>${review}</p>
    </div>
  </li>
      `;
    li.innerHTML = content;
    reviewdPlace.append(li);
    let userRate = info["userRate"];
    let starPlace = document.querySelectorAll(".starPlace");
    let reviewBody = document.querySelectorAll(".reviewBody")[i];
    let reviewText = document.querySelectorAll(".reviewText")[i];
    if (userRate !== null) {
      if (userRate !== "0.5") {
        let fullStarRate = parseInt(userRate);
        for (let j = 0; j < fullStarRate; j++) {
          let img = document.createElement("img");
          img.src = "/static/images/star.png";
          starPlace[i].append(img);
        }
      }
      let halfStarRate = userRate.toString().search(".5");
      if (halfStarRate !== -1) {
        let img = document.createElement("img");
        img.src = "/static/images/half_star.png";
        starPlace[i].append(img);
      }
    }
    // 這個理論上是給外人用的 user profile不用 但我先寫好
    if (spoilers) {
      reviewText.classList.add("hide");
      let alert = document.createElement("p");
      alert.textContent = "There are spoilers in this review!";
      let spoilerAlert = document.createElement("a");
      spoilerAlert.textContent = "I don't mind, let me read.";
      spoilerAlert.href = "#";
      spoilerAlert.addEventListener("click", function (e) {
        e.preventDefault();
        reviewText.classList.remove("hide");
        alert.classList.add("hide");
        spoilerAlert.classList.add("hide");
      });

      reviewBody.insertBefore(spoilerAlert, reviewText);
      reviewBody.insertBefore(alert, spoilerAlert);
    }
  }
  makePageTags("user_profile/", userName, data["totalPages"]);
}
redirectIfNotLogin();
showRecentlyReviews();

// // 做資料
// async function renderDataInfo() {
//   let data = await getData();
//   let userInput = data[1];
//   makeShowRow(data, userInput);
// }

// // 先打API去要資料 多頁用
// async function getData() {
//   let userInputAndPage = cutUserInputAtLast("e/");
//   console.log(userInputAndPage);
//   let req = await fetch(`/api/get_reviews_by_page/${userInputAndPage}`);
//   console.log(`/api/search?keyword=${userInputAndPage}`);
//   const res = await req.json();
//   if (res.data) {
//     return [res, userInputAndPage];
//   } else {
//     return res.message;
//   }
// }

// async function makeShowRow(data, userInputAndPage) {
//   // 沒東西就不用做了
//   console.log(data);
//   if (typeof data === "string") {
//     makeMessage(frame, data);
//   } else {
//     let showPlace = document.querySelector(".frame > ul");
//     data = data[0];

//     //   use for of for async func
//     for (const info of data.data) {
//       let id = info["id"];
//       let title = info["title"];
//       let year = info["year"];
//       let directors = info["directors"];
//       console.log(directors);
//       let li = document.createElement("li");
//       let div1 = document.createElement("div");
//       let div2 = document.createElement("div");
//       let div3 = document.createElement("div");
//       let img = document.createElement("img");
//       let a1 = document.createElement("a");
//       let a2 = document.createElement("a");
//       let p = document.createElement("p");
//       img.src = `https://dwn6ych98b9pm.cloudfront.net/moviePos/img${id}.jpg`;
//       a1.href = `/film/${id}`;
//       a2.href = `/film/${year}`;
//       a1.textContent = title + " ";
//       a2.textContent = year;
//       p.textContent = "Directed by ";
//       div1.append(img);
//       div2.append(a1);
//       div2.append(a2);
//       div2.append(p);
//       div3.append(div1);
//       div3.append(div2);
//       div3.classList.add("showRow");
//       div3.classList.add("flex");
//       makeAlinkAndAppend(p, "/director?director=", directors);
//       li.append(div3);
//       showPlace.append(li);
//     }
//   }
//   makePageTags("search?keyword", userInputAndPage, data["totalPages"]);
// }

// // 小功能

// renderDataInfo();
