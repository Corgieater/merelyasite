"use strict";
const upLoadBt = document.querySelector(".uploadBt");
let phtoFile = document.querySelector("#phtoFile");
let picPlace = document.querySelector(".picPlace");

upLoadBt.addEventListener("click", async function (e) {
  e.preventDefault();
  let userData = await getUserData();
  let userName = userData["userName"];
  show(mask);
  show(loaderPlace);
  const photoForm = new FormData(document.querySelector("#photoForm"));
  let req = await fetch(`/api/user/${currentUserId}/upload_pic`, {
    method: "PATCH",
    body: photoForm,
  });
  let res = await req.json();
  if (res.ok) {
    makeMessage(globalMessagePlace, "User picture updated");
    window.location.replace(`/user_profile/${userName.replaceAll(" ", "+")}`);
  } else {
    makeMessage(globalMessagePlace, res.message);
  }
});

// 預覽圖
phtoFile.onchange = (e) => {
  const [file] = phtoFile.files;
  show(picPlace);
  if (file) {
    picPlace.src = URL.createObjectURL(file);
  }
};
