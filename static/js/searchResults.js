let frame = document.querySelector(".frame");
let pagesPlace = document.querySelector(".pagesPlace");

// 做資料
async function renderDataInfo() {
  let data = await getData();
  let userInput = data[1];
  makeShowRow(data, userInput);
}

// 先打API去要資料
async function getData() {
  let userInputAndPage = cutUserInput("d=");
  console.log(userInputAndPage);
  let req = await fetch(`/api/search?keyword=${userInputAndPage}`);
  console.log(`/api/search?keyword=${userInputAndPage}`);
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
      img.src = `https://d4u16azcwb6ha.cloudfront.net/posters/img${id}.jpg`;
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
      makeAlinkAndAppend(p, directors);
      li.append(div3);
      showPlace.append(li);
    }
  }
  makePageTags(userInputAndPage, data["totalPages"]);
}

// 小功能
// 做頁碼
async function makePageTags(userInputAndPage, totalPages) {
  console.log("usrinpiut", userInputAndPage);
  // 這裡的問題 改一下
  for (let i = 0; i < totalPages; i++) {
    // 找出要切哪
    let sliceIndex = userInputAndPage.indexOf("e=");
    console.log("slice Index", sliceIndex);
    // 切到底拿到除了page以外的querystring
    let querystringWithoutPage = userInputAndPage.slice(0, sliceIndex + 2);
    let a = document.createElement("a");
    a.href = `/search?keyword=${querystringWithoutPage}${i + 1}`;
    a.textContent = i + 1;
    pagesPlace.append(a);
  }
}

renderDataInfo();
