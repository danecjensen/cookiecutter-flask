# Community Calendar - Social Network Application

A Flask-based social network application for small communities to build and maintain monthly calendars together. This application combines timeline-based social interactions with an integrated calendar view.

## Features

### 🔐 User Management
- **User Authentication**: Register, login, and logout functionality
- **User Roles**: Admin and regular user roles
- **Profile Management**: Users can edit their profiles and upload profile images
- **Profile Images**: Support for JPG, JPEG, PNG, and GIF formats

### 📱 Timeline UI
- **Facebook-like Timeline**: Post updates and events to a community timeline
- **Event Posts**: Create events that automatically generate timeline posts
- **Comments**: Comment on any timeline post
- **User Avatars**: Profile images displayed throughout the timeline
- **Rich Post Display**: Posts show event details, user information, and timestamps

### 📅 Calendar UI
- **FullCalendar Integration**: Interactive calendar with month, week, and day views
- **Event Details Modal**: Click any event to view:
  - Event information (title, description, date, time, location)
  - Original timeline post
  - All comments on the post
- **Event Management**: Create, edit, and delete events
- **Admin Controls**: Admins can edit any event

## Technology Stack

- **Backend**: Python Flask 3.1.1
- **Database**: SQLAlchemy with SQLite (easily swappable to PostgreSQL for production)
- **Authentication**: Flask-Login & Flask-Bcrypt
- **Forms**: Flask-WTF & WTForms
- **Frontend**: Bootstrap 5, Font Awesome 6, FullCalendar.js
- **Build Tools**: Webpack for asset bundling

## Database Models

### User
- Username, email, password (hashed)
- First name, last name, profile image
- Admin flag for elevated permissions

### Event
- Title, description, start/end dates, location
- Created by user (foreign key)
- Linked to timeline post

### Post
- Content, timestamps
- Created by user (foreign key)
- Optional link to event

### Comment
- Content, timestamp
- Created by user (foreign key)
- Links to specific post

## Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 20+
- pip and npm

### Step 1: Navigate to the Application Directory
```bash
cd community_calendar
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Install Node.js Dependencies
```bash
npm install
```

### Step 4: Build Frontend Assets
```bash
npm run build
```

### Step 5: Set Up Environment Variables
The application uses environment variables for configuration. The `.env` file is already configured for development:

```bash
FLASK_APP=autoapp.py
FLASK_DEBUG=1
FLASK_ENV=development
DATABASE_URL=sqlite:////tmp/dev.db
SECRET_KEY=not-so-secret
```

### Step 6: Initialize Database
Database migrations have already been created and applied. If you need to recreate the database:

```bash
export FLASK_APP=autoapp.py
flask db upgrade
```

### Step 7: Create Test Users
A script has been provided to create test users:

```bash
python create_test_users.py
```

This creates:
- **Admin User**: `admin` / `admin123`
- **Regular User**: `testuser` / `test123`

### Step 8: Run the Application
```bash
flask run
```

The application will be available at `http://localhost:5000`

## Usage Guide

### Getting Started
1. Navigate to `http://localhost:5000`
2. Log in with one of the test accounts:
   - Admin: `admin` / `admin123`
   - User: `testuser` / `test123`

### Creating Events
1. Click on **"Timeline"** in the navigation
2. Click **"Create Event"** button
3. Fill in event details:
   - Title (required)
   - Description (optional)
   - Start Date & Time (required)
   - End Date & Time (optional)
   - Location (optional)
4. Click **"Create Event"**
5. The event will appear on both the Timeline and Calendar

### Using the Timeline
- **Create Posts**: Type in the text box and click "Post"
- **Comment**: Click "Comment" on any post and add your thoughts
- **View Events**: Posts linked to events show event details with a link to the calendar

### Using the Calendar
1. Click on **"Calendar"** in the navigation
2. **View Modes**: Switch between Month, Week, and Day views
3. **Navigate**: Use prev/next buttons to navigate through time
4. **View Event Details**: Click any event to see:
   - Event information
   - Original timeline post
   - All comments
5. **Edit Events**: Admins can edit events by clicking "Edit Event" in the modal

### Profile Management
1. Click your username in the top-right corner
2. Select **"My Profile"**
3. Update your information:
   - First Name
   - Last Name
   - Email
   - Profile Image (upload JPG, PNG, or GIF)
