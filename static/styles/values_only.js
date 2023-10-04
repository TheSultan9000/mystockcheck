function validateInput(input) {
    // Remove any non-numeric characters, including "e"
    input.value = input.value.replace(/[^0-9.]/g, '');
  }