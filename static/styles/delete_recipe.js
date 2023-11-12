// As the buttons are being created through a for loop to extract the information from the Flask framework, a list of all buttons is created
let btns_delete = document.querySelectorAll(".delete__button");

// A listener is then added to each button before executing the deletefunction
btns_delete.forEach(btn_delete => {

  btn_delete.addEventListener('click', async (event)=> {

    event.preventDefault();
    
    // Confirm deletion
    var result = confirm("Are you sure you want to DELETE this recipe?");
    if (result) {
      await deletefunction(btn_delete.value);
    }

    // Redirect back to home page
    window.location.href = "http://127.0.0.1:5000/"
  });
});
  
async function deletefunction(buttonValue) {
  /** 
  * Passes the button id to the flask framework
  * Expects: activation of modification button, string: button id
  * Action: POST button id to the Flask framework
  * Returns: none.
  */

    var formData = new FormData();
    formData.append('button', buttonValue);
    formData.append('request_type', 'delete_recipe');

    return fetch('/', {
        method: 'POST',
        body: formData
      }).catch(error => console.error(error));
  }