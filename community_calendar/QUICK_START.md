# Community Calendar - Quick Start Guide

## 🎉 Application Successfully Built!

Your community calendar social network application has been successfully created and is ready to use!

## 📍 Location

The application is located at:
```
/home/user/cookiecutter-flask/community_calendar/
```

## 🚀 Quick Start (3 Steps)

### 1. Navigate to the application
```bash
cd /home/user/cookiecutter-flask/community_calendar
```

### 2. Run the application
```bash
flask run
```

### 3. Open in browser
Navigate to: `http://localhost:5000`

## 👤 Test Users

Two test users have been created for you:

**Admin User:**
- Username: `admin`
- Password: `admin123`
- Can edit and delete any events

**Regular User:**
- Username: `testuser`
- Password: `test123`
- Can create events and posts

## ✨ What You Can Do

### Timeline (`/events/timeline`)
- ✍️ Create posts to share with the community
- 📅 Create events that appear on both timeline and calendar
- 💬 Comment on posts
- 👥 See profile pictures and user information

### Calendar (`/events/calendar`)
- 📆 View events in an interactive calendar
- 🔄 Switch between month, week, and day views
- 👆 Click events to see details, original post, and comments
- ✏️ Create and edit events (admins can edit any event)

### Profile (`/users/profile`)
- 🖼️ Upload a profile picture
- ✏️ Edit your name and email
- 👀 View your information

## 🏗️ What's Included

### Features
- ✅ User authentication (login, register, logout)
- ✅ Admin and regular user roles
- ✅ Facebook-like timeline for posts
- ✅ FullCalendar integration for calendar view
- ✅ Event creation with automatic timeline posts
- ✅ Commenting system
- ✅ Profile image uploads
- ✅ Responsive Bootstrap 5 design

### Technology
- 🐍 Python Flask 3.1.1
- 🗄️ SQLAlchemy + SQLite database
- 🔐 Flask-Login authentication
- 📝 Flask-WTF forms
- 🎨 Bootstrap 5 + Font Awesome 6
- 📅 FullCalendar.js
- 📦 Webpack for asset bundling

### Database Models
- 👤 User (with profile images and admin flag)
- 📅 Event (title, description, dates, location)
- 📝 Post (timeline posts linked to events)
- 💬 Comment (comments on posts)

## 📖 Full Documentation

For complete documentation, see:
- `COMMUNITY_CALENDAR_README.md` - Full documentation
- `README.md` - Original cookiecutter-flask README

## 🔧 Development Commands

```bash
# Run the application
flask run

# Run tests
flask test

# Create database migration
flask db migrate -m "Description"

# Apply database migration
flask db upgrade

# Build frontend assets
npm run build

# Watch for frontend changes
npm run watch

# Lint code
flask lint
```

## 🌐 Deployment

### Google App Engine
Ready to deploy to Google App Engine! See the deployment section in `COMMUNITY_CALENDAR_README.md` for detailed instructions.

## 📂 Project Structure

```
community_calendar/
├── community_calendar/          # Main app
│   ├── events/                  # Events, timeline, calendar
│   ├── user/                    # User management
│   ├── public/                  # Public pages
│   ├── templates/               # HTML templates
│   └── static/                  # CSS, JS, uploads
├── migrations/                  # Database migrations
├── tests/                       # Test suite
└── assets/                      # Frontend source
```

## 🎯 Next Steps

1. **Try it out**: Log in and create some events!
2. **Customize**: Modify colors, styles, and branding
3. **Deploy**: Deploy to Google App Engine or your preferred platform
4. **Enhance**: Add features like email notifications, recurring events, etc.

## 💡 Tips

- **Events**: Created events automatically generate timeline posts
- **Comments**: All posts can be commented on
- **Modal View**: Click calendar events to see the full post with comments
- **Admin Powers**: Admin users can edit/delete any event
- **Profile Pictures**: Supported formats: JPG, JPEG, PNG, GIF

## 🐛 Troubleshooting

### Reset Database
```bash
rm /tmp/dev.db
flask db upgrade
python create_test_users.py
```

### Rebuild Assets
```bash
npm run build
```

### Reinstall Dependencies
```bash
pip install -r requirements.txt
npm install
```

## 📞 Support

If you encounter issues:
1. Check `COMMUNITY_CALENDAR_README.md` for detailed documentation
2. Review error messages in the console
3. Check that all dependencies are installed

---

**Happy calendaring! 🎊**

Built with ❤️ using Flask and FullCalendar
