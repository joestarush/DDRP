document.addEventListener("DOMContentLoaded", function () {
  const otpInputs = document.querySelectorAll(".otp-input");

  otpInputs.forEach((input, index) => {
    input.addEventListener("keyup", function (e) {
      // If the input is a number, move to the next input
      if (e.key >= 0 && e.key <= 9) {
        if (index < otpInputs.length - 1) {
          otpInputs[index + 1].focus();
        }
        // If backspace is pressed, move to the previous input
      } else if (e.key === "Backspace") {
        if (index > 0) {
          otpInputs[index - 1].focus();
        }
      }
    });

    // Prevent pasting non-numeric characters
    input.addEventListener("input", function () {
      input.value = input.value.replace(/[^0-9]/g, "");
    });
  });
});
