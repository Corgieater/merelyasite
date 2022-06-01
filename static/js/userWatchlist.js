"use strict";
let pageMasterAndPage = cutUserInputAtLast("e/");
let showPlace = document.querySelector(".showPlace");
let totalMoviePlace = document.querySelector(".wrap > h2 > span");
async function getWatchlist() {
  const req = await fetch(`/api/user_profile/${pageMasterAndPage}`);
  const res = await req.json();
  console.log(res);
  return res;
}

async function showWatchlist() {
  let data = await getWatchlist();
  totalMoviePlace.textContent = data["data"]["totalMovies"];
  makePageTags("/user_profile", pageMasterAndPage, data["totalPages"]);
  data = data["data"]["data"];
  for (let info of data) {
    let li = document.createElement("li");
    let content = `
    <a href="film/${info[0]}"
    ><img src="https://dwn6ych98b9pm.cloudfront.net/moviePos/img${info[0]}.jpg" alt=""
  /></a>
    `;
    li.innerHTML = content;
    showPlace.append(li);
  }
}
showWatchlist();
