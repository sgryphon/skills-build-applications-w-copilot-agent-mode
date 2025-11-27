# OctoFit Tracker Frontend

This project was created with React and connects to the Django REST API backend.

## Setup Instructions

### 1. Install Dependencies

```bash
npm install --prefix octofit-tracker/frontend
```

### 2. Configure Environment Variables

Create a `.env` file in the `frontend` directory:

```bash
cp octofit-tracker/frontend/.env.example octofit-tracker/frontend/.env
```

Edit the `.env` file and set your GitHub Codespace name:

```
REACT_APP_CODESPACE_NAME=your-codespace-name-here
```

**To find your codespace name:**
- Look at your current codespace URL
- Example: `https://musical-space-waddle-abc123-8000.app.github.dev`
- Your codespace name is: `musical-space-waddle-abc123`

### 3. Start the Backend

Make sure the Django backend is running on port 8000:

```bash
source octofit-tracker/backend/venv/bin/activate
python octofit-tracker/backend/manage.py runserver 0.0.0.0:8000
```

### 4. Start the Frontend

```bash
npm start --prefix octofit-tracker/frontend
```

The app will open at [http://localhost:3000](http://localhost:3000).

## Features

The frontend includes the following pages:

- **Home** - Welcome page with app overview
- **Activities** - View all logged fitness activities
- **Leaderboard** - See user rankings based on calories burned
- **Teams** - Browse and manage fitness teams
- **Users** - View all registered users
- **Workouts** - Browse personalized workout suggestions

## API Integration

All components connect to the Django REST API backend using:

```
https://${REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/[endpoint]/
```

Each component includes:
- Loading states
- Error handling
- Console logging for debugging
- Support for both paginated and plain array responses

## Available Scripts

### `npm start --prefix octofit-tracker/frontend`

Runs the app in development mode on port 3000.

### `npm test --prefix octofit-tracker/frontend`

Launches the test runner in interactive watch mode.

### `npm run build --prefix octofit-tracker/frontend`

Builds the app for production to the `build` folder.

## Troubleshooting

### API Connection Issues

1. Verify the backend is running on port 8000
2. Check that `REACT_APP_CODESPACE_NAME` is set correctly in `.env`
3. Open browser console to see detailed API logs
4. Ensure port 8000 is set to public visibility in Codespaces

### CORS Errors

Make sure `django-cors-headers` is properly configured in the Django backend settings.
