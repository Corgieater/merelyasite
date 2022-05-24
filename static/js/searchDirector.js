"use strict";
let frame = document.querySelector(".frame");
// colletions
let movieCollectionsBt = document.querySelector(
  ".searchCollections > a:nth-child(1)"
);
let reviewsCollectionsBt = document.querySelector(
  ".searchCollections > a:nth-child(2)"
);
let directorsCollectionsBt = document.querySelector(
  ".searchCollections > a:nth-child(3)"
);
let actorsCollectionsBt = document.querySelector(
  ".searchCollections > a:nth-child(4)"
);
let keyword = cutUserInputInMiddle("d=", "&");
movieCollectionsBt.href = `/search?keyword=${keyword}&page=1`;
reviewsCollectionsBt.href = `/review?${keyword}&page=1`;
// review要考慮show什麼
directorsCollectionsBt.href = `/search/director?director=${keyword}&page=1`;
actorsCollectionsBt.href = `/actor?actor=${keyword}&page=1`;

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
  let req = await fetch(`/api/search/director?director=${userInputAndPage}`);
  console.log(`/api/search/director?director=${userInputAndPage}`);
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
  if (typeof data === "string") {
    makeMessage(frame, data);
  } else {
    let showPlace = document.querySelector(".frame > ul");
    data = data[0]["data"];

    //   use for of for async func
    for (const info of data.data) {
      console.log(info);
      let id = info["directorId"];
      let directorName = info["directorName"];
      let noSpaceName = directorName.replaceAll(" ", "+");
      let totalMoiesCount = info["directorMovieCount"];
      let li = document.createElement("li");
      let div1 = document.createElement("div");
      let div2 = document.createElement("div");
      let div3 = document.createElement("div");
      let img = document.createElement("img");
      let a1 = document.createElement("a");
      let p = document.createElement("p");
      img.src = `../static/images/film.svg`;
      a1.href = `/director?director=${noSpaceName}&page=1`;
      a1.textContent = directorName + " ";
      p.textContent = `Director of ${totalMoiesCount} movies`;
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
  makePageTags("search?keyword", userInputAndPage, data["totalPages"]);
}

// 小功能

renderDataInfo();