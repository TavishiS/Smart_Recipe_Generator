# Smart Recipe Generator

An intelligent recipe recommendation application that generates personalized recipes based on the ingredients available with the user and their cooking preferences.

The application uses a Large Language Model (LLM) to generate recipe suggestions and then ranks them using a custom scoring system to present the most suitable recipes to the user.

---

# Features

• Generate recipes using available ingredients  
• Preference-based filtering (difficulty, cooking time, health preference)  
• Intelligent ranking of recipes using a scoring algorithm  
• AI-powered recipe generation using an LLM  
• Mobile application built using Flutter  
• Backend API built using FastAPI  
• Works both on laptop and Android device  
• APK generation for easy sharing and testing

---

# How the Project Works

The application follows a **Frontend → Backend → AI → Ranking → Response** workflow.

### Step 1: User Input
The user enters:

- Ingredients they have
- Preferred cooking time (fast / medium)
- Preferred difficulty level
- Whether they want a healthy recipe

This input is collected in the **Flutter frontend**.

---

### Step 2: API Request
The frontend sends the user input to the backend using a REST API call.

```
POST /generate_recipes
```

---

### Step 3: AI Recipe Generation
The backend sends the request to an LLM to generate multiple recipe suggestions.

The LLM returns structured recipe data including:

- recipe name
- ingredients
- cooking steps
- cooking time
- difficulty level

---

### Step 4: Recipe Ranking Algorithm

The backend evaluates each generated recipe using a **custom scoring system**.

Each recipe is scored using:

• **Ingredient Match Score** – how many ingredients match user input  
• **Difficulty Score** – whether the difficulty matches user preference  
• **Time Score** – whether cooking time matches preference  
• **Health Score** – whether the recipe satisfies healthy preference  

The recipe score is computed as:

```
Final Score =
Ingredient Match Score
+ Difficulty Score
+ Time Score
+ Health Score
```

Recipes are then **sorted in descending order of score**.

---

### Step 5: Response to Frontend
The ranked recipes are sent back to the Flutter application and displayed to the user.

---

# Tech Stack

### Frontend
Flutter  
Dart  

### Backend
FastAPI  
Python  

### AI Integration
Google Gemini API (LLM)

### API Communication
REST API  
HTTP requests

### Development Tools
Flutter SDK  
Uvicorn  
ngrok (for exposing local backend to mobile devices)

---

# Project Structure

```
instant_recipes
│
├── backend
│   ├── main.py
│   ├── recipe_generator.py
│   ├── recipe_ranker.py
│   └── .env
│
├── frontend
│   ├── instant_recipe_f
│   └── lib
│       └── services
│           └── api_service.dart
│
└── README.md
```

---

# Setup Instructions

## 1. Android Permission

Make sure the following line is present in:

```
flutter_app/android/app/src/main/AndroidManifest.xml
```

```xml
<uses-permission android:name="android.permission.INTERNET"/>
```

This enables the app to make API calls when running on a phone.

---

# 2. Clone the Repository

Clone the repository in a directory, for example:

```
instant_recipes
```

---

# 3. Running the Application

## (i) Run on Laptop

Navigate to:

```
frontend/lib/services/api_service.dart
```

Set the base URL:

```dart
static const String baseUrl = "http://localhost:8000";
```

Start the backend server:

```
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Open another terminal:

```
cd frontend/instant_recipe_f
flutter run
```

Select **Chrome** or any suitable device.

---

## (ii) Run on Phone (Using ngrok)

Start ngrok:

```
ngrok http 8000
```

Copy the URL provided by ngrok.

Update:

```
frontend/lib/services/api_service.dart
```

```dart
static const String baseUrl = "https://<app_link_provided_by_ngrok>";
```

Start backend:

```
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Build APK:

```
cd frontend/instant_recipe_f

flutter clean
flutter pub get
flutter build apk
```

APK will be generated at:

```
frontend/instant_recipe_f/build/app/outputs/flutter-apk/app-release.apk
```

Share this APK with another device while **keeping backend and ngrok running**.

Install the APK and start using the application.

---

# Disclaimer

When clicking **Generate Recipes**, the app may take **6–10 seconds** to respond.

This delay occurs because the application sends a request to the LLM to generate recipe suggestions, which are then processed and ranked by the backend.

---

# API Key

To run the project, create a `.env` file inside the backend folder and add your API key.

Example:

```
GEMINI_API_KEY=your_api_key_here
```

Without an API key, the application cannot generate recipes.

---

# Author

Tavishi Srivastava