let team_map = {"Arsenal": "Arsenal",
            "Aston Villa": "Aston Villa",
            "Brentford": "Brentford",
            "Brighton": "Brighton",
            "Burnley": "Burnley",
            "Chelsea": "Chelsea",
            "Crystal Palace": "Crystal Palace",
            "Everton": "Everton",
            "Leeds": "Leeds",
            "Leicester": "Leicester",
            "Liverpool": "Liverpool",
            "Man City": "Manchester City",
            "Man Utd": "Manchester United",
            "Newcastle": "Newcastle",
            "Norwich": "Norwich",
            "Southampton": "Southampton",
            "Spurs": "Tottenham",
            "Watford": "Watford",
            "West Ham": "West Ham",
            "Wolves": "Wolverhampton"
            };

let current_players = [];
  //load players stored from previous session
  stored_players = JSON.parse(localStorage.getItem("current_players"))
  if (stored_players) {
    for(i = 0; i < stored_players.length; i++) {
      current_players.push(stored_players[i]);
    }
    
  }

  for (i = 0; i < current_players.length; i++) {
    //create html element corresponding to player
    //for each player stored in browser localStorage
    //element functions as a button which displays the player information
    role = current_players[i].element_type;
    name = current_players[i].Name;
    value = current_players[i].now_cost;
    team = current_players[i].Team;

    var img = new Image();
    img.src = "static/img/" + team_map[team].replace(/ /g, "").toLowerCase() + ".webp";
    var span = document.createElement("span");
    span.className = "shirtSpan";
    var remove = document.createElement("span");
    //create a remove button which removes the player from the current
    //selected team and add it to the element corresponding to the player
    remove.className = "remove_player";
    remove.addEventListener("click", removePlayerEv);
    remove.param = name;
    remove.innerHTML += "&times";
    var playerButton = document.createElement("div");
    playerButton.id = name;
    playerButton.className = "team_selection_button";
    playerButton.addEventListener("click", displayInfoEv);
    playerButton.param = name;
    span.appendChild(img);
    playerButton.appendChild(span);
    playerButton.innerHTML += team + " • " + name + " • £" + value;
    playerButton.appendChild(remove);

    document.getElementById(role).appendChild(playerButton);
    //update player counter and budget
    document.getElementById("counter").innerHTML = "Players Selected &#10142;" + current_players.length +  "/15";
    document.getElementById("budget").innerHTML = "Current Team Value &#10142;" + teamValue();
  

    //remove stored players from search bar on right
    name_copy = name
    name_copy = name_copy.replace(/\s/g, "");
    name_copy = name_copy.replace(/-/g, "");
    document.getElementById(name_copy).remove();
  }
  
  

  function submitTeam () {
    //send current player data to session storage so that it can be accessed
    //on other pages of our app
    localStorage.setItem("current_players", JSON.stringify(current_players));
    localStorage.setItem("extra_funds", document.getElementById('funds').value);
  }

  //function that calculates the team value
  function teamValue() {
    count = 0;
    for(index=0; index<current_players.length;index++){
      count += (parseFloat(current_players[index].now_cost));
    }
    return count.toFixed(1);
  }

  function submitPlayer (name) {
    //submit player to server to check whether addition to team is valid
      new_player = name;

      //data to be sent to server for checks
      postage = {
          "current_players": current_players,
          "new_player": new_player,
      };

      temp_team = current_players.slice(0)

      // send the player and the current team to the server to check for validity
      fetch('/json', {
          method: 'POST',
          credentials: 'include',
          body: JSON.stringify(postage),
          cache: "no-cache",
          headers: new Headers({
              "content-type": "application/json"
          })
      })
      .then(function (response) {
        response.json().then(function (data) {
          //handle the json data returned by the response
          //if team length has changed while server fetch was processing,
          //then the player is not added (stops double adding of players)
          if (data.message == "success" && temp_team.length === current_players.length) {
              name = name.replace(/\s/g, "");
              name = name.replace(/-/g, "");
              document.getElementById(name).remove();

              var obj = data.new_player;
              current_players.push(obj);
              //add players to localStorage
              localStorage.setItem("current_players", JSON.stringify(current_players));
              role = obj.element_type;
              name = obj.Name;
              value = obj.now_cost;
              team = obj.Team;

              var img = new Image();
              img.src = "static/img/" + team_map[team].replace(/ /g, "").toLowerCase() + ".webp";
              var span = document.createElement("span");
              span.className = "shirtSpan";
              var remove = document.createElement("span");
              remove.className = "remove_player";
              remove.addEventListener("click", removePlayerEv);
              remove.param = name;
              remove.innerHTML += "&times";
              var playerButton = document.createElement("div");
              playerButton.id = name;
              playerButton.className = "team_selection_button";
              playerButton.addEventListener("click", displayInfoEv);
              playerButton.param = name;
              span.appendChild(img);
              playerButton.appendChild(span);
              playerButton.innerHTML += team + " • " + name + " • £" + value;
              playerButton.appendChild(remove);
              
              document.getElementById(role).appendChild(playerButton);
              document.getElementById("counter").innerHTML = "Players Selected &#10142;" + current_players.length +  "/15";
              document.getElementById("budget").innerHTML = "Current Team Value &#10142;" + teamValue();
          }
          else if(data.message == "failure_alreadyinteam"){
            alert('Could not add player - already in team!');
          }
          else if(data.message == "failure_playerdoesnotexist"){
            alert('Could not add player - player does not exist!');
          }
          else if(data.message == "failure_maxplayersperclub"){
            alert('Could not add player - cannot have more than 3 players from the same club!');
          }
          else if(data.message == "failure_maxrolesperteam"){
            alert('Could not add player - cannot have more than 2 GKs, 5 DEFs, 5 MIDs and 3 FWDs!');
          }
          else{
            alert('Could not add player!')
          }
        })
      })
  }
    //function that allows us to remove players from the current_players list
  function removePlayerEv(evt) {
    name = evt.target.param
    document.getElementById(name).remove();
    for(index=0; index<current_players.length;index++){
      if(name === current_players[index].Name){
        name_copy = name.replace(/\s/g, ""); //replace whitespace in name
        name_copy = name_copy.replace(/-/g, ""); //replace hyphens in name
        //add player back to player list on right
        document.getElementById("player_display").innerHTML += "<button id=\"" + name_copy + "\" onclick='submitPlayer(\"" + name_copy + "\");' type=\"button\" value=\"" + name + "\"> " + name + "</button>"
        
        current_players.splice(index,1);
        localStorage.setItem("current_players", JSON.stringify(current_players));
        break;
      }
    }
    document.getElementById("counter").innerHTML = "Players Selected &#10142;" + current_players.length +  "/15";
    document.getElementById("budget").innerHTML = "Current Team Value &#10142; " + teamValue();

}
