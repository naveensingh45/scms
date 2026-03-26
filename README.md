# Student Complaint Management System (SCMS)

A modern full-stack web application for managing student complaints with role-based dashboards for **Students, Departments, and Admins**.

---

## 🚀 Features

### 🎨 UI/UX

* Responsive design with dark mode support
* Color-coded complaint categories and status badges
* Smooth animations and clean dashboards
* Complaint status stepper (Pending → In Progress → Resolved)
* Styled logout confirmation modal

### 👥 Role-Based Access

* **Students**: Submit complaints, track status, view replies
* **Departments**: Manage assigned complaints, post updates
* **Admins**: Assign complaints, monitor system, approve resolutions

### 📊 Dashboard

* Real-time complaint statistics
* Category-based organization
* Status filtering (Pending, In Progress, Resolved, Rejected)
* Visual stat cards for quick insights

### 🔐 Security

* Password hashing using Werkzeug
* Session-based authentication
* Role-based route protection

---

## 🛠 Tech Stack

* **Backend**: Python Flask
* **Database**: MySQL
* **Frontend**: HTML5, CSS3, JavaScript

---

## 📁 Project Structure

```
scms/
├── app.py
├── config.py
├── requirements.txt
├── database/
│   └── schema.sql
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── student_dashboard.html
│   ├── admin_dashboard.html
│   └── department_dashboard.html
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database (`config.py`)

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_DB = 'complaint_system'
```

### 3. Create Database & Tables

```sql
CREATE DATABASE complaint_system;
USE complaint_system;
```

```bash
mysql -u root -p complaint_system < database/schema.sql
```

### 4. Run Application

```bash
python app.py
```

Access the app at:
👉 http://localhost:5000

---

## 👤 Demo Accounts

| Role       | Email                                                   | Password |
| ---------- | ------------------------------------------------------- | -------- |
| Student    | [student@example.com](mailto:student@example.com)       | 123456   |
| Admin      | [admin@example.com](mailto:admin@example.com)           | 123456   |
| Department | [department@example.com](mailto:department@example.com) | 123456   |

---

## 📌 Core Features

### Complaint Categories

* Academic
* Hostel
* Administrative
* Infrastructure
* Other

### Status Flow

```
Pending → In Progress → Resolved
                    ↓
                  Rejected
```

---

## 🎨 Color Scheme

### Light Mode

* Primary: #2d5a8e
* Success: #2e7d52
* Warning: #b7691a
* Danger: #c0392b
* Background: #f4f1eb

### Dark Mode

* Primary: #4a8fd4
* Success: #3fa06a
* Warning: #d4882a
* Danger: #e05244
* Background: #0f0f0f

---

## ⚠️ Important Notes

* Debug mode is enabled by default — disable in production
* Change `SECRET_KEY` before deployment
* Use environment variables for sensitive data

---

## 🔐 Security Recommendations

* Enable HTTPS in production
* Add CSRF protection
* Implement rate limiting on login
* Use secure session handling

---

## 🛠 Customization

### Add New Complaint Category

Edit `database/schema.sql`:

```sql
category ENUM('academic', 'hostel', 'admin', 'infrastructure', 'other', 'new_category')
```

### Modify Colors

Edit CSS variables in:

```
static/css/style.css
```

---

## 🧪 Troubleshooting

### Database Connection Error

* Ensure MySQL is running
* Verify credentials in `config.py`
* Check database exists

### Template Not Found

* Verify files exist in `templates/`
* Check route template names

### Styling Issues

* Clear browser cache
* Ensure CSS file path is correct

---

## 👨‍💻 Contributors

* Naveen Singh — Backend
* Bhawesh Gunjiyal — UI/UX, Dark Mode, Enhancements

---

## 📄 License

MIT License

---

Built with ❤️ using Flask and MySQL
