"use strict";
let userInputPlace = document.querySelector("#userInput");

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
let usersCollectionsBt = document.querySelector(
  ".otherCollections > li:nth-child(6) > a"
);

let keyword = cutUserInputInMiddle("r=", "%");

movieCollectionsBt.href = `/search?keyword=${keyword}&page=1`;
reviewsCollectionsBt.href = `/search/reviews?reviews=${keyword}&page=1`;
directorsCollectionsBt.href = `/search/director?director=${keyword}&page=1`;
actorsCollectionsBt.href = `/search/actor?actor=${keyword}&page=1`;
usersCollectionsBt.href = ``;

// 做資料
async function renderDataInfo() {
  let data = await getData();
  let userInput = data[1];
  makeShowRow(data, userInput);
}

// 先打API去要資料 多頁用
async function getData() {
  let userInputAndPage = cutUserInputAtLast("r=");
  let req = await fetch(`/api/search/users?user=${userInputAndPage}`);
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
    data = data[0].data;

    //   use for of for async func
    for (const info of data.data) {
      let searchedUserName = info["userName"];
      let searchedUserFollowingNum = info["followingNum"];
      let searchedUserFollowerNum = info["followerNum"];
      let noSpaceName = searchedUserName.replaceAll(" ", "+");
      let li = document.createElement("li");
      let div1 = document.createElement("div");
      let div2 = document.createElement("div");
      let div3 = document.createElement("div");
      let img = document.createElement("img");
      let a1 = document.createElement("a");
      let a2 = document.createElement("a");
      let a3 = document.createElement("a");
      let section = document.createElement("section");
      let userImage = info["userImageId"];
      if (userImage === null) {
        userImage = "../static/images/user.png";
      } else {
        userImage = `https://dwn6ych98b9pm.cloudfront.net/userPic/${userImage}.jpg`;
      }
      img.src = userImage;
      img.classList.add("userImg");
      a1.href = `/user_profile/${noSpaceName}`;
      a1.textContent = searchedUserName + " ";
      if (searchedUserFollowingNum === null) {
        searchedUserFollowingNum = 0;
      }
      if (searchedUserFollowerNum === null) {
        searchedUserFollowerNum = 0;
      }
      a2.textContent = `${searchedUserFollowingNum} following`;
      a3.textContent = `${searchedUserFollowerNum} followers`;
      a2.href = "#";
      a3.href = "#";

      div1.append(img);
      div2.append(a1);
      section.append(a2);
      section.append(a3);
      div2.append(section);
      div3.append(div1);
      div3.append(div2);
      div3.classList.add("showRow");
      div3.classList.add("flex");
      li.append(div3);
      showPlace.append(li);
    }
  }
  makePageTags("search/genre?genre=", userInputAndPage, data["totalPages"]);
}

// 小功能

renderDataInfo();
