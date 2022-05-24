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
    const spoilers = info["spoilers"];
    console.log("spoilers", typeof spoilers);
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
    } else {
      console.log("we are good");
    }
  }
}
getLatestFiveReviews();
redirectIfNotLogin();
showRecentlyReviews();
