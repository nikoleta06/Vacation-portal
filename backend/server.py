from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sqlite3
from urllib.parse import urlparse, parse_qs

PORT = 8000
DB_NAME = "backend/database.db"


class LeavePortalServer(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Acess-Allow-Methods", "GET, POST,PUT,DELETE") 
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers() 

    def do_OPTIONS(self):                         # allow the browser to send the so-called preflight request, i add 2 more lines for connection with frontend
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")      # new line
        self.send_header("Access-Control-Max-Age", "86400")                                  #new line
        self.end_headers()

    def do_GET(self):
                                                # returns all permission requests for the specified user.
        print("GET request detected!")           #for debugging

        try:
            if self.path == "/users":
                print("GET /users detected")

                conn = sqlite3.connect(DB_NAME)
                conn.row_factory = sqlite3.Row
                users = conn.execute("SELECT id, name, email, role FROM users").fetchall()
                conn.close()
                
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps([dict(u) for u in users]).encode())
                print("Returned", len(users), "users")

            elif self.path.startswith("/vocation"):
                print("GET /vocation detected")

                # ---- Reading parameters from URL ----

                query = urlparse(self.path).query
                params = parse_qs(query)
                user_email = params.get("email", [None])[0]
                user_id = params.get("user_id", [None])[0]

                conn = sqlite3.connect(DB_NAME)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                   
                         # email or id
                if user_email:
                    print(f"Fetching vocation requests for email: {user_email}")
            
                    cursor.execute("""
                        SELECT v.id, v.start_date, v.end_date, v.reason, u.email 
                        FROM vocation_requests v
                        JOIN users u ON v.user_id = u.id 
                        WHERE u.email = ?
                        ORDER BY v.id DESC
                    """, (user_email,))

                elif user_id:
                    print(f"Fetching vocation requests fore user_id: {user_id}")
                    cursor.execute("""
                        SELECT v.id, v.start_date, v.end_date, v.reason, u.email 
                        FROM vocation_requests v
                        JOIN users u ON v.user_id = u.id 
                        WHERE u.email = ?
                        ORDER BY v.id DESC
                    """, (user_id,))


                else:
                    print("Fetching all vocation requests")
                    cursor.execute("""
                        SELECT v.id, v.start_date, v.end_date, v.reason, u.email 
                        FROM vocation_requests v
                        JOIN users u ON v.user_id = u.id 
                        WHERE u.email = ?
                        ORDER BY v.id DESC
                    """)

                rows = cursor.fetchall()
                conn.close()

                            # ..........  conversion of results.........
                results = [
                    {
                        "id": row["id"],
                        "start_date": row["start_date"],
                        "end_date": row["end_date"],
                        "reason": row["reason"],
                        "email": row["email"]
                    }
                    for row in rows
                ]   
                print("Returned", len(results), "vocation requests")

                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(results).encode())
            
            elif self.path == "/vocation_all":
                print("GET /vocation_all detected")
                conn = sqlite3.connect(DB_NAME)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM vocation_requests")
                rows = cursor.fetchall()
                conn.close()

                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps([dict(r) for r in rows]).encode())
                
            else:
                print("Invalid GET path:", self.path)
                                
                self.send_response(404)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Not found"}).encode())

        except Exception as e:
            print("SERVER ERROR:", e)
            self.send_response(500)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_POST(self):
        print("  do_POST triggered!") # i want to see what coming here
        
        try:
            if self.path == "/users":                     # Sign up creating new user 
                print("  POST /users detected")
                content_length= int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                user_data = json.loads(post_data)
                print("  Received data:", user_data)

                name = user_data.get("name")
                email = user_data.get("email")
                role = user_data.get("role", "employee")
                password = user_data.get("password")

                            # check
                if not name or not email or not password:
                    self.send_response(400)
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
                    self.send_header("Content-Type","application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Missing required fields"}).encode())
                    return
                
                conn= sqlite3.connect(DB_NAME)
                cursor = conn.cursor()

                # Check if user already exists
                cursor.execute("SELECT * FROM users WHERE email=?", (email,))
                existing_user = cursor.fetchone()

                if existing_user:
                    print(f"User already exists: {email}")
                    self.send_response(409)
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "User already exists"}).encode())
                    conn.close()
                    return
                
                # Insert new user
                cursor.execute("INSERT INTO users (name,email,role,password) VALUES (?,?,?,?)", 
                               (name,email,role,password))
                conn.commit()
                conn.close()
                print("User inserted into DB successfully")

                self.send_response(201)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "User created successfully"}).encode())

                

            # creating login for users connection
            elif self.path == "/login":                                     
                print("POST /login detected")         # this line for debugging

                 
                content_length=int(self.headers["Content-Length"])
                post_data=self.rfile.read(content_length)
                login_data= json.loads(post_data)
                print("Received login data:", login_data)

                email = login_data.get("email")
                password = login_data.get("password")

                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email,password))
                user = cursor.fetchone()
                conn.close()

                if user: 
                    print(f"Login successful for: {email}")
                    self.send_response(200)
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()

                    # here we take the data from user 
                    user_data = {
                        "id": user[0],
                        "name": user[1],
                        "email": user[2],
                        "role": user[3]
                    }

                    self.wfile.write(json.dumps({
                        "message": "Login successful",
                        "user": user_data
                    }).encode())
                else:
                    print(f"Login failed for: {email}")
                    self.send_response(401)
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Invalid credentials"}).encode())

                 # Submitting a permit application
            elif self.path == "/vocation":             # CREATION SUBMISSION OF A LICENSE APPLICATION 
                print("POST /vocation detected") 

                content_length= int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                vocation_data = json.loads(post_data)
                print("Received vocation data:", vocation_data)

                user_id = vocation_data.get("user_id")
                start_date= vocation_data.get("start_date")
                end_date = vocation_data.get("end_date")
                reason = vocation_data.get("reason")


                # Validation 
                if not user_id or not start_date or not end_date or not reason:
                    self.send_response(400)
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Missing required fields"}).encode())
                    return

                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
 
                #  Add application with status 'pending'
                cursor.execute(
                    """ 
                    INSERT INTO vocation_requests (user_id, start_date, end_date, reason, status)
                    VALUES (?, ?, ?, 'pending')
                    """,
                    (user_id, start_date, end_date, reason))
                    
                conn.commit()
                conn.close()
                print("Vacation request inserted into DB (pending approval)")

                self.send_response(201)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Vacation request submitted successfully"}).encode())


                      # IN CASE  something wrong 
            else:                                                               
                print("Invalid POST path:", self.path)
                self.send_response(404)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Not found"}).encode())


        except Exception as e:
                print(f" SERVER ERROR: {e}")
                self.send_response(500)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())


    def do_PUT(self):
        print("PUT /vocation detected")

        try:
            if self.path =="/vocation":
                
                 # read data from request body 
                content_length= int(self.headers["Content-Length"])
                put_data = self.rfile.read(content_length)
                update_data = json.loads(put_data)
                print("Received update data:", update_data)

                 # get the fields from json 
                vocation_id = update_data.get("id")
                new_status = update_data.get("status")

                if not vocation_id or new_status not in ["approved", "rejected"]:
                    self.send_response(400)
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Missing or invalid fields"}).encode())
                    return
                
                # Update database 
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute("UPDATE vocation_requests SET status=? WHERE id=?", (new_status, vocation_id))
                conn.commit()
                conn.close()

                print(f"Vocation {vocation_id} updated to {new_status}")

                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Vocation status updated successfully"}).encode())

            else:
                print("Invalid PUT path:", self.path)
                self.send_response(404)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"errors": "Not found"}).encode())

        except Exception as e:
            print("SERVER ERROR:", e)
            self.send_response(500)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())


# start server 

if __name__ == "__main__":
    server = HTTPServer(("", PORT), LeavePortalServer)
    print(f"start server running at http://localhost:{PORT}")
    server.serve_forever()
      
