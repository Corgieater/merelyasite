"use strict";
let userNameAngPage = cutUserInputAtLast("e/");
let userName = cutUserInputInMiddle("e/", "/r");

let page = cutUserInputAtLast("e=");

// // 看這頁面屬不屬於使用者判斷顯示什麼
// async function checkUserBelongs() {
//   let isThePageBelongsToLoggedUser = await checkUserForPages(
//     userName.replaceAll("+", " ")
//   );
//   if (isThePageBelongsToLoggedUser === false) {
//     return
//   } else {
//     console.log("yes master");
//   }
// }

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
  console.log("11111", pageBelongsToLoggedUser);

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
    const reviewPage = `/user_profile/${userName}/reviews/films/${filmTitleForHref}/${reviewId}`;
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
    // 不是page擁有者就要防spoiler 是擁有者就讓他知道這是spoiler就好
    if (spoilers && pageBelongsToLoggedUser === false) {
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
    } else {
      let p = document.createElement("p");
      p.textContent = "This review may contain spoilers.";
      reviewBody.insertBefore(p, reviewText);
    }
  }
  console.log("userName from userprofilereviews", userName);
  makePageTags("user_profile/", userNameAngPage, data["totalPages"]);
}
showRecentlyReviews();
