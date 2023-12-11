function autocomplete(inp, arr) {
  var currentFocus;

  inp.addEventListener("input", debounce(function (e) {
      closeAllLists();
      if (!this.value) {
          return false;
      }
      currentFocus = -1;

      var suggestionList = document.createElement("DIV");
      suggestionList.setAttribute("id", this.id + "autocomplete-list");
      suggestionList.setAttribute("class", "autocomplete-items");
      this.parentNode.appendChild(suggestionList);

      // Use jQuery to make an asynchronous request to the server
      $.get("/autocomplete", { partial_name: this.value }, function (data) {
          // Parse the JSON response from the server
          var suggestions = data;

          for (var i = 0; i < suggestions.length; i++) {
              var suggestion = suggestions[i];
              var suggestionItem = document.createElement("DIV");
              suggestionItem.innerHTML = "<strong>" + suggestion.substr(0, inp.value.length) + "</strong>";
              suggestionItem.innerHTML += suggestion.substr(inp.value.length);
              suggestionItem.innerHTML += "<input type='hidden' value='" + suggestion + "'>";
              suggestionItem.addEventListener("click", function (e) {
                  inp.value = this.getElementsByTagName("input")[0].value;
                  closeAllLists();
              });
              suggestionList.appendChild(suggestionItem);
          }
      });
  }, 300));

  inp.addEventListener("keydown", function (e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
          currentFocus++;
          addActive(x);
      } else if (e.keyCode == 38) {
          currentFocus--;
          addActive(x);
      } else if (e.keyCode == 13) {
          e.preventDefault();
          if (currentFocus > -1) {
              if (x) x[currentFocus].click();
          }
      }
  });

  function addActive(x) {
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = (x.length - 1);
      x[currentFocus].classList.add("autocomplete-active");
  }

  function removeActive(x) {
      for (var i = 0; i < x.length; i++) {
          x[i].classList.remove("autocomplete-active");
      }
  }

  function closeAllLists(elmnt) {
      var x = document.getElementsByClassName("autocomplete-items");
      for (var i = 0; i < x.length; i++) {
          if (elmnt != x[i] && elmnt != inp) {
              x[i].parentNode.removeChild(x[i]);
          }
      }
  }

  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}
function debounce(func, delay) {
  let timeoutId;
  return function () {
    const context = this;
    const args = arguments;
    clearTimeout(timeoutId);
    timeoutId = setTimeout(function () {
      func.apply(context, args);
    }, delay);
  }
}
