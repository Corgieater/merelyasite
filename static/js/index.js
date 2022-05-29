"use strict";
// 查詢用

async function getData() {
  let req = await fetch(`/api/user/follows/reviews`);
  const res = await req.json();
  console.log(res);
  if (res.data) {
    return res;
  } else {
    return res.message;
  }
}

getData();
