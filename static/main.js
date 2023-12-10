// main.js

function addPredefinedStatsCheckboxes() {
    var predefinedStats = [
        "GP", "GS", "MIN", "FGM", "FGA", "FG_PCT", "FG3M", "FG3A", "FG3_PCT",
        "FTM", "FTA", "FT_PCT", "OREB", "DREB", "REB", "AST", "STL", "BLK",
        "TOV", "PF", "PTS"
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
}
