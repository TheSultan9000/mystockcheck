// Get all elements with the class '.recipe__container'
var selectionElements = document.querySelectorAll('.recipe__container');

// Initialize an array to store selected items
var selectedItems = [];

// Add the click event listener to all '.recipe__container' elements
selectionElements.forEach(function (element) {
    element.addEventListener('click', handleContainerClick);
});

// Create an event listener function
function handleContainerClick(event) {
    var clickedContainer = findParentContainer(event.target, 'recipe__container');

    if (clickedContainer) {
        // Check if the clicked element has the 'clicked' class
        if (clickedContainer.classList.contains('clicked')) {
            // Extract the entire content of the container
            var containerContent = clickedContainer.textContent;

            // Add the selection data to the array
            selectedItems.push(containerContent);
        } else {
            // Extract the entire content of the container
            var containerContent = clickedContainer.textContent;

            // Find the index of the containerContent in the selectedItems array
            var removeIndex = selectedItems.indexOf(containerContent);

            // Check if the value exists in the array before removing
            if (removeIndex !== -1) {
                selectedItems.splice(removeIndex, 1);
            }
        }

        // Call sendSelectedItems() whenever a .recipe__container is clicked
        sendSelectedItems();
    }
}

// Function to find the nearest ancestor with a specific class
function findParentContainer(element, className) {
    while (element && !element.classList.contains(className)) {
        element = element.parentNode;
    }
    return element;
}

// Function to send selected items in a POST request
function sendSelectedItems() {
    var formData = new FormData();
    formData.append('selectedItems', JSON.stringify(selectedItems));

    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const data_formatted = {
            ingredients_type: data.ingredients_type.join(","),
            ingredients: data.ingredients.join(","),
            quantities: data.quantities.join(","),
            units: data.units.join(","),
            };
            
        // Split the comma-separated strings into arrays
        const ingredients_type = data_formatted.ingredients_type.split(",");
        const ingredients = data_formatted.ingredients.split(",");
        const quantities = data_formatted.quantities.split(",");
        const units = data_formatted.units.split(",");
        
        // Create an array containing the individual items
        const dataArray = [];
        for (let i = 0; i < ingredients.length; i++) {
        dataArray.push({
            ingredients_type: ingredients_type[i],
            ingredient: ingredients[i],
            quantity: quantities[i],
            unit: units[i],
        });
        }

        // Sort dataArray by ingredient type
        dataArray.sort((a, b) => a.ingredients_type.localeCompare(b.ingredients_type));
        
        // Create a table element
        const table = document.createElement("table");
        
        // Create the table header
        const thead = table.createTHead();
        const headerRow = thead.insertRow(0);
        
        // Create table header cells
        const headerCells = ["Type", "Ingredients", "Quantities", "Units"];
        headerCells.forEach((headerText) => {
        const th = document.createElement("th");
        th.textContent = headerText;
        headerRow.appendChild(th);
        });
        
        // Create the table body and rows
        const tbody = table.createTBody();
        dataArray.forEach((item) => {
        const row = tbody.insertRow();
        const typeCell = row.insertCell(0);
        const ingredientCell = row.insertCell(1);
        const quantityCell = row.insertCell(2);
        const unitCell = row.insertCell(3);
        
        typeCell.textContent = item.ingredients_type;
        ingredientCell.textContent = item.ingredient;
        quantityCell.textContent = item.quantity;
        unitCell.textContent = item.unit;
        });
        
        // Get the tableContainer element
        const tableContainer = document.getElementById("table__container");

        // Replace the existing table with the new one
        tableContainer.innerHTML = "";
        tableContainer.appendChild(table);
      })
    .catch(error => {
        console.error('Error:', error);
    });
}

