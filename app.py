from flask import Flask, render_template, request, redirect, session, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import config

app = Flask(__name__)
app.config.from_object(config)
mysql = MySQL(app)

def check_login():
    """Check if user is logged in"""
    return 'user_id' in session

def get_user_info():
    """Get current user info from session"""
    if check_login():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id=%s", [session['user_id']])
        user = cur.fetchone()
        if not user:
            session.clear()
        return user
    return None

@app.route("/")
def home():
    if check_login():
        user = get_user_info()
        if user[4] == 'admin':
            return redirect("/admin")
        elif user[4] == 'department':
            return redirect("/department")
        return redirect("/dashboard")
    return render_template("login.html")

@app.route("/register_page")
def register_page():
    # Always allow registering a new account; if already logged in, clear the old session.
    if check_login():
        session.clear()

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT name FROM departments ORDER BY name")
        departments = [d[0] for d in cur.fetchall()]
    except Exception as e:
        app.logger.exception("Error loading departments")
        departments = []
    
    return render_template("register.html", departments=departments)

@app.route("/register", methods=["POST"])
def register():
    try:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role', 'student')
        department = request.form.get('department', '').strip() if role == 'department' else None

        if not name or not email or not password:
            return render_template("register.html", error="All fields are required")

        if role == 'department' and not department:
            return render_template("register.html", error="Department is required for department role")

        # Check if email already exists
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE email=%s", [email])
        if cur.fetchone():
            return render_template("register.html", error="Email already exists")

        password_hash = generate_password_hash(password)

        if role == 'department':
            cur.execute("INSERT INTO users(name,email,password,role,department) VALUES(%s,%s,%s,%s,%s)", 
                        (name, email, password_hash, role, department))
        else:
            cur.execute("INSERT INTO users(name,email,password,role,department) VALUES(%s,%s,%s,%s,%s)",
                        (name, email, password_hash, role, None))

        mysql.connection.commit()
        
        # Ensure new registration does not continue any existing session
        session.clear()
        return redirect("/")
    except Exception as e:
        app.logger.exception("Registration error")
        return render_template("register.html", error=f"An error occurred during registration: {str(e)}")

@app.route("/login", methods=["POST"])
def login():
    try:
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            return render_template("login.html", error="Please enter email and password")

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", [email])
        user = cur.fetchone()

        if not user:
            return render_template("login.html", error="Invalid email or password")

        # Ensure column indexes are correct
        password_hash = user[3] if len(user) > 3 else None
        role = user[4] if len(user) > 4 else 'student'
        name = user[1] if len(user) > 1 else ''
        department = user[5] if len(user) > 5 else ''

        if not password_hash:
            return render_template("login.html", error="User record is invalid")

        if check_password_hash(password_hash, password):
            session['user_id'] = user[0]
            session['role'] = role
            session['name'] = name
            session['department'] = department or ''

            if role == 'admin':
                return redirect("/admin")
            elif role == 'department':
                return redirect("/department")
            return redirect("/dashboard")

        return render_template("login.html", error="Invalid email or password")
    except Exception as e:
        app.logger.exception("Login error")
        return render_template("login.html", error="Unexpected error on login")

@app.route("/dashboard")
def dashboard():
    if not check_login():
        return redirect("/")
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM complaints WHERE user_id=%s ORDER BY created_at DESC", [session['user_id']])
        complaints = cur.fetchall()
        
        # Get statistics
        cur.execute("SELECT COUNT(*) FROM complaints WHERE user_id=%s", [session['user_id']])
        total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM complaints WHERE user_id=%s AND status='pending'", [session['user_id']])
        pending = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM complaints WHERE user_id=%s AND status='in_progress'", [session['user_id']])
        inprogress = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM complaints WHERE user_id=%s AND status='resolved'", [session['user_id']])
        resolved = cur.fetchone()[0]
    except Exception as e:
        app.logger.exception("Dashboard query error")
        complaints = []
        total = pending = inprogress = resolved = 0
    
    stats = {
        'total': total,
        'pending': pending,
        'inprogress': inprogress,
        'resolved': resolved
    }
    
    return render_template("student_dashboard.html", complaints=complaints, name=session['name'], stats=stats)
    
    stats = {
        'total': total,
        'pending': pending,
        'inprogress': inprogress,
        'resolved': resolved
    }
    
    return render_template("student_dashboard.html", complaints=complaints, name=session['name'], stats=stats)

