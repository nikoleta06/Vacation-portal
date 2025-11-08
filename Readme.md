### SET UP  
1. git clone https://github.com/nikoleta06/Vacation-portal.git
2. cd Vacation-portal
3. py backend/server.py

4. open frontend/index.html with a browser

###  Application Architecture
1. Frontend (HTML/CSS/JS) : UI presentation, login handling, dashboard display
2. Backend (Python HTTPServer) /login, /users, /vocation request management
3. Database (SQLite3) User and permission request storage

###  Execution Flow
1. User opens index.html
2. Logs in → data is fetched() to the server (/login)
3. If valid, userEmail is stored in localStorage
4. Browser navigates to dashboard.html
5.dashboard.js retrieves the email from localStorage and displays the welcome message.
6.Role management (Administrator table). There is an administrator role for approving/rejecting applications.
7.Full connection of the control panel to the database. The application table has been dynamically updated from the backend. 

### Unimplemented Functions
1. Display all applications    Only the applications of the logged-in user are displayed.   
2. Edit / Delete applications    It is not possible to change or cancel an application. 
3. Secure storage of passwords	Passwords are not stored with encryption (hash).
4. Data validation    There are no checks for incomplete or incorrect information in the form. 


