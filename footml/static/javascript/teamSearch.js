
//map from informal team names to full team names
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

//list of teams to be displayed in the filter section
teamSearchList =    ['Arsenal',
                    'Aston Villa',
                    'Brentford',
                    'Brighton',
                    'Burnley',
                    'Chelsea',
                    'Crystal Palace',
                    'Everton',
                    'Leeds',
                    'Leicester',
                    'Liverpool',
                    'Manchester City',
                    'Manchester United',
                    'Newcastle',
                    'Norwich',
                    'Southampton',
                    'Tottenham',
                    'Watford',
                    'West Ham',
                    'Wolverhampton']


//teams that the user has excluded (items shared with teamSearchList)
var excludedTeams = []

//list of players in premier league (populated from fetch request below)
var playerList = [];


//load images only once
var arsenalshirt = new Image();
var astonvillashirt = new Image();
var brentfordshirt = new Image();
var brightonshirt = new Image();
var burnleyshirt = new Image();
var chelseashirt = new Image();
var crystalpalaceshirt = new Image();
var evertonshirt = new Image();
var leedsshirt = new Image();
var leicestershirt = new Image();
var liverpoolshirt = new Image();
var manchestercityshirt = new Image();
var manchesterunitedshirt = new Image();
var newcastleshirt = new Image();
var norwichshirt = new Image();
var southamptonshirt = new Image();
var tottenhamshirt = new Image();
var watfordshirt = new Image();
var westhamshirt = new Image();
var wolverhamptonshirt = new Image();

arsenalshirt.src = '/static/img/arsenal.webp';
astonvillashirt.src = '/static/img/astonvilla.webp';
brentfordshirt.src = '/static/img/brentford.webp';
brightonshirt.src = '/static/img/brighton.webp';
burnleyshirt.src = '/static/img/burnley.webp';
chelseashirt.src = '/static/img/chelsea.webp';
crystalpalaceshirt.src = '/static/img/crystalpalace.webp';
evertonshirt.src = '/static/img/everton.webp';
leedsshirt.src = '/static/img/leeds.webp';
leicestershirt.src = '/static/img/leicester.webp';
liverpoolshirt.src = '/static/img/liverpool.webp';
manchestercityshirt.src = '/static/img/manchestercity.webp';
manchesterunitedshirt.src = '/static/img/manchesterunited.webp';
newcastleshirt.src = '/static/img/newcastle.webp';
norwichshirt.src = '/static/img/norwich.webp';
southamptonshirt.src = '/static/img/southampton.webp';
tottenhamshirt.src = '/static/img/tottenham.webp';
watfordshirt.src = '/static/img/watford.webp';
westhamshirt.src = '/static/img/westham.webp';
wolverhamptonshirt.src = '/static/img/wolverhampton.webp';



//populate player-search-list
fetch('/player-search-list', {
    method: 'POST',
    credentials: 'include',
    cache: "no-cache",
    headers: new Headers({
        "content-type": "application/json"
    })
})
.then(function (response) {
  response.json().then(function (data) {
      playerList = data
      for (i = 0; i < playerList.length; i++) {
        playerList[i].display = "";
        //create the ui elements corresponding to the player information
        let logoSpan = document.createElement("span");
        let shirtName = team_map[playerList[i].team].replace(/ /g, "").toLowerCase() + "shirt";
        logoSpan.className = "shirtSpan";
        logoSpan.appendChild(window[shirtName]);
        let playerDiv = document.createElement("div");
        playerDiv.id = playerList[i].elementName;
        playerDiv.className = "playerSearchListEntry";
        playerDiv.addEventListener('click', displayInfoEv);
        playerDiv.param = playerList[i].name;
        playerDiv.appendChild(logoSpan);
        playerDiv.innerHTML += playerList[i].name + " • " + playerList[i].team + " • " + playerList[i].role + " • £" + playerList[i].cost + " • " + playerList[i].points;

        
        document.getElementById("playerSearchList").appendChild(playerDiv); 

    }
    
})})

