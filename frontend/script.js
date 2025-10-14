


document.addEventListener("DOMContentLoaded", () => {
    
    console.log("script loaded");

    const form = document.getElementById("loginForm");
    if (!form){
        console.error("Login form not found!");
        return;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        console.log("Login form submitted");
        
    

        const email= document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const message = document.getElementById("message");

        try{
          const response = await fetch("http://127.0.0.1:8000/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({email, password})
          });

          const data = await response.json();

          if (response.ok) {
            message.style.color = "green";
            message.textContent = "Successful connection"
            
            //........SAVE NAME AND EMAIL.......//
            localStorage.setItem("userEmail", email);

            const userName = email.split("@")[0];        // save the name of user from email
            localStorage.setItem("userName", userName);

            setTimeout(() => {
              window.location.href = "dashboard.html";
            },1500);

          } else{
            message.style.color = "red";
            message.textContent = "ERROR" + (data.error || "Incorrect email or password");
          }
        } catch (error) {
          message.style.color = "red";
          message.textContent =  "Server Error: " + error.message;
        }
    });  // close form.addEventListener
});      // close document.addEventListener
