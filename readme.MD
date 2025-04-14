

This project is a backend for an AI-powered website builder built using **Flask**, **MongoDB**, and **Google's Gemini AI model**. It allows users to sign up, log in securely using **JWT**, and generate customizable websites dynamically using AI.


- 🔐 JWT-based Authentication (Signup/Login)
- 🧠 AI-powered content generation via Gemini API
- 🌐 Website CRUD operations (Create,  Update, Delete)
- 🗃️ MongoDB for storing user and website data
- 🧪 API Testing with Postman
- 📦 Scalable and simple folder structure

---

ai_website_builder/ │
 ├── app/ │
  ├── init.py # Flask app factory │
  ├── auth.py # Auth routes (signup/login) 
  ├── ai.py # AI content generation │
  ├── website.py # Website CRUD operations │
  ├── templates/ # HTML templates (for frontend preview) 
    │--Preview_template/
        ├──Index.html #templates for generated website

  ├── static/ # Static assets (CSS/JS/images) │ 
  ├── .env # Environment variables (e.g. DB URI, JWT secret) 
  ├── run.py # Entry point ├── requirements.txt # Python dependencies 
  └── README.md # You're here!

## 🧪 API Endpoints

### Auth
| Method | Endpoint              | Description        |
|--------|-----------------------|--------------------|
| POST   | `/api/auth/signup`    | Register new user  |
| POST   | `/api/auth/login`     | Login and get JWT  |

### AI
| Method | Endpoint             | Description                          |
|--------|----------------------|--------------------------------------|
| POST   | `/api/ai/generate`   | Generate website content using AI    |

### Website
| Method | Endpoint                     | Description                |
|--------|------------------------------|----------------------------|
| GET    | `/api/website/`              | Get all websites (user)    |
| POST   | `/api/website/`              | Create a new website       |
| PUT    | `/api/website/<id>`          | Update website by ID       |
| DELETE | `/api/website/<id>`          | Delete website by ID       |

Set up your .env file Create a .env file in the root with the following:
FLASK_ENV=development
MONGO_URI=mongodb://localhost:27017/ai_website_builder
JWT_SECRET_KEY=your_super_secret_key
GEMINI_API_KEY=your_google_gemini_api_key

Create virtual environment & install dependencies
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

python run.py


