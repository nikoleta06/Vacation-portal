document.addEventListener("DOMContentLoaded", () => {
    const userEmail = localStorage.getItem("userEmail");
    const welcomeMsg = document.getElementById("welcomeMsg");
    const logoutBtn = document.getElementById("logoutBtn");
    const requestBtn = document.getElementById("requestBtn");
    const vacationForm = document.getElementById("vacationForm");
    const saveVacationBtn = document.getElementById("saveVacationBtn");
    const vacationTableBody = document.querySelector("#vacationTable tbody");

    //---------user login check--------
    if (userEmail) {
        // We remove the part before the @ so it appears as a name//
        const userName = userEmail.split("@")[0];
        // We capitalize the first letter (e.g. maria -> Maria)//
        const formattedName = userName.charAt(0).toUpperCase() + userName.slice(1);
         // We display the message//
        welcomeMsg.textContent = `Welcome, ${formattedName}!`;
    } else{
        window.location.href= "index.html"; // If there is no user, go back to login
    }

        //......... LOGOUT........
    logoutBtn.addEventListener("click", () => {
        localStorage.removeItem("userEmail");
        window.location.href = "index.html";
    });

    //----------toggle vacation form----------
    requestBtn.addEventListener("click", () => {
        vacationForm.classList.toggle("hidden");
    });

    //----Save vacation request------
    saveVacationBtn.addEventListener("click", async () => {
        const starDate = document.getElementById("startDate").value;
        const endDate = document.getElementById("endDate").value;
        const reason = document.getElementById("reason").value;

        if(!startDate || !endDate || !reason){
            alert("Please fell all fields!");
            return;
        }

        //-----Find user ID by email---------
        
    })
});

