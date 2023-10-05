function validateNumberInput(input) {
    // Remove any non-numeric characters, including "e"
    input.value = input.value.replace(/[^0-9.]/g, '');
  }

  function validateTextInput(input) {
    // Remove any commas as this will affect listing in python
    input.value = input.value.replace(/,/g, '');
  }
