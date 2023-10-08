function validateNumberInput(input) {
    // Remove any non-numeric characters, including "e"
    input.value = input.value.replace(/[^0-9.]/g, '');
  }

function validateTextInput(input) {
    // Remove any commas as this will affect listing in python
    input.value = input.value.replace(/[,_]/g, '');
  }


// Get all the <h2> elements with the class name 'recipe__title'
var recipetitle = document.querySelectorAll('h2.recipe__title');

// Define the function to be applied to each <h2> element
function ValidRepipeTitle(element) {
    // Modify the element as needed
    // For example, to remove any commas
    element.textContent = element.textContent.replace(/[0-9.,_]/g, '');
}

// Iterate through the selected <h2> elements and apply the function
for (var i = 0; i < recipetitle.length; i++) {
  ValidRepipeTitle(recipetitle[i]);
}