# Sip&Match

A collaborative cocktail discovery web application built with **Flask, MongoDB, and external APIs**, combining cocktail search, personalised recommendations, bar discovery, and social features.

> **Collaborative university project developed at Vrije Universiteit Amsterdam.**

## Overview

**Sip&Match** is a web application designed to help users discover cocktails based on their preferences and explore what other users are drinking.

The application combines several features into one platform:

- 🔎 **Cocktail Search** — Search cocktails by name or ingredient
- 🍸 **Cocktail Creator** — Generate cocktail ideas based on selected ingredients and taste preferences
- 📍 **Bar Finder** — Discover nearby bars using location-based search
- ⭐ **Cocktail of the Day** — Receive a new cocktail recommendation
- 🔥 **Trending Cocktails** — Explore popular cocktail choices
- 👥 **Social Feed** — Create posts, share drinks, and interact with other users
- 👤 **User Accounts** — Register and manage user accounts

## Installation & Setup

### 1. Clone the repository

```
git clone https://github.com/patrycjabeder-rgb/cocktail-api-app.git
cd cocktail-api-app
```

### 2. Create and activate a virtual environment

**Windows**

```
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r backend/requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```
MONGO_URI=<your_mongodb_atlas_connection_string>
SERPAPI_API_KEY=<your_serpapi_key>
```

### 5. Import cocktail data

Populate the MongoDB cocktail collection using TheCocktailDB API:

```
python backend/import_cocktails.py
```

### 6. Start the backend

```
python backend/src/app.py
```

The API will be available at:

```
http://127.0.0.1:5000
```

### 7. Open the frontend

Open the frontend HTML file in a browser to interact with the application.

The application follows a **client-server architecture**.

```text
┌─────────────────────┐
│      Frontend       │
│   HTML / CSS / JS   │
└──────────┬──────────┘
           │ HTTP requests
           ▼
┌─────────────────────┐
│       Flask         │
│     REST API        │
└──────┬────────┬─────┘
       │        │
       ▼        ▼
┌──────────┐  ┌─────────────────┐
│ MongoDB  │  │  External APIs  │
│  Atlas   │  │ CocktailDB      │
│          │  │ SerpAPI         │
└──────────┘  └─────────────────┘

```
### Frontend

The frontend provides the user interface for:

- User registration and login
- Cocktail search
- Ingredient-based search
- Cocktail details
- Social features
- Cocktail discovery

The frontend communicates with the backend through HTTP requests to REST API endpoints.

### Backend

The backend is implemented using **Python and Flask**.

The application is organized into routes and services. Routes handle HTTP requests and responses, while services contain the underlying application logic.

The backend includes functionality for:

- Cocktail search
- User account management
- Social feed functionality
- Bar discovery
- Cocktail recommendations
- Database interaction

### Database

**MongoDB Atlas** is used as the application's database and is accessed through **PyMongo**.

The database contains collections for:

- `users`
- `cocktails`
- `posts`
- `follows`

### External APIs

The application integrates with external services including:

- **TheCocktailDB API** — cocktail data and information
- **SerpAPI** — bar discovery functionality

## Testing

The backend includes automated tests using **pytest** to test application functionality and user-account behaviour.

## My Contribution

This was a **collaborative project** developed as part of a university group assignment.

I contributed to the development of the application across the backend and application functionality, working collaboratively with the other team members on the implementation and integration of the different components.

## Technologies

### Programming & Frameworks

- Python
- Flask
- HTML
- CSS
- JavaScript

### Database

- MongoDB
- PyMongo

### APIs & Tools

- TheCocktailDB API
- SerpAPI
- REST APIs
- Git
- GitHub
- pytest

## Project Structure

```text
cocktail-api-app/
├── backend/
│   ├── src/
│   ├── tests/
│   ├── app.py
│   ├── import_cocktails.py
│   └── requirements.txt
├── frontend/
│   └── templates/
├── .gitignore
└── README.md
```
## Academic Context

This project was developed collaboratively as part of an **Artificial Intelligence university course at Vrije Universiteit Amsterdam**.

The project combines web development, REST APIs, database management, external API integration, and automated testing into a single application.