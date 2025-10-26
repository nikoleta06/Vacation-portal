document.addEventListener("DOMContentLoaded", async () => {
    const tableBody = document.querySelector("#vocationTable tbody");

    //1. Fetch all the applications from the server
    const response = await fetch("http://127.0.0.1:8000/vocation_all");
    const requests = await response.json();
    
    //2. Display the applications in table
    requests.forEach(req => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <><td>${req.id}</td><td>${req.user_id}</td><td>${req.start_date}</td><td>${req.end_date}</td><td>${req.reason}</td><td>${req.status}</td><td>
                <button class="approve" data-id="${req.id}">acceptable</button>
                <button class="reject" data-id="${req.id}">not acceptable</button>
            </td></>
        `;
        tableBody.appendChild(row);
    });

    // 3. Add event listeners for the button
    document.addEventListener("click", async (e) => {
        if (e.target.classList.contains("approve") || e.target.classList.contains("reject")) {
           const id = e.target.dataset.id;
           const status = e.target.classList.contains("approve") ? "approved" : "rejected";

           const res = await fetch("http://127.0.0.1:8000/vocation", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id, status })
           });

           if (res.ok) {
            alert(`The application #${id} updated to ${status}`);
            location.reload();
           } else {
            alert("Error while updating!");
           }
        }
    });
});