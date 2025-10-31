document.addEventListener("DOMContentLoaded",  () => {
    const logoutBtn = document.getElementById("logoutBtn");
    const tableBody = document.querySelector("#applicationsTable tbody");

    //-----Logout--------
    logoutBtn.addEventListener("click", () => {
        localStorage.removeItem("userEmail");
        window.location.href = "index.html";
    });

    // -------Load all vacation requests----------
    async function loadApplications() {
        try {
            const response = await fetch("http://127.0.0.1:8000/vocation");
            const data = await response.json();

            tableBody.innerHTML = "";

            data.forEach(req => {
                const row = document.createElement("tr");
                row.innerHTML= `
                    <td>${req.id}</td>
                    <td>${req.email}</td>
                    <td>${req.start_date}</td>
                    <td>${req.end_date}</td>
                    <td>${req.reason}</td>
                    <td>${req.status || "pending"}</td>
                    <td>
                        <buttton class="approveBtn" data-id="${req.id}">Approve</button>
                        <button class="rejectBtn" data-id="${req.id}">Reject</button>
                    </td>    
                `;
                tableBody.appendChild(row);
            });

            //--Attach events for approve/reject buttons---
            document.querySelectorAll(".approveBtn").forEach(btn => {
                btn.addEventListener("click", () => updateStatus(btn.dataset.id, "approved"));   
            });
            document.querySelectorAll(".rejectBtn").forEach(btn => {
                btn.addEventListener("click", () => updateStatus(btn.dataset.id, "rejected"));
            });
           
        } catch (error) {
            console.error("Error loading applications:", error);
        }
    }

    //---Update vacation request status------
    async function updateStatus(id,status) {
        try {
            const response = await fetch("http://127.0.0.1:8000/vocation", {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id, status }),
            });

            const data = await response.json();

            if (response.ok) {
                alert(`Request #${id} ${status}!`);
                loadApplications();
            } else {
                alert("Error:" + data.error);
            }
        } catch (error) {
            alert("Server error: " + error.message);
        }
    }

    loadApplications();

});

            
    

   