"use strict";
// let genre = cutUserInput("e/");
let href = window.location.href;
let genre = cutUserInputAtLast("e=");
// let page = cutUserInputAtLast("ge=");
let posterPlace = document.querySelector(".posterPlace");

async function makePosterLi(movieIdList) {
  for (let movie of movieIdList) {
    let li = document.createElement("li");
    let img = document.createElement("img");
    let aLink = document.createElement("a");
    aLink.href = `/film/${movie["movieId"]}`;
    aLink.append(img);
    img.src = `https://dwn6ych98b9pm.cloudfront.net/moviePos/img${movie["movieId"]}.jpg`;
    li.append(aLink);
    posterPlace.append(li);
  }
}
async function getMovieByDirector() {
  let req = await fetch(`/api/genre?genre=${genre}&page=1`);
  let res = await req.json();
  let movieIdList = await res["data"]["data"];
  makePosterLi(movieIdList);
  let userInputAndPage = cutUserInputAtLast("e=");
  makePageTags("genre?genre=", userInputAndPage, res["totalPages"]);
}
getMovieByDirector();
