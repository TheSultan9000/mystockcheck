    // Using the DOMContentLoaded event is a common practice in web development to ensure that JavaScript code that interacts with the 
    // DOM is executed only after the DOM is fully ready. It helps prevent issues where JavaScript attempts to manipulate elements that 
    //haven't been created yet. 
    document.addEventListener("DOMContentLoaded", function () {
        const ingredientContainer = document.getElementById("ingredientContainer");
        const newIngredientButton = document.getElementById("button__new__ingredient");


        // Function to find the nearest ancestor with a specific class
        function findParentContainer(element, className) {
          while (element && element !== document) {
            if (element.classList.contains(className)) {
              return element;
            }
            element = element.parentNode;
          }
          return null; // Return null if no element with the specified class is found
        }

        // Function to handle the removal of a content instance
          function removeContentInstance(event) {
              const contentInstance = findParentContainer(event.target, 'new__recipe__content');
              if (contentInstance) {
                  contentInstance.remove();
              } else {
                  const updateContentInstance = findParentContainer(event.target, 'update__recipe__content');
                  if (updateContentInstance) {
                      updateContentInstance.remove();
                  }
              }
          }


        newIngredientButton.addEventListener("click", function () {
            // Clone the template content
            const newContent = document.querySelector(".new__recipe__content").cloneNode(true);
        
            // Clear only the input fields (excluding buttons) in the cloned content
            const ClearIngredient = newContent.querySelector("#new__recipe__ingredient");
            if (ClearIngredient) {
              ClearIngredient.value = "";
            }

            const ClearQuantity = newContent.querySelector("#new__recipe__quantity");
            if (ClearQuantity) {
              ClearQuantity.value = "";
            }


            // Set the "Remove ingredient" button's display style to "inline" or "block"
            const removeIngredientButton = newContent.querySelector(".button__remove__ingredient");
            // removeIngredientButton.style.display = "block";
            // Attach a click event handler to the "Remove ingredient" button in the cloned content
            removeIngredientButton.addEventListener("click", removeContentInstance);

            // Append the cloned content to the container
            newContent.style.display = "block";
            ingredientContainer.appendChild(newContent);
        });
        // Function to attach event listeners to existing "Remove ingredient" buttons
        const existingRemoveButtons = document.querySelectorAll(".button__remove__ingredient");
        existingRemoveButtons.forEach(button => {
            button.addEventListener("click", removeContentInstance);
        });
      });