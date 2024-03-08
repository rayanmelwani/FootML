function filterSearch() {
  // Declare variables
  var input, filter, list, butt, a, i, txtValue;
  input = document.getElementById('input_name');
  filter = input.value.toUpperCase();
  list = document.getElementById("player_list");
  butt = list.getElementsByTagName('button');

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < butt.length; i++) {
    a = butt[i];
    txtValue = a.textContent || a.innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      butt[i].style.display = "";
    } else {
      butt[i].style.display = "none";
    }
  }
}
