"""Create test users for the application."""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from community_calendar.app import create_app
from community_calendar.extensions import db
from community_calendar.user.models import User

app = create_app()

with app.app_context():
    # Create admin user
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            is_admin=True,
            active=True
        )
        admin.password = 'admin123'
        admin.save()
        print('Created admin user: admin/admin123')
    else:
        print('Admin user already exists')

    # Create regular user
    user = User.query.filter_by(username='testuser').first()
    if not user:
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            is_admin=False,
            active=True
        )
        user.password = 'test123'
        user.save()
        print('Created test user: testuser/test123')
    else:
        print('Test user already exists')

    print('\nTest users created successfully!')
    print('You can now log in with:')
    print('  - Admin: admin / admin123')
    print('  - Regular user: testuser / test123')
