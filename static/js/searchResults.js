"use strict";
let frame = document.querySelector(".frame");
// other colletions
let movieCollectionsBt = document.querySelector(
  ".otherCollections > li:nth-child(2) > a"
);
let reviewsCollectionsBt = document.querySelector(
  ".otherCollections > li:nth-child(3) > a"
);
let directorsCollectionsBt = document.querySelector(
  ".otherCollections > li:nth-child(4) > a"
);
let actorsCollectionsBt = document.querySelector(
  ".otherCollections > li:nth-child(5) > a"
);

let keyword = cutUserInputInMiddle("d=", "&");
movieCollectionsBt.href = `/search?keyword=${keyword}&page=1`;
reviewsCollectionsBt.href = `/search/reviews?reviews=${keyword}&page=1`;
// review要考慮show什麼
directorsCollectionsBt.href = `/search/director?director=${keyword}&page=1`;
actorsCollectionsBt.href = `/search/actor?actor=${keyword}&page=1`;

// 做資料
async function renderDataInfo() {
  let data = await getData();
  let userInput = data[1];
  makeShowRow(data, userInput);
}

// 先打API去要資料 多頁用
async function getData() {
  let userInputAndPage = cutUserInputAtLast("d=");
  let req = await fetch(`/api/search?keyword=${userInputAndPage}`);
  const res = await req.json();
  if (res.data) {
    return [res, userInputAndPage];
  } else {
    return res.message;
  }
}

async function makeShowRow(data, userInputAndPage) {
  // 沒東西就不用做了
  if (typeof data === "string") {
    makeMessage(frame, data);
  } else {
    let showPlace = document.querySelector(".showPlace");
    data = data[0];

    //   use for of for async func
    for (const info of data.data) {
      let id = info["id"];
      let title = info["title"];
      let year = info["year"];
      let directors = info["directors"];
      let li = document.createElement("li");
      let div1 = document.createElement("div");
      let div2 = document.createElement("div");
      let div3 = document.createElement("div");
      let img = document.createElement("img");
      let a1 = document.createElement("a");
      let p1 = document.createElement("p");
      let p2 = document.createElement("a");

      img.src = `https://dwn6ych98b9pm.cloudfront.net/moviePos/img${id}.jpg`;
      img.classList.add("moviePos");
      a1.href = `/film/${id}`;
      a1.textContent = title + " ";
      p2.textContent = year;
      p1.textContent = "Directed by ";
      div1.append(img);
      div2.append(a1);
      div2.append(p2);
      div2.append(p1);
      div3.append(div1);
      div3.append(div2);
      div3.classList.add("showRow");
      div3.classList.add("flex");
      makeAlinkAndAppend(p1, "/director?director=", directors);
      li.append(div3);
      showPlace.append(li);
    }
  }
  makePageTags("search?keyword=", userInputAndPage, data["totalPages"]);
}

renderDataInfo();
