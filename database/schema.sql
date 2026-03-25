-- Create Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('student', 'department', 'admin') NOT NULL DEFAULT 'student',
    department VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Complaints Table
CREATE TABLE IF NOT EXISTS complaints (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category ENUM('academic', 'hostel', 'admin', 'infrastructure', 'other') NOT NULL DEFAULT 'other',
    status ENUM('pending', 'in_progress', 'resolved', 'rejected') NOT NULL DEFAULT 'pending',
    assigned_to VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create Replies Table
CREATE TABLE IF NOT EXISTS replies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    complaint_id INT NOT NULL,
    user_id INT NOT NULL,
    reply_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (complaint_id) REFERENCES complaints(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create Departments Table
CREATE TABLE IF NOT EXISTS departments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample Departments
INSERT INTO departments (name) VALUES ('Academic Affairs'), ('Hostel Management'), ('Administration'), ('Infrastructure'), ('Other') ON DUPLICATE KEY UPDATE id=id;

-- Default Admin User
INSERT INTO users (name, email, password, role) VALUES ('Admin', 'admin@example.com', 'scrypt:32768:8:1$1byjShDGxAUAugxX$9fde282506cef11f5397e56673f34eb0e3f31728668fe181b78d369eddf5e467206a8e8d01b299035ba48f5ff07ae31e628f7dc1db6634c6f2cad666a6e503c3', 'admin') ON DUPLICATE KEY UPDATE id=id;

