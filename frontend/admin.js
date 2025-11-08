document.addEventListener("DOMContentLoaded",  () => {
    const logoutBtn = document.getElementById("logoutBtn");
    const tableBody = document.querySelector("#applicationTable tbody");

    //-----Logout--------
    logoutBtn.addEventListener("click", () => {
        localStorage.removeItem("userEmail");
        window.location.href = "index.html";
    });

    // -------Load all vacation requests----------
    async function loadApplications() {
        try {
            const response = await fetch("http://127.0.0.1:8000/admin/vocations");
            const data = await response.json();

            tableBody.innerHTML = "";

            if (data.length === 0) {
                tableBody.innerHTML = `<tr><td colspan="8" style="text-align:center;">No vocation requests found.</td></tr>`;
                return;
            }

            data.forEach(req => {
                const row = document.createElement("tr");
                const statusColor = req.status === "approved" ? "green" : req.status === "rejected" ? "red" : "orange";
                row.innerHTML= `
                    <td>${req.id}</td>
                    <td>${req.name || "-"}</td>
                    <td>${req.email}</td>
                    <td>${req.start_date}</td>
                    <td>${req.end_date}</td>
                    <td>${req.reason}</td>
                    <td>${req.status || "pending"}</td>
                    <td>
                        <button class="approveBtn" data-id="${req.id}">Approve</button>
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

    //---Update vacation request status,PUT request------
    async function updateStatus(id,status) {
        try {
            console.log("Sending update:", { id, status });
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

    // loading all vocation request on page load
    loadApplications();

});

            
    

   