@app.route("/admin")
def admin():
    if not check_login() or session.get('role') != 'admin':
        return redirect("/")
    
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT complaints.*, users.name as user_name FROM complaints 
        JOIN users ON complaints.user_id = users.id 
        ORDER BY complaints.created_at DESC
    """)
    complaints = cur.fetchall()
    
    # Get statistics
    cur.execute("SELECT COUNT(*) FROM complaints")
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM complaints WHERE status='pending'")
    pending = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM complaints WHERE status='in_progress'")
    inprogress = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM complaints WHERE status='resolved'")
    resolved = cur.fetchone()[0]
    
    # Get departments
    cur.execute("SELECT name FROM departments ORDER BY name")
    departments = [d[0] for d in cur.fetchall()]
    
    stats = {
        'total': total,
        'pending': pending,
        'inprogress': inprogress,
        'resolved': resolved
    }
    
    return render_template("admin_dashboard.html", complaints=complaints, name=session['name'], 
                          stats=stats, departments=departments)

@app.route("/department")
def department():
    if not check_login() or session.get('role') != 'department':
        return redirect("/")
    
    user_name = session.get('name')
    department_name = session.get('department', '')

    assigned_filters = []
    if user_name:
        assigned_filters.append(user_name)
    if department_name and department_name not in assigned_filters:
        assigned_filters.append(department_name)
    assigned_filters.append('department')

    placeholders = ', '.join(['%s'] * len(assigned_filters))

    cur = mysql.connection.cursor()
    query = f"""
        SELECT complaints.*, users.name as user_name FROM complaints 
        JOIN users ON complaints.user_id = users.id 
        WHERE complaints.assigned_to IN ({placeholders})
        ORDER BY complaints.created_at DESC
    """
    cur.execute(query, tuple(assigned_filters))
    complaints = cur.fetchall()
    
    # Get statistics
    count_query = f"SELECT COUNT(*) FROM complaints WHERE assigned_to IN ({placeholders})"
    cur.execute(count_query, tuple(assigned_filters))
    total = cur.fetchone()[0]

    cur.execute(count_query + " AND status='pending'", tuple(assigned_filters))
    pending = cur.fetchone()[0]

    cur.execute(count_query + " AND status='in_progress'", tuple(assigned_filters))
    inprogress = cur.fetchone()[0]

    cur.execute(count_query + " AND status='resolved'", tuple(assigned_filters))
    resolved = cur.fetchone()[0]
    
    stats = {
        'total': total,
        'pending': pending,
        'inprogress': inprogress,
        'resolved': resolved
    }
    
    return render_template("department_dashboard.html", complaints=complaints, name=session['name'], stats=stats)

@app.route("/complaint/<int:id>")
def view_complaint(id):
    if not check_login():
        return redirect("/")
    
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT complaints.*, users.name as user_name FROM complaints 
        JOIN users ON complaints.user_id = users.id 
        WHERE complaints.id=%s
    """, [id])
    complaint = cur.fetchone()
    
    # Check authorization
    if not complaint:
        return redirect("/")
    
    user = get_user_info()
    if not user:
        return redirect("/")

    user_role = user[4]
    user_name = user[1]
    assigned_to = complaint[6] or ''

    if user_role == 'student' and complaint[1] != user[0]:
        return redirect("/")
    elif user_role == 'department' and assigned_to not in [user_name, session.get('department', ''), user_role]:
        return redirect("/")
    
    # Get replies
    cur.execute("""
        SELECT replies.*, users.name as reply_user_name FROM replies
        JOIN users ON replies.user_id = users.id
        WHERE replies.complaint_id=%s
        ORDER BY replies.created_at ASC
    """, [id])
    replies = cur.fetchall()
    
    return jsonify({
        'complaint': {
            'id': complaint[0],
            'title': complaint[2],
            'description': complaint[3],
            'category': complaint[4],
            'status': complaint[5],
            'assigned_to': complaint[6],
            'user_name': complaint[9],
            'created_at': str(complaint[7]),
            'updated_at': str(complaint[8])
        },
        'replies': [{'id': r[0], 'reply': r[3], 'user': r[5], 'created_at': str(r[4])} for r in replies]
    })

