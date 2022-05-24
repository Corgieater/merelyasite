"use strict";
const userName = cutUserInputAtLast("e/");

async function getLatestFiveReviews() {
  const req = await fetch(`/api/get_latest_reviews/${userName}`);
  const res = await req.json();
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
  console.log(data);

  for (let i = 0; i < data["data"].length; i++) {
    let li = document.createElement("li");
    li.classList.add("flex");
    let info = data["data"][i];
    console.log(info);
    let watchedDay = info["watchedDay"];
    let reviewDay = info["reviewDay"];
    let date = null;
    console.log("watchedDay", watchedDay);
    const filmId = info["filmId"];
    const filmTitle = info["filmTitle"];
    const review = info["review"];
    const reviewId = info["reviewId"];
    // 把後面的時間切掉
    if (watchedDay !== null) {
      console.log("use watched day");
      date = `Watched on ${watchedDay.substring(0, 16)}`;
    } else {
      console.log("reivewDay");
      // 如果使用者沒填watched day 就拿填表日期來用
      date = `Reviewd on ${reviewDay.substring(0, 16)}`;
    }
    const reviewPage = `/user_profile/${userName}/films/${filmTitle}/${reviewId}`;
    let content = `
      <div>
      <img
        src="https://dwn6ych98b9pm.cloudfront.net/moviePos/img${filmId}.jpg"
        alt="img"
      />
    </div>
    <div class='reviewBody'>
      <a href="/film/${reviewPage}">${filmTitle}</a>
      <a href="#">${info["filmYear"]}</a>
      <section class="starPlace"></section>
      <p>${date}</p>
      <p class='reviewText'>${review}</p>
    </div>
  </li>
      `;
    // let watchdDatePlace = document.querySelector(
    //   "ul > li:nth-child(1) > div.reviewBody > p:nth-child(4)"
    // );

    // if (watchedDay === null) {

    // }else{

    // }
    li.innerHTML = content;
    reviewdPlace.append(li);
    let userRate = info["userRate"];
    let starPlace = document.querySelectorAll(".starPlace");
    if (userRate !== null) {
      if (userRate !== "0.5") {
        let fullStarRate = parseInt(userRate);
        for (let j = 0; j < fullStarRate; j++) {
          let img = document.createElement("img");
          img.src = "../static/images/star.png";
          starPlace[i].append(img);
        }
      }
      let halfStarRate = userRate.search(".5");
      if (halfStarRate !== -1) {
        let img = document.createElement("img");
        img.src = "../static/images/half_star.png";
        starPlace[i].append(img);
      }
    }
  }
}
getLatestFiveReviews();
redirectIfNotLogin();
showRecentlyReviews();
