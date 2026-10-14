# Project Title
// IMAGE OF THE REAL FRONTEND
## Brief description of the project
Sip&Match is a cocktail web application with multiple features, designed to help you search for cocktails and bars in your area, filtering by city, rating, custom search, and price range. You can also create a user account and upload pictres of your drinks, post them on your feed, see what other people are drinking and posting, and what they think about the cocktails they had. From the captions, you can find out if they enjoyed the taste of their drink, or if they would not reccommend sipping that cocktail. Another feature is the cocktail of the day, suggesting some new cocktails worth trying. The cocktail creator feature allows you to add ingredients you like and receive an interesting cocktail recipe that suits your flavour and taste profile. If you are searching for inspiration, you can also check out the trending cocktails tab.
## Frontend mockup
// TBA
## Team members
Nikola Andonov, Patrycja Beder, Hana Grigoriu, Rida el Harchaoui

## Installation details
### 1. Clone the repository 
    git clone <repository-url>
### 2. Create and activate a virtual environment
Windows

    python -m venv venv
    venv\Scripts\activate
Mac/Linux
    
    python3 -m venv venv
    source venv/bin/activate
### 3. Install dependencies
    pip install -r requirements.txt
### 4. Create a .env file
Create a '.env' file in the project root and add:
    
    MONGO_URI=<your_mongodb_atlas_connection_string>
    SERPAPI_API_KEY=<your_serpapi_key>
### 5. Import cocktail data (first-time setup)

Import cocktail data from the free CocktailDB API into your MongoDB collection.
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
### 7. Start the frontend
Open the frontend HTML file in a browser.

## Architecture
The application follows a client-server architecture.

### Frontend

The frontend is implemented using HTML, CSS, and JavaScript. It provides the user interface for:

- User registration and login
- Searching cocktails by name
- Searching cocktails by ingredient(s)
- Viewing cocktail details
- Interacting with social features

The frontend communicates with the backend through HTTP requests to REST API endpoints.

### Backend

The backend is implemented using Flask and organized into routes and services.

Routes are responsible for:
- Handling HTTP requests
- Validating input
- Returning JSON responses

Services contain the application logic, such as:
- User account management
- Cocktail search functionality
- Feed functionality
- Bar finder functionality
- Cocktail of the day generation

### Database

MongoDB Atlas is used as the database.

Collections include:

- `users` – user account information
- `cocktails` – cocktail data imported from TheCocktailDB
- `posts` – user-generated posts
- `follows` – user follow relationships

MongoDB is accessed through PyMongo.

### External APIs

The application integrates with external services:

- TheCocktailDB API (used to request cocktail data)
- SerpAPI (used for bar finder functionality)

### Data Flow

1. User interacts with the frontend.
2. The frontend sends an HTTP request to a Flask endpoint.
3. The backend service processes the request.
4. Data is retrieved from MongoDB or an external API.
5. The backend returns a JSON response.
6. The frontend displays the results to the user.

### Files description 
- **db.py** – Creates the MongoDB connection and provides access to database collections.
- **search_cocktails.py** – Flask routes for cocktail search endpoints.
- **search_cocktail_service.py** – Functions for searching cocktails by name, ingredient, multiple ingredients, and ID.
- **user_accounts.py** – Flask routes for user account management.
- **user_account_service.py** – Handles account creation, login, deletion, and password change.
- **feed.py** – Routes related to the social feed.
- **feed_service.py** – Functions for creating and retrieving posts.
- **bar_finder.py** – Routes for finding nearby bars.
- **bar_finder_service.py** – Integrates with SerpAPI to retrieve bar information.
- **cocktail_of_the_day.py** – Route for generating a cocktail recommendation.
- **cocktail_of_the_day_service.py** – Logic for selecting and returning a random cocktail of the day.
