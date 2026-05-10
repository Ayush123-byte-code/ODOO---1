# Traveloop Backend

Flask-based REST API backend with SQLite database for the Traveloop travel planning application.

## Quick Start

### Option 1: Using run.py (Recommended)
```bash
cd backend
python run.py
```
This will automatically install dependencies and start the server.

### Option 2: Manual Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

## Default Credentials

**Admin User:**
- Email: `admin@traveloop.com`
- Password: `admin123`

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | Register new user |
| POST | `/api/auth/login` | Login user |
| POST | `/api/auth/logout` | Logout user |
| GET | `/api/auth/me` | Get current user |

### User Profile
| Method | Endpoint | Description |
|--------|----------|-------------|
| PUT | `/api/users/profile` | Update profile |
| PUT | `/api/users/password` | Change password |

### Trips
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/trips` | Get all trips |
| GET | `/api/trips/:id` | Get trip details |
| POST | `/api/trips` | Create trip |
| PUT | `/api/trips/:id` | Update trip |
| DELETE | `/api/trips/:id` | Delete trip |

### Stops (Destinations)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/trips/:id/stops` | Get trip stops |
| POST | `/api/trips/:id/stops` | Add stop |
| PUT | `/api/stops/:id` | Update stop |
| DELETE | `/api/stops/:id` | Delete stop |

### Activities
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/stops/:id/activities` | Add activity |
| PUT | `/api/activities/:id` | Update activity |
| DELETE | `/api/activities/:id` | Delete activity |

### Budget
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/trips/:id/budget` | Get budget items |
| POST | `/api/trips/:id/budget` | Add budget item |
| DELETE | `/api/budget/:id` | Delete budget item |

### Packing List
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/trips/:id/packing` | Get packing list |
| POST | `/api/trips/:id/packing` | Add packing item |
| PUT | `/api/packing/:id` | Update item |
| DELETE | `/api/packing/:id` | Delete item |

### Notes/Journal
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/trips/:id/notes` | Get notes |
| POST | `/api/trips/:id/notes` | Create note |
| PUT | `/api/notes/:id` | Update note |
| DELETE | `/api/notes/:id` | Delete note |

### Saved Destinations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/destinations/saved` | Get saved |
| POST | `/api/destinations/saved` | Save destination |
| DELETE | `/api/destinations/saved/:id` | Remove saved |

### Search
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/search/cities` | Search cities |
| GET | `/api/search/activities` | Search activities |

### Public/Shared
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/trips/shared/:code` | Get shared trip |
| POST | `/api/trips/:id/copy` | Copy public trip |

### Admin (Admin Only)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin/stats` | Get statistics |
| GET | `/api/admin/users` | Get all users |
| DELETE | `/api/admin/users/:id` | Delete user |

## Database Schema

The SQLite database (`traveloop.db`) contains:

- **users** - User accounts and profiles
- **sessions** - Authentication sessions
- **trips** - Travel trips
- **stops** - Destinations/stops within trips
- **activities** - Activities at each stop
- **budget_items** - Budget/expense tracking
- **packing_items** - Packing checklist
- **notes** - Trip notes/journal entries
- **saved_destinations** - User's saved destinations
- **collaborators** - Trip sharing/collaboration

## Authentication

The API uses token-based authentication:

1. Login/Signup returns a `token`
2. Include token in requests: `Authorization: Bearer <token>`
3. Tokens expire after 7 days

## CORS

CORS is enabled for all origins to support local frontend development.

## Error Handling

All endpoints return JSON with consistent error format:
```json
{
    "error": "Error message here"
}
```

HTTP Status Codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error
