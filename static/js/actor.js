"use strict";
let actor = cutUserInputInMiddle("r=");
// let page = cutUserInputAtLast("ge=");
let posterPlace = document.querySelector(".posterPlace");

async function makePosterLi(idList) {
  for (let id of idList) {
    let li = document.createElement("li");
    let img = document.createElement("img");
    let aLink = document.createElement("a");
    aLink.href = `/film/${id}`;
    aLink.append(img);
    img.src = `https://dwn6ych98b9pm.cloudfront.net/posters/img${id}.jpg`;
    li.append(aLink);
    posterPlace.append(li);
  }
}
async function getMovieByDirector() {
  let req = await fetch(`/api/actor?actor=${actor}&page=1`);
  let res = await req.json();
  let idList = await res["data"]["id_list"];
  makePosterLi(idList);
}
getMovieByDirector();
