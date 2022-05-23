"use strict";
let director = cutUserInputInMiddle("r/", "&");
console.log(director, "directorjs");
let posterPlace = document.querySelector(".posterPlace");

async function makePosterLi(directorMovieId) {
  for (let id of directorMovieId) {
    let li = document.createElement("li");
    let img = document.createElement("img");
    let aLink = document.createElement("a");
    aLink.href = `/film/${id}`;
    aLink.append(img);
    img.src = `https://dwn6ych98b9pm.cloudfront.net/moviePos/img${id}.jpg`;
    li.append(aLink);
    posterPlace.append(li);
  }
}
async function getMovieByDirector() {
  let req = await fetch(`/api/director/${director}`);
  let res = await req.json();
  console.log(res);
  let idList = await res["data"]["directorMovieId"];
  makePosterLi(idList);
}
getMovieByDirector();
