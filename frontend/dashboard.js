document.addEventListener("DOMContentLoaded", () => {
    const userEmail = localStorage.getItem("userEmail");
    const welcomeText = document.getElementById("welcomeText");
    

    if (userEmail) {
          
        // We remove the part before the @ so it appears as a name//
        const userName = userEmail.split("@")[0];

        // We capitalize the first letter (e.g. maria -> Maria)//
        const formattedName = userName.charAt(0).toUpperCase() + userName.slice(1);

        welcomeText.textContent = `Welcome, ${formattedName}!`;
    } else{
        window.location.href= "index.html"; // If there is no user, go back to login
    }

    const logoutBtn = document.getElementById("logoutBtn");
    logoutBtn.addEventListener("click", () => {
        localStorage.removeItem("userEmail");
        window.location.href = "index.html";
    });
});

