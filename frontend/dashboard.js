document.addEventListener("DOMContentLoaded", () => {
    const userEmail = localStorage.getItem("userEmail");
    const userEmailDisplay = document.getElementById("userEmailDisplay");
    const logoutBtn = document.getElementById("logoutBtn");

    if (userEmail) {
        userEmailDisplay.textContent = "Welcome, ${userEmail}";
    } else{
        window.location.href= "index.html"; // If there is no user, go back to login
    }

    logoutBtn.addEventListener("click", () => {
        localStorage.removeItem("userEmail");
        window.location.href = "index.html";
    });
});

