# Student Complaint Management System (SCMS)

A beautiful, modern fullstack web application for managing student complaints with role-based dashboards for students, departments, and administrators.

## Features

✨ **Modern UI/UX**
- Beautiful, responsive design with color-coded complaint categories
- Smooth animations and transitions
- Mobile-friendly interface

👥 **Role-Based Access**
- **Students**: File complaints, track status, view replies
- **Departments**: Manage assigned complaints, post updates
- **Admins**: Oversee all complaints, assign to departments, approve resolutions

📊 **Dashboard Features**
- Real-time statistics and complaint counts
- Category-based organization (Academic, Hostel, Administrative, Infrastructure)
- Status tracking (Pending, In Progress, Resolved, Rejected)
- Color-coded badges for quick status identification

🔒 **Security**
- Password hashing with Werkzeug
- Session-based authentication
- Role-based route protection

## Tech Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Design**: Custom CSS with beautiful color scheme

## Project Structure

```
scms/
├── app.py                    # Flask application & routes
├── config.py                 # Database configuration
├── requirements.txt          # Python dependencies
├── database/
│   └── schema.sql           # Database schema
├── static/
│   └── css/
│       └── style.css        # Application styling
├── templates/
│   ├── base.html            # Base template with sidebar
│   ├── login.html           # Login page
│   ├── register.html        # Register page
│   ├── student_dashboard.html      # Student dashboard
│   ├── admin_dashboard.html        # Admin dashboard
│   └── department_dashboard.html   # Department dashboard
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.7+
- MySQL Server
- pip (Python package manager)

### 1. Clone & Install Dependencies

```bash
cd scms
pip install -r requirements.txt
```

### 2. Configure Database

Update `config.py` with your MySQL credentials:
```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_DB = 'complaint_system'
```

### 3. Create Database & Tables

Create the database in MySQL:
```sql
CREATE DATABASE complaint_system;
USE complaint_system;
```

Then run the schema:
```bash
mysql -u root -p complaint_system < database/schema.sql
```

### 4. Add Demo Data (Optional)

Insert demo users for testing:
```sql
INSERT INTO users (name, email, password, role) VALUES
('John Student', 'student@example.com', 'pbkdf2:sha256:...', 'student'),
('Admin User', 'admin@example.com', 'pbkdf2:sha256:...', 'admin'),
('Dept Manager', 'department@example.com', 'pbkdf2:sha256:...', 'department');
```

Use password hash from Python:
```python
from werkzeug.security import generate_password_hash
print(generate_password_hash('123456'))
```

### 5. Run Application

```bash
python app.py
```

Access at: `http://localhost:5000`

## Demo Accounts

For testing, create accounts with these credentials (in the application):

| Role | Email | Password |
|------|-------|----------|
| Student | student@example.com | 123456 |
| Admin | admin@example.com | 123456 |
| Department | department@example.com | 123456 |

## File Format Guide

### Static Files
- All CSS is in `static/css/style.css`
- Add custom stylesheets in the same directory
- Images should be placed in `static/images/`

### Templates
- Use Jinja2 templating syntax
- All dynamic templates extend `base.html`
- Authentication pages (login, register) are standalone

## Database Schema

### Users Table
- id, name, email, password, role (student/department/admin), created_at

### Complaints Table
- id, user_id, title, description, category, status, assigned_to, created_at, updated_at

### Replies Table
- id, complaint_id, user_id, reply_text, created_at

### Departments Table
- id, name, created_at

## API Routes

### Authentication
- `GET /` - Home/Login page
- `GET /register_page` - Registration page
- `POST /register` - Register new user
- `POST /login` - User login
- `GET /logout` - Logout user

### Student Routes
- `GET /dashboard` - View my complaints
- `POST /add` - Submit new complaint
- `GET /complaint/<id>` - View complaint details (JSON)

### Admin Routes
- `GET /admin` - View all complaints
- `POST /assign/<id>` - Assign complaint to department
- `GET /update/<id>/<status>` - Update complaint status

### Department Routes
- `GET /department` - View assigned complaints
- `GET /update/<id>/<status>` - Update complaint status
- `POST /reply/<id>` - Add reply to complaint

## Complaint Categories

1. **Academic** - Academic-related issues
2. **Hostel** - Hostel facility issues
3. **Administrative** - Administrative matters
4. **Infrastructure** - Infrastructure and maintenance
5. **Other** - Miscellaneous issues

## Status Flow

```
Pending → In Progress → Resolved
                    ↓
                  Rejected
```

## Color Scheme

- **Primary (Accent)**: #2d5a8e (Blue)
- **Success (Green)**: #2e7d52
- **Warning (Amber)**: #b7691a
- **Danger (Red)**: #c0392b
- **Text**: #1a1916
- **Background**: #f4f1eb

## Important Notes

⚠️ **Development Only**
- Debug mode is enabled in `app.py`
- Change `debug=True` to `debug=False` for production
- Update SECRET_KEY in config.py before deployment

🔐 **Security Recommendations**
- Use environment variables for secrets
- Implement HTTPS in production
- Add CSRF protection
- Implement rate limiting on login

## Customization

### Add New Complaint Category
Edit the enum in `database/schema.sql`:
```sql
category ENUM('academic', 'hostel', 'admin', 'infrastructure', 'other', 'new_category')
```

### Modify Color Scheme
Edit CSS variables in `static/css/style.css`:
```css
:root {
  --accent: #your-color;
  /* ... other variables ... */
}
```

## Troubleshooting

### Database Connection Error
- Check MySQL is running
- Verify credentials in `config.py`
- Ensure database exists

### Template Not Found
- Check file naming in `templates/` folder
- Verify template paths in routes

### Styling Issues
- Clear browser cache
- Check `static/css/style.css` is linked correctly
- Verify CSS file permissions

## Support & Contribution

For issues or suggestions, please create an issue in the repository.

## License

MIT License - See LICENSE file for details.

---

Built with ❤️ using Flask and MySQL

