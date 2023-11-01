// This script was created to allow communication between the upload HTML and Flask function
document.getElementById('new__recipe__submit').addEventListener('submit', async function(event) {
    // This is used to prevent defult form behaviour to ensure the function is excecuted below
      event.preventDefault();
    
      // await ensures the Flask function is complete before progessing
      await sumbitRecipe();
    
      // Reload the page once the script is executed
      location.reload();
    });
    
    function sumbitRecipe() {
        var recipeValue = document.getElementById('new__recipe__name').value;
        // Get all elements with the same ID
        var elements = document.querySelectorAll('#new__recipe__ingredient');
        var ingredientValue = []
        elements.forEach(function (element){
            ingredientValue.push(element.value);
        });
        var elements = document.querySelectorAll('#meal__days');
        var dayValue = []
        elements.forEach(function (element){
            dayValue.push(element.value);
        });
        var elements = document.querySelectorAll('#complete__meal');
        var completeValue = []
        elements.forEach(function (element){
            completeValue.push(element.value);
        });
        var elements = document.querySelectorAll('#new__recipe__quantity');
        var quantityValue = []
        elements.forEach(function (element){
            quantityValue.push(element.value);
        });
        var elements = document.querySelectorAll('#measure__name');
        var measureValue = []
        elements.forEach(function (element){
            measureValue.push(element.value);
        });
        var elements = document.querySelectorAll('#ingredient__type');
        var typeValue = []
        elements.forEach(function (element){
          typeValue.push(element.value);
        });
        
      var formData = new FormData();
      formData.append('recipe', recipeValue);
      formData.append('ingredient', ingredientValue);
      formData.append('quantity', quantityValue);
      formData.append('measure', measureValue);
      formData.append('day', dayValue);
      formData.append('complete', completeValue);
      formData.append('type', typeValue);
  
      return fetch('/newrecipe/', {
          method: 'POST',
          body: formData
        })
          .catch(error => console.error(error));
    }