updateLists();

function advancedSearch() {
    // Declare variables
    var input, filter;

    input = document.getElementById('inputName');
    filter = input.value.toUpperCase(); //player name filter

    roleFilter = document.getElementById("roleFilter").value; //filter by role

    costFilter = parseFloat(document.getElementById("costFilter").value); //filter by cost
    if (isNaN(costFilter)) {
        costFilter = 100
    }

    // update whether player is displayed based on filter
    for (i = 0; i < playerList.length; i++) {
        //if a player violates any of the filters put in place by the user, set their 'display' attribute to none
        if (roleFilter != "None" || playerList[i].name.toUpperCase().indexOf(filter) === -1 || playerList[i].cost > costFilter || excludedTeams.indexOf(team_map[playerList[i].team]) !== -1) {
            if (playerList[i].role.indexOf(roleFilter) == -1 || playerList[i].elementName.toUpperCase().indexOf(filter) === -1 || playerList[i].cost > costFilter || excludedTeams.indexOf(team_map[playerList[i].team]) !== -1) {
                playerList[i].display = "none";
            }
            else {
                playerList[i].display="block";
            }
        }
        else {
            playerList[i].display = "block";
        }
    }
  
    // apply display settings based on display attribute of players
    for (i = 0; i < playerList.length; i++) {
        document.getElementById(playerList[i].elementName).style.display = playerList[i].display   
    }
  }


  //exclude players from a team from the search list when clicked by user
function excludeTeam(evt) {
    teamCode = evt.target.myParameter
    excludedTeams.push(teamCode);
    excludedTeams.sort();
    for (i = 0; i < teamSearchList.length ; i++) {
        if (teamSearchList[i] === teamCode) {
            teamSearchList.splice(i, 1);
        }
    }

    updateLists();
    advancedSearch();
}

//stop excluding players from specified team
function includeTeam(evt) {
    teamCode = evt.target.myParameter
    teamSearchList.push(teamCode);
    teamSearchList.sort();

    for (i = 0; i < excludedTeams.length ; i++) {
        if (excludedTeams[i] === teamCode) {
            excludedTeams.splice(i, 1);
        }
    }

    updateLists();
    advancedSearch();
}

//redraw included/excluded lists once updates have been made
function updateLists() {

    document.getElementById("teamSearchList").innerHTML = "";
    

    for (i = 0; i < teamSearchList.length; i++) {
        //create elements corresponding to each team
        let newDiv = document.createElement("div");
        newDiv.id = teamSearchList[i];
        newDiv.className = "teamSearchListButton";
        newDiv.addEventListener("click", excludeTeam);
        newDiv.myParameter = teamSearchList[i];

        let newSpan = document.createElement("span");
        newSpan.className = "teamLogo";

        let newImg = document.createElement("img");
        newImg.src = "static/img/" + teamSearchList[i].replace(/ /g, "").toLowerCase() + "logo.png";

        newSpan.appendChild(newImg);
        newDiv.appendChild(newSpan);
        newDiv.innerHTML += teamSearchList[i];

        document.getElementById("teamSearchList").appendChild(newDiv);
        
    }


    document.getElementById("excludedTeamList").innerHTML = "";

    for (i = 0; i < excludedTeams.length; i++) {
        //create elements corresponding to each team
        let newDiv = document.createElement("div");
        newDiv.id = excludedTeams[i] + "Excluded";
        newDiv.className = "teamSearchListButton";
        newDiv.addEventListener("click", includeTeam);
        newDiv.myParameter = excludedTeams[i];

        let newSpan = document.createElement("span");
        newSpan.className = "teamLogo";

        let newImg = document.createElement("img");
        newImg.src = "static/img/" + excludedTeams[i].replace(/ /g, "").toLowerCase() + "logo.png";
        newSpan.appendChild(newImg);
        newDiv.appendChild(newSpan);
        newDiv.innerHTML += excludedTeams[i];
        document.getElementById("excludedTeamList").appendChild(newDiv);
    }

}


