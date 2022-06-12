"use strict";
let actor = cutUserInputAtLast("r=");
// let page = cutUserInputAtLast("ge=");
let posterPlace = document.querySelector(".posterPlace");

async function makePosterLi(movieIds) {
  for (let id of movieIds) {
    let movieId = id;
    let li = document.createElement("li");
    let img = document.createElement("img");
    let aLink = document.createElement("a");
    aLink.href = `/film/${movieId}`;
    aLink.append(img);
    img.src = `https://dwn6ych98b9pm.cloudfront.net/moviePos/img${movieId}.jpg`;
    li.append(aLink);
    posterPlace.append(li);
  }
}
async function getMovieByDirector() {
  let req = await fetch(`/api/actor?actor=${actor}&page=1`);
  let res = await req.json();
  if (res.data) {
    let movieIds = await res["data"]["actorMovieId"];
    makePosterLi(movieIds);
    let userInputAndPage = cutUserInputAtLast("r=");
    makePageTags("actor?actor=", userInputAndPage, res["totalPages"]);
  }
}
getMovieByDirector();
