// main.js

function addPredefinedStatsCheckboxes() {
    var predefinedStats = [
        "Games Played", "Games Started", "Minutes", "Field Goals Made", "Field Goals Attempted", "3pt Made", "3pt Attempted"
, "3pt%", "Free Throws Made", "Free Throws Attempted", "Offensive Rebounds", "Defensive Rebounds", "Rebounds", "Assists"
, "Steals", "Blocks", "Turnovers", "Personal Fouls", "Points"
    ];

    var container = document.getElementById("checkboxContainer");

    for (var i = 0; i < predefinedStats.length; i++) {
        var checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.name = "stats[]";
        checkbox.value = predefinedStats[i];

        var label = document.createElement("label");
        label.innerHTML = predefinedStats[i];

        container.appendChild(checkbox);
        container.appendChild(label);
        container.appendChild(document.createElement("br"));
    }

    // Add event listener to the form to check if at least one checkbox is checked
    var form = document.querySelector('form');
    form.addEventListener('submit', function (event) {
        var checkboxes = document.querySelectorAll('input[name="stats[]"]:checked');
        if (checkboxes.length === 0) {
            alert("Select at least one stat.");
            event.preventDefault(); // Prevent form submission
        }
    });
}
