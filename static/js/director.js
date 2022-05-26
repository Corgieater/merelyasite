"use strict";
let director = cutUserInputAtLast("r=");
// this need to be take care, include actor's part and actor's html
// actor's message showing
console.log(director, "directorjs");
let posterPlace = document.querySelector(".posterPlace");
let frame = document.querySelector(".frame");

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
  let req = await fetch(`/api/director?director=${director}&page=1`);
  let res = await req.json();
  if (res.data) {
    let idList = await res["data"]["directorMovieId"];
    makePosterLi(idList);
    let userInputAndPage = cutUserInputAtLast("r=");
    makePageTags("director?director", userInputAndPage, res["totalPages"]);
  } else {
    console.log(res);
    console.log(frame);
    makeMessage(frame, res.message);
  }
}

async function makeShowRow(data, userInputAndPage) {
  // 沒東西就不用做了
  console.log(data);
  if (typeof data === "string") {
    makeMessage(frame, data);
  } else {
    let showPlace = document.querySelector(".frame > ul");
    data = data[0];

    //   use for of for async func
    for (const info of data.data) {
      let id = info["id"];
      let title = info["title"];
      let year = info["year"];
      let directors = info["directors"];
      console.log(directors);
      let li = document.createElement("li");
      let div1 = document.createElement("div");
      let div2 = document.createElement("div");
      let div3 = document.createElement("div");
      let img = document.createElement("img");
      let a1 = document.createElement("a");
      let a2 = document.createElement("a");
      let p = document.createElement("p");
      img.src = `https://dwn6ych98b9pm.cloudfront.net/moviePos/img${id}.jpg`;
      a1.href = `/film/${id}`;
      a2.href = `/film/${year}`;
      a1.textContent = title + " ";
      a2.textContent = year;
      p.textContent = "Directed by ";
      div1.append(img);
      div2.append(a1);
      div2.append(a2);
      div2.append(p);
      div3.append(div1);
      div3.append(div2);
      div3.classList.add("showRow");
      div3.classList.add("flex");
      makeAlinkAndAppend(p, "/director?director=", directors);
      li.append(div3);
      showPlace.append(li);
    }
  }
  makePageTags("search?keyword", userInputAndPage, data["totalPages"]);
}

getMovieByDirector();
