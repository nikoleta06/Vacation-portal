document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("signupForm");
    const message = document.getElementById("message");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        console.log("Signup form submitted!");

        const name = document.getElementById("name").value;
        const email= document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try {
            const response = await fetch("http://127.0.0.1:8000/users", {
                method: "POST",
                headers: {"Content-Type": "application/json" },
                body: JSON.stringify({ name, email, password }),
            });

            const data = await response.json();

            if (response.ok) {
                message.style.color= "green";
                message.textContent= "Registration successful! You can now log in";
                form.reset();  //clears the fields
            } else {
                message.style.color= "red";
                message.textContent= (data.error || "Error during registration.");
            }
        } catch (error) {
          message.style.color="red";
          message.textContent="Error connecting to the server.";
        }
    });
});