"use strict";
let actor = cutUserInputAtLast("r=");
console.log(actor);
// let page = cutUserInputAtLast("ge=");
let posterPlace = document.querySelector(".posterPlace");

async function makePosterLi(movieDat) {
  for (let data of movieDat) {
    let movieId = data["movieId"];
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
  console.log(res);
  let movieData = await res["data"]["data"];
  makePosterLi(movieData);
}
getMovieByDirector();
