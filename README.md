# 🌱 EcoFinds

> **Give products a second life.**

EcoFinds is a full-stack, eco-friendly marketplace platform where users can buy, sell, search, save, and message about reusable and second-hand products. Every listed product is scored automatically by an environmental sustainability algorithm based on category and condition.

---

## 🚀 Features

* **Authentication & Profiles:** Session-based user sign up, login, and secure password hashing with Werkzeug.
* **Product Catalog & Filtering:** Real-time multi-attribute search and filtering across categories, price ranges, condition, and location.
* **Sustainability Scoring System:** Automatic eco-impact rating (0–100 🌱) computed per item.
* **Listing Management:** Registered users can create, photograph, and manage their listings.
* **Wishlist Integration:** Interactive AJAX-powered wishlist to save items.
* **Direct Messaging:** Built-in internal messaging to contact sellers regarding specific items.
* **Admin Dashboard:** Platform metrics overview, listing moderation, and user management.

---

## 🛠️ Technology Stack

* **Backend:** Python, Flask
* **Database:** SQLite3
* **Templates & Frontend:** Jinja2, HTML5, CSS3, Vanilla JavaScript

---

## 📁 Project Structure

```text
EcoFinds/
│
├── app.py                     # Main application factory & route registration
├── database.py                # Database connection and schema creation
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
├── .gitignore                 # Version control exclusions
│
├── database/
│   ├── ecofinds.db            # SQLite database file (generated automatically)
│   └── init_db.py             # Database initialization and sample seed script
│
├── routes/
│   ├── __init__.py
│   ├── auth.py                # Signup, login, logout routes
│   ├── products.py            # Browse, details, sell, delete routes
│   ├── wishlist.py            # Wishlist toggle and view routes
│   ├── messages.py            # Direct messaging routes
│   └── admin.py               # Admin and user dashboard routes
│
├── utils/
│   ├── __init__.py
│   ├── scoring.py             # Sustainability score calculation algorithm
│   └── validation.py          # Email, file upload, and image validation helpers
│
├── templates/
│   ├── index.html             # Landing page with hero & featured items
│   ├── login.html             # User authentication login
│   ├── signup.html            # User registration
│   ├── products.html          # Marketplace catalog with dynamic filters
│   ├── product-details.html   # Detailed product view & contact seller form
│   ├── sell.html              # Item submission form with image upload
│   ├── dashboard.html         # User dashboard & personal listings
│   ├── wishlist.html          # Saved items view
│   ├── messages.html          # Inbox & conversation view
│   └── admin.html             # Admin portal for platform moderation
│
├── static/
│   ├── css/
│   │   ├── style.css          # Core design system & common components
│   │   ├── auth.css           # Forms and authentication styling
│   │   ├── products.css       # Catalog cards and details page styling
│   │   └── dashboard.css      # Tables, stats, and message UI styling
│   └── js/
│       ├── main.js            # Responsive navbar & global utilities
│       ├── auth.js            # Form verification & password matching
│       ├── products.js        # Filter & AJAX wishlist handler
│       ├── sell.js            # Image upload preview handler
│       ├── wishlist.js        # Wishlist interactions
│       ├── dashboard.js       # Dashboard behavior
│       └── api.js             # Reusable async fetch wrappers
│
└── uploads/
    └── products/              # Uploaded user product images