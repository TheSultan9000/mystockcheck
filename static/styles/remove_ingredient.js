    // Using the DOMContentLoaded event is a common practice in web development to ensure that JavaScript code that interacts with the 
    // DOM is executed only after the DOM is fully ready. It helps prevent issues where JavaScript attempts to manipulate elements that 
    //haven't been created yet. 
    document.addEventListener("DOMContentLoaded", function () {
        const ingredientContainer = document.getElementById("ingredientContainer");
        const newIngredientButton = document.getElementById("button__new__ingredient");
    
        // Function to handle the removal of a content instance
        function removeContentInstance(event) {
          const contentInstance = event.target.closest(".new__recipe__content");
          if (contentInstance && ingredientContainer.contains(contentInstance)) {
            ingredientContainer.removeChild(contentInstance);
          }
        }
    
        newIngredientButton.addEventListener("click", function () {
            // Clone the template content
            const newContent = document.querySelector(".new__recipe__content").cloneNode(true);
        
            // Clear only the input fields (excluding buttons) in the cloned content
            const inputs = newContent.querySelectorAll("input:not([type='submit'])");
            inputs.forEach((input) => {
                input.value = "";
            });

            // Set the "Remove ingredient" button's display style to "inline" or "block"
            const removeIngredientButton = newContent.querySelector(".button__remove__ingredient");
            removeIngredientButton.style.display = "block";

            // Append the cloned content to the container
            ingredientContainer.appendChild(newContent);
        
            // Attach a click event handler to the "Remove ingredient" button in the cloned content
            removeIngredientButton.addEventListener("click", removeContentInstance);
        });
      });