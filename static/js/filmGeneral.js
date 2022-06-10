// 做spoiler alert
function makeSpoilersAlert(placeNeedToAntiSpoilers, review) {
  let alert = document.createElement("p");
  alert.textContent = "There are spoilers in this review!";
  alert.classList.add("spoilerAlertText");
  let spoilerAlert = document.createElement("a");
  spoilerAlert.textContent = "I don't mind, let me read.";
  spoilerAlert.classList.add("spoilerAlert");

  spoilerAlert.href = "#";
  placeNeedToAntiSpoilers.append(alert);
  placeNeedToAntiSpoilers.append(spoilerAlert);
  spoilerAlert.addEventListener("click", function (e) {
    e.preventDefault();
    hide(alert);
    hide(spoilerAlert);
    placeNeedToAntiSpoilers.textContent = review;
  });
}

// watchlist functions 填入動作以及api地址
// 給右邊的watchlist和Like rate用
async function smallActionFunc(action, api) {
  let userData = await getUserData();
  let userId = userData["userId"];
  let data = {
    movieId: movieId,
    userId: userId,
  };
  let watchlistAction = await sendDataToBackend(action, data, api);
  if (watchlistAction === true) {
    window.location.reload();
  }
}

function rateToStars(rate) {
  switch (rate) {
    case "0.5": {
      let star = document.querySelector("#rating1");
      star.checked = true;
      break;
    }
    case "1.0": {
      let star = document.querySelector("#rating2");
      star.checked = true;
      break;
    }
    case "1.5": {
      let star = document.querySelector("#rating3");
      star.checked = true;
      break;
    }
    case "2.0": {
      let star = document.querySelector("#rating4");
      star.checked = true;
      break;
    }
    case "2.5": {
      let star = document.querySelector("#rating5");
      star.checked = true;
      break;
    }
    case "3.0": {
      let star = document.querySelector("#rating6");
      star.checked = true;
      break;
    }
    case "3.5": {
      let star = document.querySelector("#rating7");
      star.checked = true;
      break;
    }
    case "4.0": {
      let star = document.querySelector("#rating8");
      star.checked = true;
      break;
    }
    case "4.5": {
      let star = document.querySelector("#rating9");
      star.checked = true;
      break;
    }
    case "5.0": {
      let star = document.querySelector("#rating10");
      star.checked = true;
      break;
    }
    default:
      break;
  }
}
