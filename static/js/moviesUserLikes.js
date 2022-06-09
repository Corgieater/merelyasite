"use strict";
let pageMasterAndPage = cutUserInputAtLast("e/");
let pageMaster = cutUserInputInMiddle("file/", "/likes");
let showPlace = document.querySelector(".showPlace");
let totalMoviePlace = document.querySelector(".wrap > h2 > span");
let isMouseHover = false;

let userProfileReviewsBt = document.querySelector(".userProfileReviewsBt");
let userProfileHomeBt = document.querySelector(".userProfileHomeBt");
let userProfileLikesBt = document.querySelector(".userProfileLikesBt");

// user profile nav bar
userProfileReviewsBt.href = `/user_profile/${pageMaster}/reviews?page=1`;
userProfileHomeBt.href = `/user_profile/${pageMaster}`;
userProfileLikesBt.href = `/user_profile/${pageMaster}/likes`;

async function getAllMoviesUserLikes() {
  const req = await fetch(
    `/api/user_profile/${pageMaster}/likes/allMovies?page=1`
  );
  const res = await req.json();
  console.log(res);
  return res;
}

async function showAllMoviesUserLikes() {
  let data = await getAllMoviesUserLikes();
  makePageTags("user_profile/", pageMasterAndPage, data["totalPages"]);
  data = data["data"]["data"];
  for (let i = 0; i < data.length; i++) {
    let li = document.createElement("li");
    li.classList.add("posterFrame");
    let filmId = data[i][0];
    let content = `
    <div class='posterMask hide'>
    <section class='flex'>
    <a target="_blank" href="/film/${filmId}"> 
    <img src="/static/images/external-link-s.svg"/>
    </a>
    <a class="removeWatchlistBt hide" href="#">
    <img src="/static/images/trash-s.svg"/>
    </a>
    </section>
    </div>
    <img class="moviePos"src="https://dwn6ych98b9pm.cloudfront.net/moviePos/img${filmId}.jpg"/>
   
    `;
    li.innerHTML = content;
    showPlace.append(li);
    let userData = await getUserData();
    let userId = userData["userId"];
    // 沒登入就不會秀出removeLikesBts
    if (userId !== undefined) {
      let removeLikesBts = document.querySelectorAll(".removeWatchlistBt");
      show(removeWatchlistBts[i]);
      removeLikesBts[i].addEventListener("click", async function (e) {
        e.preventDefault();
        let data = {
          movieId: filmId,
          userId: userId,
        };

        let removeFromWatchlistMessage = await sendDataToBackend(
          "DELETE",
          data,
          "/api/user_profile/watchlist"
        );
        if (removeFromWatchlistMessage === true) {
          window.location.reload();
          makeMessage(
            globalMessagePlace,
            `${movieName} was removed from your watchlist`,
            "good"
          );
        }
      });
    }
  }
  let posterMask = document.querySelectorAll(".posterMask");
  let posterFrame = document.querySelectorAll(".posterFrame");
  for (let i = 0; i < posterFrame.length; i++) {
    posterFrame[i].addEventListener(
      "mouseover",
      function () {
        isMouseHover = true;
        show(posterMask[i]);
      },
      false
    );
    posterFrame[i].addEventListener(
      "mouseleave",
      function () {
        isMouseHover = false;
        hide(posterMask[i]);
      },
      false
    );
  }
}

showAllMoviesUserLikes();
