# Sustainability Actions Tracker

A full-stack application built with Django REST Framework backend and React frontend to track and manage sustainability actions. Users can create, read, update, and delete sustainability actions with points and dates.

## Features

### Backend (Django REST API)
- **GET `/api/actions/`**: Retrieve all sustainability actions
- **POST `/api/actions/`**: Create a new sustainability action
- **GET `/api/actions/<id>/`**: Retrieve a specific action by ID
- **PUT/PATCH `/api/actions/<id>/`**: Update an existing action
- **DELETE `/api/actions/<id>/`**: Delete an action
- **JSON File Storage**: Actions are stored in a JSON file instead of a traditional database
- **Data Validation**: Proper validation for action data with error handling
- **CORS Support**: Configured for React frontend integration

### Frontend (React)
- **Action Display**: View all actions in a clean table format
- **Add Actions**: Form to add new sustainability actions
- **Edit Actions**: Click to edit existing actions inline
- **Delete Actions**: Remove actions with confirmation dialog
- **Responsive Design**: Works on desktop and mobile devices
- **Error Handling**: User-friendly error messages and loading states
- **Form Validation**: Client-side and server-side validation

## Tech Stack

### Backend
- Python 3.x
- Django 5.2.5
- Django REST Framework 3.16.1
- Django CORS Headers 4.7.0

### Frontend
- React 18
- Axios for API calls
- CSS3 for styling
- Functional components with React Hooks

## Project Structure

```
Django_API/
├── sustainability_api/          # Django project settings
│   ├── settings.py             # Main settings with CORS configuration
│   ├── urls.py                 # URL routing
│   └── ...
├── actions/                    # Django app for sustainability actions
│   ├── models.py               # Action model with JSON file storage
│   ├── serializers.py          # DRF serializers
│   ├── views.py                # API views
│   └── urls.py                 # App URL patterns
├── frontend/                   # React application
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── ActionsList.js  # Display actions table
│   │   │   └── ActionForm.js   # Add/edit form
│   │   ├── services/
│   │   │   └── api.js          # Axios API service
│   │   ├── App.js              # Main App component
│   │   └── App.css             # Styling
│   └── ...
├── venv/                       # Python virtual environment
├── actions_data.json           # JSON file for data storage
└── README.md                   # This file
```

## Installation & Setup

### Backend Setup

1. **Clone the repository and navigate to the project directory:**
   ```bash
   cd Django_API
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # source venv/bin/activate    # On macOS/Linux
   ```

3. **Install Python dependencies:**
   ```bash
   pip install django djangorestframework django-cors-headers
   ```

4. **Start the Django development server:**
   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://localhost:8000/api/actions/`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the React development server:**
   ```bash
   npm start
   ```

   The React app will be available at `http://localhost:3000`

## API Usage Examples

### Using cURL

1. **Get all actions:**
   ```bash
   curl -X GET "http://localhost:8000/api/actions/"
   ```

2. **Create a new action:**
   ```bash
   curl -X POST "http://localhost:8000/api/actions/" \
        -H "Content-Type: application/json" \
        -d '{"action": "Recycling", "date": "2025-01-08", "points": 25}'
   ```

3. **Update an action:**
   ```bash
   curl -X PUT "http://localhost:8000/api/actions/1/" \
        -H "Content-Type: application/json" \
        -d '{"action": "Solar Panel Installation", "date": "2025-01-08", "points": 100}'
   ```

4. **Delete an action:**
   ```bash
   curl -X DELETE "http://localhost:8000/api/actions/1/"
   ```

### Using Postman

Import the following endpoints into Postman:

- **GET** `http://localhost:8000/api/actions/`
- **POST** `http://localhost:8000/api/actions/`
- **GET** `http://localhost:8000/api/actions/{id}/`
- **PUT** `http://localhost:8000/api/actions/{id}/`
- **DELETE** `http://localhost:8000/api/actions/{id}/`

For POST/PUT requests, use JSON body:
```json
{
  "action": "Action Name",
  "date": "YYYY-MM-DD",
  "points": 25
}
```

## Data Model

Each sustainability action has the following fields:

| Field  | Type    | Description                    | Constraints                   |
|--------|---------|--------------------------------|-------------------------------|
| id     | Integer | Auto-generated unique ID       | Primary key, read-only        |
| action | String  | Name of the sustainability action | Required, max 255 characters |
| date   | Date    | Date of the action             | Required, cannot be in future |
| points | Integer | Points earned for the action   | Required, must be positive    |

## Error Handling

The API returns appropriate HTTP status codes:

- **200 OK**: Successful GET/PUT requests
- **201 Created**: Successful POST requests
- **204 No Content**: Successful DELETE requests
- **400 Bad Request**: Invalid data or validation errors
- **404 Not Found**: Action not found
- **500 Internal Server Error**: Server errors

## Development Features

### Code Quality
- Clean, readable code with meaningful variable names
- Proper separation of concerns
- RESTful API design principles
- Comprehensive error handling
- Input validation on both client and server

### React Best Practices
- Functional components with hooks
- Proper state management with useState and useEffect
- Component reusability
- Responsive CSS design
- User experience considerations (loading states, confirmations)

## Testing

### Backend Testing
Test the API endpoints using cURL or Postman as shown in the examples above.

### Frontend Testing
1. Start both backend and frontend servers
2. Open `http://localhost:3000` in your browser
3. Test all CRUD operations through the UI:
   - Add new actions using the form
   - View actions in the table
   - Edit actions by clicking the Edit button
   - Delete actions by clicking the Delete button

## Production Considerations

For production deployment, consider:

1. **Security**: Change Django's SECRET_KEY and set DEBUG=False
2. **Database**: Replace JSON file storage with a proper database (PostgreSQL, MySQL)
3. **Static Files**: Configure proper static file serving
4. **Environment Variables**: Use environment variables for sensitive configuration
5. **HTTPS**: Enable HTTPS for secure communication
6. **Docker**: Containerize the application for easier deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is created for educational purposes and is open source.