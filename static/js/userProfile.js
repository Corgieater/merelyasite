"use strict";
let userName = cutUserInputAtLast("e/");
console.log(userName);
let userNameWithNoPlus = userName.replaceAll("+", " ");
let userProfileReviewsBt = document.querySelector(".userProfileReviewsBt");
let userProfileWatchlistBt = document.querySelector(".userProfileWatchlistBt");
userProfileReviewsBt.href = `/user_profile/${userName}/reviews?page=1`;
userProfileWatchlistBt.href = `/user_profile/${userName}/watchlist?page=1`;

// 使用者相關按鈕
let editProfileBt = document.querySelector(".edditProfileBt");
let followBt = document.querySelector(".followBt");
let unFollowBt = document.querySelector(".unFollowBt");

// 給滑鼠移動到unfollowBt上用的
let isMouseHover = false;

// *************起來要做unfollow事件
// *************要想辦法抓到追蹤跟被追蹤數
// *************滑鼠移動到folowbt的時候要不要做個效果?
// *************沒follow到要顯示global news嗎?
// *************userProfileReviewEach裡面不是該頁面擁有者的星星是壞的 要修 表示要準備兩套星星?

// 追隨事件
followBt.addEventListener("click", async function (e) {
  e.preventDefault();
  let message = await following_page_master();
  if (message === true) {
    window.location.reload();
  } else {
    makeMessage(globalMessagePlace, message);
  }
});
// 把滑鼠移到following上會變成unfollowing
unFollowBt.addEventListener(
  "mouseover",
  function () {
    isMouseHover = true;
    unFollowBt.classList.add("unFollow");
    unFollowBt.textContent = "UNFOLLOW";
  },
  false
);
unFollowBt.addEventListener(
  "mouseleave",
  function () {
    isMouseHover = false;
    unFollowBt.classList.remove("unFollow");
    unFollowBt.textContent = "FOLLOWING";
  },
  false
);

// 看這頁面屬不屬於使用者判斷顯示什麼
async function checkUserBelongs() {
  let isThePageBelongsToLoggedUser = await checkUserForPages(
    userName.replaceAll("+", " ")
  );
  if (isThePageBelongsToLoggedUser === false) {
    console.log("page not belong to the logger");
    is_following();
  } else if (isThePageBelongsToLoggedUser === true) {
    console.log("yes master");
    show(editProfileBt);
  }
}

// 追蹤別人
async function following_page_master() {
  let loggedUser = await getUserData();

  let data = {
    following: userNameWithNoPlus,
    follower: loggedUser["userId"],
  };
  const followingMessage = await sendDataToBackend(
    "PATCH",
    data,
    `/api/user_profile/follows`
  );
  return followingMessage;
}

// 確認有沒有追蹤
async function is_following() {
  console.log(`/api/user_profile/${userNameWithNoPlus}`);
  const req = await fetch(`/api/user_profile/${userNameWithNoPlus}`);
  const res = await req.json();
  console.log(res);
  if (res.ok) {
    hide(followBt);
    show(unFollowBt);
  } else {
    show(followBt);
    hide(unFollowBt);
  }
}

// 拿最近五個reviews
async function getLatestFiveReviews() {
  const req = await fetch(`/api/get_latest_reviews/${userName}`);
  const res = await req.json();
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
    const filmId = info["filmId"];
    const filmTitle = info["filmTitle"];
    const filmTitleForHref = filmTitle.replaceAll(" ", "+");
    const review = info["review"];
    const reviewId = info["reviewId"];
    const spoilers = info["spoilers"];
    // 把後面的時間切掉
    if (watchedDay !== null) {
      console.log("use watched day");
      date = `Watched on ${watchedDay.substring(0, 16)}`;
    } else {
      console.log("reivewDay");
      // 如果使用者沒填watched day 就拿填表日期來用
      date = `Reviewd on ${reviewDay.substring(0, 16)}`;
    }
    const reviewPage = `/user_profile/${userName}/reviews/films/${filmTitleForHref}/${reviewId}`;
    // ("/user_profile/<user_name>/reviews/films/<movie_name>/<review_id></review_id>");
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
    // let userRate = info["userRate"];
    // console.log(userRate, "userrate");
    let starPlace = document.querySelectorAll(".starPlace");
    let reviewBody = document.querySelectorAll(".reviewBody")[i];
    let reviewText = document.querySelectorAll(".reviewText")[i];
    // if (userRate !== null) {
    //   if (userRate !== "0.5") {
    //     let fullStarRate = parseInt(userRate);
    //     for (let j = 0; j < fullStarRate; j++) {
    //       let img = document.createElement("img");
    //       img.src = "../static/images/star.png";
    //       starPlace[i].append(img);
    //     }
    //   }
    //   console.log(userRate, "beffor finding fhasl");
    //   let halfStarRate = userRate.toString().search(".5");
    //   if (halfStarRate !== -1) {
    //     let img = document.createElement("img");
    //     img.src = "../static/images/half_star.png";
    //     starPlace[i].append(img);
    //   }
    // }
    // 不是page擁有者就要防spoiler 是擁有者就讓他知道這是spoiler就好
    if (spoilers && pageBelongsToLoggedUser !== true) {
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
    } else if (spoilers && pageBelongsToLoggedUser == true) {
      let p = document.createElement("p");
      p.textContent = "This review may contain spoilers.";
      reviewBody.insertBefore(p, reviewText);
    }
  }
}

// 小功能

checkUserBelongs();
showRecentlyReviews();
// is_following();
