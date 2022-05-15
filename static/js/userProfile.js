const userName = cutUserInput("e/");

async function getLatestFiveReviews() {
  const req = await fetch(`/api/get_latest_reviews/${userName}`);
  const res = await req.json();
  console.log(res);
}

async function redirectIfNotLogin() {
  const userLoged = await checkIfLogged();
  if (!userLoged) {
    window.location.replace("/");
  }
}

getLatestFiveReviews();
redirectIfNotLogin();
