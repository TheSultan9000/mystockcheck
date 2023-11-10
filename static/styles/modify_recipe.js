
// As the buttons are being created through a for loop to extract the information from the Flask framework, a list of all buttons is created
let btns = document.querySelectorAll(".modification__button");

// A listener is then added to each button before executing the deletefunction
btns.forEach(btn => {

   btn.addEventListener('click', async (event)=> {

    event.preventDefault();
    
    await modifyfunction(btn.value);
  });
});
  
async function modifyfunction(buttonValue) {
  /** 
  * Passes the button id to the flask framework
  * Expects: activation of modification button, string: button id
  * Action: POST button id to the Flask framework
  * Returns: none.
  */

    var formData = new FormData();
    formData.append('button', buttonValue);
    formData.append('request_type', 'modify_recipe');

    return fetch('/', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        window.location.href = "http://127.0.0.1:5000/" + data + "/";
      })
        .catch(error => console.error(error));
  }