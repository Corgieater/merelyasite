let director = cutUserInput("r/");
let posterPlace = document.querySelector(".posterPlace");

async function makePosterLi(idList) {
  for (let id of idList) {
    let li = document.createElement("li");
    let img = document.createElement("img");
    let aLink = document.createElement("a");
    aLink.href = `/film/${id}`;
    aLink.append(img);
    img.src = `https://d4u16azcwb6ha.cloudfront.net/posters/img${id}.jpg`;
    li.append(aLink);
    posterPlace.append(li);
  }
}
async function getMovieByDirector() {
  let req = await fetch(`/api/director/${director}`);
  let res = await req.json();
  let idList = await res["data"]["id_list"];
  makePosterLi(idList);
}
getMovieByDirector();
