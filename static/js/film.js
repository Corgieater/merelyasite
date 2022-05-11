"use strict";
let poster = document.querySelector(".posterPlace > img");
let title = document.querySelector(".headArea :nth-child(1)");
let year = document.querySelector(".headArea >:nth-child(2)");
let directors = document.querySelector(".headArea :nth-child(4)");
let plot = document.querySelector(".plot > p");
let casts = document.querySelector(".casts");
let genres = document.querySelector(".genres");

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
