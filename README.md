# MapFameLocation API

A Django REST Framework API for managing locations and feedback with user authentication.

## Features

- **User Authentication**: Registration, login, logout, and password reset
- **Location Management**: Create, read, update, and delete locations with categories
- **Feedback System**: Users can leave feedback with ratings (1-5 stars) and comments
- **Rating System**: Automatic calculation of average ratings for locations
- **Filtering & Search**: Filter locations by rating and category, search by name
- **Pagination**: Built-in pagination for list views
- **Permissions**: Users can only modify their own feedbacks
- **Email Notifications**: Subscribed users receive email notifications for new feedbacks

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd MapFameLocation
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from `.env.example`:
```bash
cp .env.example .env
```

5. Update `.env` with your configuration:
- Database credentials
- Email settings (for password reset and notifications)
- Secret key (generate a new one for production)

6. Run migrations:
```bash
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Users

- `POST /users/register/` - Register a new user
- `POST /users/login/` - Login (creates session)
- `POST /users/logout/` - Logout
- `GET /users/protected/` - Test protected endpoint
- `POST /users/subscribe/` - Toggle subscription status (authenticated users only)

#### Password Reset

- `POST /users/password_reset/` - Request password reset email
- `GET /users/password_reset/done/` - Password reset email sent confirmation
- `GET /users/reset/<uidb64>/<token>/` - Password reset confirmation page
- `GET /users/reset/done/` - Password reset complete

### Locations

- `GET /locations/locations/` - List all locations (with search: `?name=<query>`)
- `POST /locations/locations/` - Create a new location (authenticated users only)
- `GET /locations/locations/<id>/` - Get location details
- `PUT /locations/locations/<id>/` - Update location (authenticated users only)
- `PATCH /locations/locations/<id>/` - Partially update location (authenticated users only)
- `DELETE /locations/locations/<id>/` - Delete location (authenticated users only)
- `GET /locations/detail-location/<location_id>/` - Get location with all feedbacks
- `GET /locations/filter-rating/<rating>/` - Filter locations by minimum rating (1-5)
- `GET /locations/filter-category/?category=<category>` - Filter locations by category
- `GET /locations/save_data/` - Export all data to CSV files (authenticated users only)

### Feedbacks

- `GET /feedbacks/feedback/` - List all feedbacks (with filter: `?location_id=<id>`)
- `POST /feedbacks/feedback/` - Create a new feedback (authenticated users only)
- `GET /feedbacks/feedback/<id>/` - Get feedback details
- `PUT /feedbacks/feedback/<id>/` - Update your feedback (owner only)
- `PATCH /feedbacks/feedback/<id>/` - Partially update your feedback (owner only)
- `DELETE /feedbacks/feedback/<id>/` - Delete your feedback (owner only)

### Admin

- `GET /admin/` - Django admin interface (superuser only)

## API Authentication

The API uses session-based authentication. After logging in, Django will set a session cookie that will be used for subsequent requests.

Alternatively, you can use Basic Authentication with username and password.

## Response Format

All API responses are in JSON format:

### Success Response
```json
{
  "id": 1,
  "name": "Location Name",
  "category": "Restaurant",
  "average_rating": 4.5,
  ...
}
```

### Error Response
```json
{
  "error": "Error message",
  "details": {...}
}
```

## Pagination

List endpoints support pagination. Response format:
```json
{
  "count": 100,
  "next": "http://example.com/api/endpoint/?page=2",
  "previous": null,
  "results": [...]
}
```

Default page size is 20 items. You can customize with `?page=<number>`.

## Models

### Location
- `id`: Primary key
- `name`: Location name (unique)
- `category`: Location category
- `average_rating`: Calculated average rating (0-5)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Feedback
- `id`: Primary key
- `user`: Foreign key to User
- `location`: Foreign key to Location
- `comments`: Feedback text
- `comments_like`: Like flag
- `comments_dislike`: Dislike flag
- `stars`: Rating (1-5)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### User
- Extends Django's AbstractUser
- `subscription`: Boolean flag for email notifications

## Development

### Running Tests
```bash
python manage.py test
```

### Database Reset
```bash
python manage.py flush
python manage.py migrate
```

## Security Notes

- Never commit `.env` file to version control
- Change the `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Use environment variables for all sensitive data
- Configure proper `ALLOWED_HOSTS` for production

## License

This project is provided as-is for educational purposes.

