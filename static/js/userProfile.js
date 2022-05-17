"use strict";
const userName = cutUserInput("e/");

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
    let watchedDate = null;
    let info = data["data"][i];
    console.log(info);
    if (info["watchedDay"] !== null) {
      // 把後面的時間切掉
      watchedDate = info["watchedDay"].substring(0, 16);
    } else {
      watchedDate = info["reviewDay"].substring(0, 16);
    }
    let content = `
      <div>
      <img
        src="https://dwn6ych98b9pm.cloudfront.net/posters/img${info["filmId"]}.jpg"
        alt="img"
      />
    </div>
    <div>
      <a href="/film/${info["filmId"]}">${info["filmTitle"]}</a>
      <a href="#">${info["filmYear"]}</a>
      <section class="starPlace"></section>
      <p>${watchedDate}</p>
      <p class='reviewText'>${info["review"]}</p>
    </div>
  </li>
      `;
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
      console.log(halfStarRate);
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
