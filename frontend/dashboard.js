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
        const start_date = document.getElementById("startDate").value;
        const end_date = document.getElementById("endDate").value;
        const reason = document.getElementById("reason").value;

        if(!start_date || !end_date || !reason) {
            alert("Please fill all fields!");
            return;
        }

        //-----Find user ID by email---------
        const userEmail = localStorage.getItem("userEmail");
        const userResponse = await fetch("http://127.0.0.1:8000/users");
        const users = await userResponse.json();
        const user = users.find(u => u.email === userEmail);

        if(!user) {
            alert("User not found in database!");
            return;
        }
        
        const vocationData = {
            user_id: user.id,
            start_date: start_date,
            end_date: end_date,
            reason: reason
        };

        try {
            const response = await fetch("http://127.0.0.1:8000/vocation", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(vocationData)
            });

            const data = await response.json();

            if (response.ok) {
                alert("Vacation request submitted successfully!");
                vacationForm.classList.add("hidden");
                loadVacationRequests();   // refreshes the table
            } else {
              alert("Error: " + data.error);
            }    
        } catch (error) {
          alert("Server error: " + error.message);
        }
    });

    //--------Function to calculate total days between two days--------
    function calcDays(start, end) {
        const startDate = new Date(start);
        const endDate = new Date(end);
        const diffTime = endDate - startDate;
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1; // inclusive count
    }


    //-------Load existing requests--------
    async function loadVacationRequests() {
        try {
            const userEmail = localStorage.getItem("userEmail");
            const response = await fetch(`http://127.0.0.1:8000/vocation?email=${userEmail}`);
            const data = await response.json();

            vacationTableBody.innerHTML = "";  //----Clear old rows-----

            if (data.length === 0) {
                vacationTableBody.innerHTML = `<tr><td colspan="5" style="text-align:center;">No vacation requests yet.</td></tr>`;
                return;
            }

            data.forEach(req => {
                const totalDays = calcDays(req.start_date, req.end_date); // ---This is where the calculation takes place.
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${new Date().toLocaleDateString()}</td>
                    <td>${req.start_date} - ${req.end_date}</td>
                    <td>${req.reason}</td>
                    <td>${totalDays} days</td>
                    <td>${req.status || "pending"}</td>
                `;
                vacationTableBody.appendChild(row);
            });
        
        } catch (error) {
            console.error("Error loading vacation requests:", error);
        }
    }

    //-------Helper- Calculate total days----
    function calcDays(start, end) {
        const s = new Date(start);
        const e = new Date(end);
        const diff = (e-s) / (1000 * 3600 * 24) + 1;
        return diff;
    }

    // ----Load existing requests on page load-----
    loadVacationRequests();

});

