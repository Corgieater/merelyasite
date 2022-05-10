let frame = document.querySelector(".frame");

async function getData() {
  let webHref = window.location.href;
  let userInput = webHref.slice(29);
  let req = await fetch(`/api/search/${userInput}`);
  const res = await req.json();
  if (res.data) {
    return res;
  } else {
    return res.message;
  }
}

async function makeShowRow() {
  let data = await getData();
  if (typeof data === "string") {
    makeMessage(frame, data);
  } else {
    let showPlace = document.querySelector(".frame > ul");
    data = data.data;

    //   use for of for async func
    for (const info of data) {
      console.log(info);
      let id = info["id"];
      let title = info["title"];
      let hrefTitle = title.split(" ").join("-");
      let year = info["year"];
      let directors = info["directors"];
      let li = document.createElement("li");
      let div1 = document.createElement("div");
      let div2 = document.createElement("div");
      let div3 = document.createElement("div");
      let img = document.createElement("img");
      let a1 = document.createElement("a");
      let a2 = document.createElement("a");
      let p = document.createElement("p");
      img.src = `https://d4u16azcwb6ha.cloudfront.net/img${id}.jpg`;
      a1.href = `/film/${hrefTitle}`;
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
      for (let director of directors) {
        let hrefDirector = director.replace(" ", "-");
        let a = document.createElement("a");
        a.href = `/director/${hrefDirector}`;
        a.textContent = director;
        p.append(a);
      }
      li.append(div3);
      showPlace.append(li);
    }
  }
}

makeShowRow();
