# EduLearn - Student Learning Platform

A comprehensive web-based learning platform built with Flask that allows students to access lectures, notes, and educational content. Instructors can create and manage courses with rich multimedia content.

## 🚀 Features

### For Students
- **User Registration & Authentication**: Secure login system with user accounts
- **Course Discovery**: Browse available courses with detailed descriptions
- **Lecture Access**: View and access course lectures and materials
- **Study Notes**: Download and access supplementary study materials
- **Progress Tracking**: Monitor learning progress across courses
- **Responsive Design**: Mobile-friendly interface for learning anywhere

### For Instructors
- **Course Creation**: Create comprehensive courses with detailed information
- **Content Management**: Upload lectures, notes, and educational materials
- **Student Management**: Track student enrollment and progress
- **Course Analytics**: Monitor course performance and engagement

### Technical Features
- **Modern UI/UX**: Beautiful, responsive design with Bootstrap 5
- **Database Management**: SQLite database with SQLAlchemy ORM
- **File Upload System**: Support for various file types (PDFs, videos, documents)
- **Security**: Password hashing, user authentication, and session management
- **Scalable Architecture**: Modular Flask application structure

## 🛠️ Technology Stack

- **Backend**: Python 3.8+, Flask 2.3.3
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5.3
- **Authentication**: Flask-Login for user management
- **Forms**: Flask-WTF for form handling and validation
- **File Handling**: Werkzeug for secure file uploads
- **Icons**: Font Awesome 6.4.0

## 📋 Prerequisites

Before running this application, make sure you have:

- Python 3.8 or higher installed
- pip (Python package installer)
- A modern web browser
- Git (for cloning the repository)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd ET617_Web_Based_System
```

### 2. Create Virtual Environment (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
Create a `.env` file in the project root (optional):
```env
FLASK_APP=main.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-here
```

### 5. Run the Application
```bash
python main.py
```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
ET617_Web_Based_System/
├── main.py                 # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── templates/             # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Homepage
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── course_detail.html # Course detail view
│   └── create_course.html # Course creation form
├── static/                # Static files (CSS, JS, images)
│   ├── css/              # Stylesheets
│   └── js/               # JavaScript files
└── uploads/               # File upload directory
```

## 🗄️ Database Models

### User
- Basic user information (username, email, password)
- Role-based access (student/instructor)
- Account creation timestamp

### Course
- Course details (title, description, category)
- Instructor relationship
- Creation and modification timestamps

### Lecture
- Lecture content and metadata
- File attachments support
- Course relationship

### Note
- Study materials and supplementary content
- File download capabilities
- Course association

## 🔐 User Roles & Permissions

### Students
- Register and create accounts
- Browse available courses
- Access course content (lectures, notes)
- Track learning progress

### Instructors
- All student permissions
- Create and manage courses
- Upload course materials
- Monitor student engagement

## 🎨 Customization

### Styling
The application uses Bootstrap 5 with custom CSS. You can customize:
- Color scheme in `base.html`
- Layout and spacing
- Component styling

### Adding New Features
- **New Routes**: Add to `main.py`
- **New Templates**: Create in `templates/` directory
- **Database Changes**: Modify models in `main.py`
- **Static Files**: Add to `static/` directory

## 📱 Responsive Design

The platform is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- All modern web browsers

## 🔒 Security Features

- **Password Hashing**: Secure password storage using Werkzeug
- **User Authentication**: Flask-Login session management
- **Form Validation**: CSRF protection and input validation
- **File Upload Security**: Secure filename handling
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production Deployment
For production deployment, consider:
- Using a production WSGI server (Gunicorn, uWSGI)
- Setting up a reverse proxy (Nginx, Apache)
- Using a production database (PostgreSQL, MySQL)
- Setting up SSL/TLS certificates
- Configuring environment variables

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Errors**: Delete `learning_platform.db` and restart
   ```bash
   rm learning_platform.db
   python main.py
   ```

3. **Port Already in Use**: Change the port in `main.py`
   ```python
   app.run(debug=True, port=5001)
   ```

4. **Template Errors**: Ensure all HTML files are in the `templates/` directory

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section
2. Review the Flask documentation
3. Create an issue in the repository
4. Contact the development team

## 🔮 Future Enhancements

- **Video Streaming**: Integrated video player for lectures
- **Interactive Quizzes**: Built-in assessment system
- **Discussion Forums**: Student-instructor communication
- **Progress Analytics**: Detailed learning analytics
- **Mobile App**: Native mobile application
- **Payment Integration**: Course monetization features
- **Multi-language Support**: Internationalization
- **Advanced Search**: Course and content search functionality

---

**Happy Learning! 🎓**

Built with ❤️ using Flask and modern web technologies.