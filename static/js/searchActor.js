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

let keyword = cutUserInputInMiddle("r=", "&");

movieCollectionsBt.href = `/search?keyword=${keyword}&page=1`;
reviewsCollectionsBt.href = `/review?${keyword}&page=1`;
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
  let userInputAndPage = cutUserInputAtLast("r=");
  console.log(userInputAndPage);
  let req = await fetch(`/api/search/actor?actor=${userInputAndPage}`);
  console.log(`/api/search/actor?actor=${userInputAndPage}`);
  const res = await req.json();
  if (res.data) {
    return [res, userInputAndPage];
  } else {
    return res.message;
  }
}

async function makeShowRow(data, userInputAndPage) {
  // 沒東西就不用做了
  console.log(data);
  makePageTags("search/actor?actor=", userInputAndPage, data[0]["totalPages"]);
  if (typeof data === "string") {
    makeMessage(frame, data);
  } else {
    let showPlace = document.querySelector(".showPlace");
    data = data[0]["data"];

    //   use for of for async func
    for (const info of data.data) {
      console.log(info);
      let id = info["actorId"];
      let actorName = info["actorName"];
      let noSpaceName = actorName.replaceAll(" ", "+");
      let totalMoiesCount = info["actorMovieCount"];
      let li = document.createElement("li");
      let div1 = document.createElement("div");
      let div2 = document.createElement("div");
      let div3 = document.createElement("div");
      let img = document.createElement("img");
      let a1 = document.createElement("a");
      let p = document.createElement("p");
      img.src = `../static/images/actor.svg`;
      a1.href = `/actor?actor=${noSpaceName}&page=1`;
      a1.textContent = actorName + " ";

      if (totalMoiesCount === 1) {
        p.textContent = `Star of 1 movie`;
      } else {
        p.textContent = `Star of ${totalMoiesCount} movies`;
      }

      div1.append(img);
      div2.append(a1);
      div2.append(p);
      div3.append(div1);
      div3.append(div2);
      div3.classList.add("showRow");
      div3.classList.add("flex");
      li.append(div3);
      showPlace.append(li);
    }
  }
}

// 小功能

renderDataInfo();
