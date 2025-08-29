# Sustainability Actions Tracker

A full-stack application built with Django REST Framework backend and React frontend to track and manage sustainability actions. Features comprehensive API testing with integrated Postman collections, automated validation, and multi-environment support.

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

### API Testing & Documentation
- **Automated Postman Integration**: Complete collection with one-command setup
- **Comprehensive Test Coverage**: Built-in validation for all endpoints and error scenarios
- **Multi-Environment Support**: Separate configurations for development and production
- **CLI Testing**: Newman integration for automated testing and CI/CD
- **Documentation Generation**: Auto-generated HTML API documentation
- **Error Scenario Testing**: Validation of 404, 400, and edge cases

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

### API Testing
- Postman Collections with automated tests
- Newman CLI for headless testing
- Environment-specific configurations
- Comprehensive error scenario coverage

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
├── postman/                    # Postman integration files
│   ├── Sustainability_Actions_API.postman_collection.json
│   ├── Development.postman_environment.json
│   └── Production.postman_environment.json
├── scripts/                    # Automation scripts
│   ├── setup_postman.py       # Full automation script (requires Node.js)
│   ├── setup_postman.sh       # Shell setup script  
│   └── validate_postman.py    # Collection validator (no dependencies)
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

#### Automated Setup (Recommended)

**Quick Setup:**
```bash
# Full automation (requires Node.js)
bash scripts/setup_postman.sh

# Python script with Node.js detection
python scripts/setup_postman.py --setup-all

# No Node.js? No problem! Validate collections only
python scripts/validate_postman.py
```

**Manual Import:**
1. **Import Collection:** `postman/Sustainability_Actions_API.postman_collection.json`
2. **Import Environment:** `postman/Development.postman_environment.json`
3. **Select Environment:** Choose "Development Environment" in Postman
4. **Start Django Server:** `python manage.py runserver`
5. **Run Collection:** Use the collection runner or individual requests

#### Features Included

✅ **Complete API Coverage:** All CRUD endpoints with proper HTTP methods  
✅ **Automated Tests:** Built-in test scripts for validation and error handling  
✅ **Environment Variables:** Separate configs for Development and Production  
✅ **Dynamic Data:** Auto-generated timestamps and IDs  
✅ **Error Scenarios:** Tests for 404, 400, and validation errors  
✅ **Documentation:** Self-documenting requests with descriptions  

#### CLI Testing with Newman

```bash
# Install Newman (if not already installed)
npm install -g newman

# Run all tests
newman run postman/Sustainability_Actions_API.postman_collection.json \
  -e postman/Development.postman_environment.json

# Generate HTML report
newman run postman/Sustainability_Actions_API.postman_collection.json \
  -e postman/Development.postman_environment.json \
  --reporters htmlextra \
  --reporter-htmlextra-export postman/test-report.html
```

#### Available Endpoints

- **GET** `{{baseUrl}}/api/actions/` - Get all actions
- **POST** `{{baseUrl}}/api/actions/` - Create new action  
- **GET** `{{baseUrl}}/api/actions/{{actionId}}/` - Get specific action
- **PUT** `{{baseUrl}}/api/actions/{{actionId}}/` - Update action (full)
- **PATCH** `{{baseUrl}}/api/actions/{{actionId}}/` - Update action (partial)
- **DELETE** `{{baseUrl}}/api/actions/{{actionId}}/` - Delete action

#### Request Examples

**Create Action:**
```json
{
  "action": "Solar Panel Installation",
  "date": "{{timestamp}}",
  "points": 100
}
```

**Update Action (PATCH):**
```json
{
  "points": 150
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

### API Testing & Automation
- **Postman Collections**: Comprehensive test coverage for all endpoints
- **Automated Validation**: Built-in tests for response validation and error handling
- **Environment Management**: Development and production environment configurations
- **Newman CLI Integration**: Headless testing for CI/CD pipelines
- **Documentation Generation**: Auto-generated API documentation from collections
- **Error Scenario Coverage**: Tests for 404, 400, validation errors, and edge cases

## Testing

### Automated API Testing (Recommended)
Use the integrated Postman collections for comprehensive testing:

```bash
# Quick setup and testing
bash scripts/setup_postman.sh --test

# Run tests with Newman CLI
newman run postman/Sustainability_Actions_API.postman_collection.json \
  -e postman/Development.postman_environment.json

# Generate detailed HTML test report
newman run postman/Sustainability_Actions_API.postman_collection.json \
  -e postman/Development.postman_environment.json \
  --reporters htmlextra \
  --reporter-htmlextra-export postman/test-report.html
```

### Backend Testing
- **Postman Collection**: Import and run the comprehensive collection
- **Newman CLI**: Automated testing for CI/CD integration
- **Manual Testing**: Use cURL commands as shown in the API examples above

### Frontend Testing
1. Start both backend and frontend servers
2. Open `http://localhost:3000` in your browser
3. Test all CRUD operations through the UI:
   - Add new actions using the form
   - View actions in the table
   - Edit actions by clicking the Edit button
   - Delete actions by clicking the Delete button

### Test Coverage
✅ All CRUD operations (Create, Read, Update, Delete)  
✅ Data validation and error handling  
✅ Response time and performance testing  
✅ Error scenarios (404, 400, validation errors)  
✅ Environment-specific configurations  
✅ Automated test reporting

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