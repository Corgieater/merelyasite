const signInBt = document.querySelector("#signInBt");
const upComingArea = document.querySelector("#upComingArea");

signInBt.addEventListener("click", function () {
  let signInArea = document.querySelector("#signInArea");
  signInArea.classList.toggle("collapse");
});

async function getUpComing() {
  let req = await fetch(
    "https://api.themoviedb.org/3/movie/upcoming?api_key=679b8029d0a53b6dfc099b3509278a55",
    {
      method: "GET",
    }
  );
  let res = await req.json();
  console.log(res);
}
getUpComing();
