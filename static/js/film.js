"use strict";
// 頁面區
let poster = document.querySelector(".posterPlace > img");
let title = document.querySelector(".headArea > section :nth-child(1)");
let year = document.querySelector(".headArea > section :nth-child(2)");
let directors = document.querySelector(".headArea > section :nth-child(4)");
let plot = document.querySelector(".plot > p");
let casts = document.querySelector(".casts");
let genres = document.querySelector(".genres");

// action區
let rateBts = document.querySelectorAll("input[type='radio']");
let cancel = document.querySelector(".cancel");

// 隨著點按星星會輸出分數 記得寫進資料庫 要打API 用patch
rateBts.forEach((bt) => {
  bt.addEventListener("click", async function (e) {
    let rate = e.target.value;
    console.log(rate);
    let userId = userData["userId"];
    let movieId = cutUserInput("m/");
    let data = {
      rate: rate,
      userId: userId,
      movieId: movieId,
    };
    sendDataToBackend("PATCH", data, "/api/rate");
  });
});

cancel.addEventListener("click", function () {
  for (let bt of rateBts) {
    bt.checked = false;
    // 打API 用DELETE
  }
});

// review區
let reviewTitle = document.querySelector(
  ".reviewBox > section:nth-child(2) > h2"
);

async function getFilm() {
  const filmId = cutUserInput("m/");
  const req = await fetch(`/api/film/${filmId}`);
  const res = await req.json();
  return res;
}

async function showFilmInfo() {
  let data = await getFilm();
  console.log(data);
  let filmId = data["id"];
  let filmTitle = data["title"];
  reviewTitle.textContent = data["title"];
  let filmYear = data["year"];
  let filmDirectors = data["directors"];
  let filmPlot = data["plot"];
  let filmStars = data["stars"];
  let filmGenres = data["genres"];
  poster.src = `https://d4u16azcwb6ha.cloudfront.net/img${filmId}.jpg`;
  title.textContent = filmTitle;
  year.textContent = filmYear;
  plot.textContent = filmPlot;
  makeAlinkAndAppend(directors, filmDirectors);
  makeAlinkAndAppend(casts, filmStars);
  makeAlinkAndAppend(genres, filmGenres);
  //   for (let director of filmDirectors) {
  //     let hrefDirector = director.replace(" ", "-");
  //     let a = document.createElement("a");
  //     a.href = `/director/${hrefDirector}`;
  //     a.textContent = director;
  //     directors.append(a);
  //   }
}

showFilmInfo();