4. Click **"Update Profile"**

## Project Structure

```
community_calendar/
├── community_calendar/          # Main application package
│   ├── events/                  # Events blueprint
│   │   ├── models.py           # Event, Post, Comment models
│   │   ├── views.py            # Timeline & calendar routes
│   │   └── forms.py            # Event, Post, Comment forms
│   ├── user/                    # User blueprint
│   │   ├── models.py           # User & Role models
│   │   ├── views.py            # User profile routes
│   │   └── forms.py            # Registration & profile forms
│   ├── public/                  # Public blueprint
│   │   ├── views.py            # Home, login, register routes
│   │   └── forms.py            # Login form
│   ├── templates/               # Jinja2 templates
│   │   ├── events/             # Timeline & calendar templates
│   │   ├── users/              # User profile templates
│   │   └── public/             # Public page templates
│   ├── static/                  # Static files (CSS, JS, images)
│   │   └── uploads/            # Uploaded profile images
│   ├── app.py                   # Application factory
│   ├── extensions.py            # Flask extensions
│   ├── database.py              # Database utilities
│   └── settings.py              # Configuration
├── assets/                      # Frontend source files
├── migrations/                  # Database migrations
├── tests/                       # Test suite
├── autoapp.py                   # Application entry point
├── requirements.txt             # Python dependencies
├── package.json                 # Node.js dependencies
└── webpack.config.js            # Webpack configuration
```

## API Endpoints

### Timeline & Events
- `GET /events/timeline` - View timeline
- `POST /events/timeline/post` - Create a post
- `POST /events/timeline/post/<id>/comment` - Add comment to post
- `GET /events/calendar` - View calendar
- `GET /events/create` - Create event form
- `POST /events/create` - Create event
- `GET /events/edit/<id>` - Edit event form (admin only)
- `POST /events/edit/<id>` - Update event (admin only)
- `POST /events/delete/<id>` - Delete event (admin only)

### API Endpoints for Calendar
- `GET /events/api/events` - Get all events (JSON)
- `GET /events/api/events/<id>` - Get single event with post & comments (JSON)

### User Management
- `GET /users/profile` - View/edit profile
- `POST /users/profile` - Update profile

## Deployment to Google App Engine

### Prerequisites
1. Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
2. Create a Google Cloud Project
3. Enable App Engine for your project

### Configuration for Production

1. **Update `app.yaml`** (create if it doesn't exist):
```yaml
runtime: python311

env_variables:
  FLASK_ENV: production
  SECRET_KEY: "your-secret-key-here"
  DATABASE_URL: "postgresql://user:password@/dbname?host=/cloudsql/project:region:instance"

handlers:
- url: /static
  static_dir: community_calendar/static

- url: /.*
  script: auto
```

2. **Update Database**: For production, use Cloud SQL (PostgreSQL)
   - Update `DATABASE_URL` in `app.yaml`
   - Install PostgreSQL driver: Already included (`psycopg2-binary`)

3. **Deploy**:
```bash
gcloud app deploy
```

## Development

### Running Tests
```bash
flask test
```

### Code Linting
```bash
flask lint
```

### Database Migrations
Create a new migration after model changes:
```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

### Building Assets
Watch for changes during development:
```bash
npm run watch
```

## Security Notes

⚠️ **Important for Production**:
1. Change `SECRET_KEY` in `.env` to a strong random value
2. Set `FLASK_DEBUG=0` in production
3. Use a production-grade database (PostgreSQL)
4. Configure proper file upload validation and limits
5. Set up HTTPS
6. Configure CORS if needed
7. Review and update security headers

## Troubleshooting

### Database Issues
If you encounter database errors:
```bash
# Reset the database
rm /tmp/dev.db
flask db upgrade
python create_test_users.py
```

### Asset Build Issues
If CSS/JS isn't loading:
```bash
# Rebuild assets
npm run build
```

### Import Errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
npm install
```

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Include error messages and steps to reproduce

## Future Enhancements

Potential features to add:
- Email notifications for events
- Event RSVP functionality
- Recurring events
- Event categories and filtering
- Search functionality
- Social sharing
- Mobile app
- Real-time updates with WebSockets
- File attachments on posts
- Event reminders
- Calendar export (iCal format)
- Integration with Google Calendar

---

**Built with Flask** | **Powered by FullCalendar** | **Styled with Bootstrap 5**
