# 🏛️ IndiaHeritage — Indian Cultural Heritage Directory & Interactive Map

> **Preserve. Discover. Celebrate.**  
> A full-stack web application designed to document, map, and celebrate India's 5,000-year-old living heritage — from monuments and classical art forms to regional festivals and folk traditions.

---

## 🌟 Key Features

- 🗺️ **Interactive Geospatial Map**: Built using Leaflet.js powered by Mapbox Streets. Features custom-styled pins, auto-framing (`fitBounds`), and rich modal popups linking directly to heritage detail pages.
- 🔐 **User Authentication & Permissions**: Complete signup, sign-in, and session management. Creation, editing, and deletion are restricted to authenticated users, with strict author ownership enforcement.
- 🛡️ **Duplicate Prevention Engine**: Case-insensitive backend validation (`clean_title`) combined with frontend double-click submission safeguards to ensure database integrity.
- 🔍 **Live Search & Dynamic Category Filtering**: Search instantly across titles, regions, and descriptions, or filter by categories (Monuments, Festivals, Classical Arts, Folk Traditions).
- 🎨 **Plum & Milk Design System**: Tailored with an Indian royal aesthetic using a palette of Royal Plum (`#381932`) and Warm Creamy Milk (`#FFF3E6`), modern typography (*Playfair Display* & *Poppins*), and glassmorphism cards.
- 🍃 **Cloud Database Integration**: Seamless NoSQL document storage powered by MongoDB Atlas and `django_mongodb_backend`.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Python, Django 6.1 |
| **Database** | MongoDB Atlas via `django_mongodb_backend` |
| **Mapping & GIS** | Leaflet.js, Mapbox API (`mapbox/streets-v12`) |
| **Frontend / Styling** | HTML5, Tailwind CSS, Vanilla JavaScript, FontAwesome 6 |
| **Typography** | Google Fonts (*Playfair Display* & *Poppins*) |

---

## 📁 Project Architecture

```
HeritageProject/
├── HeritageProject/          # Core Django project settings & root URLs
│   ├── settings.py           # MongoDB config, Auth redirects, Mapbox settings
│   ├── urls.py               # Root URL configurations
│   └── wsgi.py
├── culture_hub/              # Cultural Heritage Django App
│   ├── models.py             # HeritageItem model with GPS coordinates & Author FK
│   ├── forms.py              # ModelForm with duplicate validation & Tailwind styling
│   ├── views.py              # Auth views, CRUD handlers, and JSON map serializers
│   ├── urls.py               # App routes (/directory/, /login/, /register/, etc.)
│   └── templates/            # Plum & Milk themed HTML templates
│       ├── landing.html      # Hero showcase with glassmorphism & CTA
│       ├── home.html         # Heritage directory & Leaflet Mapbox map
│       ├── item_detail.html  # Full single-item heritage view
│       ├── add_item.html     # Community contribution form with GPS coordinates
│       ├── edit_item.html    # Author-only item editor
│       ├── confirm_delete.html# Author-only deletion safeguard
│       ├── login.html        # Authentication sign-in card
│       └── register.html     # Registration card with instant session login
└── manage.py
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Sorabh-Sharma/indian_heritage.git
cd indian_heritage
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install django django-mongodb-backend pymongo dnspython
```

### 4. Database Setup
Ensure your MongoDB Atlas connection string is configured in `HeritageProject/settings.py`.

Apply migrations:
```bash
python manage.py migrate
```

### 5. Run the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
- **Landing Page**: `http://127.0.0.1:8000/`
- **Heritage Directory & Map**: `http://127.0.0.1:8000/directory/`

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
