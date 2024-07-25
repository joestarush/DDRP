document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("donation-form");
  const editButton = document.querySelector(".btn-edit");
  const submitButton = document.querySelector(".btn-submit");
  const inputs = form.querySelectorAll("input");

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    let valid = true;
    inputs.forEach((input) => {
      if (!input.value.trim()) {
        valid = false;
        input.style.borderColor = "red";
      } else {
        input.style.borderColor = "#ccc";
      }
    });

    if (valid) {
      const data = {
        donatorId: document.getElementById("donator-id").value,
        donatorName: document.getElementById("donator-name").value,
        adminId: document.getElementById("admin-id").value,
      };

      fetch("log_requirements", {
        // Replace with your Django view URL
        method: "POST",
        body: JSON.stringify(data),
        headers: { "Content-Type": "application/json" },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            alert("Form Submitted Successfully!");
            // Clear form or show success message in UI
          } else {
            alert("Error: " + data.message); // Handle errors from Django view
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("An error occurred. Please try again later.");
        });
    } else {
      alert("Please fill all the fields.");
    }
  });

  // Edit button functionality remains the same
});