@app.route("/add", methods=["POST"])
def add():
    if not check_login():
        return redirect("/")
    
    try:
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO complaints(user_id, title, description, category, status) 
            VALUES(%s, %s, %s, %s, 'pending')
        """, (session['user_id'], title, description, category))
        mysql.connection.commit()
        
        return redirect("/dashboard")
    except Exception as e:
        return redirect("/dashboard")

@app.route("/assign/<int:id>", methods=["POST"])
def assign(id):
    if not check_login() or session.get('role') != 'admin':
        return redirect("/")
    
    try:
        dept = request.form['department']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE complaints SET assigned_to=%s, status='in_progress' WHERE id=%s", (dept, id))
        mysql.connection.commit()
        return redirect("/admin")
    except:
        return redirect("/admin")

@app.route("/update/<int:id>/<status>")
def update(id, status):
    if not check_login():
        return redirect("/")
    
    status = status.lower().replace('-', '_').replace(' ', '_')
    valid_statuses = ['pending', 'in_progress', 'resolved', 'rejected']
    if status not in valid_statuses:
        return redirect("/")
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE complaints SET status=%s WHERE id=%s", (status, id))
        mysql.connection.commit()
        
        if session.get('role') == 'admin':
            return redirect("/admin")
        elif session.get('role') == 'department':
            return redirect("/department")
        else:
            return redirect("/dashboard")
    except Exception as e:
        return redirect("/")

@app.route("/reply/<int:complaint_id>", methods=["POST"])
def add_reply(complaint_id):
    if not check_login():
        return redirect("/")
    
    try:
        reply_text = request.form.get('reply', '')
        if not reply_text:
            return redirect("/")
        
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO replies(complaint_id, user_id, reply_text)
            VALUES(%s, %s, %s)
        """, (complaint_id, session['user_id'], reply_text))
        mysql.connection.commit()
        
        return redirect(request.referrer or "/")
    except:
        return redirect("/")

@app.route("/reset_db")
def reset_db():
    if not check_login() or session.get('role') != 'admin':
        return "Unauthorized"
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("DROP TABLE IF EXISTS replies")
        cur.execute("DROP TABLE IF EXISTS complaints")
        cur.execute("DROP TABLE IF EXISTS departments")
        cur.execute("DROP TABLE IF EXISTS users")
        mysql.connection.commit()
        
        # Recreate tables
        with open('database/schema.sql', 'r') as f:
            sql = f.read()
        for statement in sql.split(';'):
            if statement.strip():
                cur.execute(statement)
        mysql.connection.commit()
        
        return "Database reset successfully"
    except Exception as e:
        return f"Error resetting database: {str(e)}"

@app.route("/update_schema")
def update_schema():
    if not check_login() or session.get('role') != 'admin':
        return "Unauthorized"
    
    try:
        cur = mysql.connection.cursor()
        
        # Check if department column exists
        cur.execute("SHOW COLUMNS FROM users LIKE 'department'")
        if not cur.fetchone():
            cur.execute("ALTER TABLE users ADD COLUMN department VARCHAR(100)")
            mysql.connection.commit()
            return "Schema updated successfully: added department column"
        else:
            return "Schema is already up to date"
    except Exception as e:
        return f"Error updating schema: {str(e)}"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.exception('Internal server error')
    return redirect("/")

@app.errorhandler(404)
def not_found_error(e):
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)