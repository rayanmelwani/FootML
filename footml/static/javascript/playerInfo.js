// Get the modal
var playerInfo = document.getElementById("player-info");
var infoContent = document.getElementById("player-info-content")

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal with correct player info
function displayInfoEv(evt) {
    //don't display the player info if the user clicks on the remove_player button
    if (evt.target.className === "remove_player") {
        return;
    }
    console.log("bye there");
  text = {"name": evt.target.param};
  //fetch player information from server
  fetch('/player-info', {
      method: 'POST',
      credentials: 'include',
      body: JSON.stringify(text),
      cache: "no-cache",
      headers: new Headers({
          "content-type": "application/json"
      })
  }).then(function (response) {
      response.json().then(function (data) {
      info = data.info
      playerName = info.name
      team = info.team
      role = info.role
      cost = info.cost
      points = info.points
      schedule = info.schedule
      gameweek = data.gameweek

        //display player info in a table
      infoContent.innerHTML = "<table> <th>Name</th> <th>Team</th> <th>Role</th> <th>Cost</th> <th>Predicted Points GW " + gameweek + "</th> <tr>" + "<td>" + playerName + "</td>" + "<td>" + "<img class='imageTeamLogo' src='static/img/" + team_map[team].replace(/ /g, "").toLowerCase() + "logo.png'></img>" + team + "</td>" + "<td>" + role + "</td>" + "<td>" + cost + "</td><td>" + points + "</td>" + "</tr></table>" + "<table> <th><br>Schedule<br><br></th>" + schedule + "</table>";
      playerInfo.style.display = "block";
  })})
}

window.onclick = function(event) {
  if (event.target == playerInfo) {
    playerInfo.style.display = "none";
  }
}