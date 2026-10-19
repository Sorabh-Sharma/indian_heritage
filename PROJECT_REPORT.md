# ACADEMIC PROJECT REPORT: INDIAN CULTURAL HERITAGE PLATFORM (CULTURE HUB)

**Degree:** Bachelor of Technology (B.Tech) / Computer Science & Engineering (Semester VII)  
**Project Title:** Interactive Digital Preservation and Geolocation Mapping System for Indian Cultural Heritage  
**Repository:** [github.com/Sorabh-Sharma/indian_heritage](https://github.com/Sorabh-Sharma/indian_heritage)  
**Deployment Platform:** Vercel Serverless (Python WSGI) + MongoDB Atlas Cloud Database  

---

## TABLE OF CONTENTS
1. [Abstract](#1-abstract)
2. [Problem Statement & Motivation](#2-problem-statement--motivation)
3. [Objectives & Scope](#3-objectives--scope)
4. [Technology Stack & Justification](#4-technology-stack--justification)
5. [System Architecture & Data Flow](#5-system-architecture--data-flow)
6. [Database Design & Data Modeling (MongoDB Atlas)](#6-database-design--data-modeling-mongodb-atlas)
7. [Core Modules & Implementation Details](#7-core-modules--implementation-details)
    - 7.1 Landing Page Experience
    - 7.2 Directory & Real-time Search / Filter Engine
    - 7.3 Geospatial Interactive Mapping (Mapbox & Leaflet.js)
    - 7.4 Authentication & Ownership-based Authorization (RBAC)
    - 7.5 Duplicate Prevention & Data Validation Logic
    - 7.6 Custom Royal Color Palette & UI Design System
8. [Security & Production Configuration](#8-security--production-configuration)
9. [Deployment Architecture (Vercel Serverless WSGI)](#9-deployment-architecture-vercel-serverless-wsgi)
10. [Test Cases & Verification Matrix](#10-test-cases--verification-matrix)
11. [Conclusion & Future Enhancements](#11-conclusion--future-enhancements)

---

## 1. ABSTRACT

India is home to an extraordinary cultural legacy comprising ancient architectural monuments, classical dances, music, spiritual festivals, handicrafts, and regional culinary arts. However, vast amounts of cultural documentation remain fragmented across static encyclopedia articles or isolated local repositories without interactive geographic context or community contribution capabilities.

This project, titled **"Indian Cultural Heritage Platform" (Culture Hub)**, is a full-stack web application built using **Django 5.0**, **MongoDB Atlas**, **Leaflet.js**, **Mapbox Tile API**, and **Tailwind CSS**. The platform provides an interactive, community-driven digital archive where authenticated cultural enthusiasts, researchers, and tourists can catalog heritage artifacts with precise GPS coordinates, rich descriptions, and categorization. The system features an interactive GIS map pinpointing heritage locations across the Indian subcontinent, real-time multi-attribute search and filtering, strict case-insensitive duplicate prevention algorithms, secure role-based item management (owners can edit and delete only their own contributions), and an ultra-modern responsive UI adhering to a custom royal palette (Deep Plum `#381932` and Milk Cream `#FFF3E6`). The application is engineered for production deployment on **Vercel Serverless Functions** with automated continuous delivery.

---

## 2. PROBLEM STATEMENT & MOTIVATION

### 2.1 The Problem
1. **Lack of Geographic Context:** Traditional cultural websites present records as plain text lists or tables. Users cannot visualize where monuments or regional festivals originate relative to each other on a map.
2. **Data Duplication:** Open crowdsourced repositories suffer from duplicate entries (e.g., "Taj Mahal", "taj mahal", "Taj mahal"), dispersing historical commentary across fragmented pages.
3. **Absence of Accountability:** Platforms without ownership controls permit anonymous tampering or unauthorized deletion of valuable entries.
4. **Outdated Aesthetics:** Many existing archival platforms are built on legacy frameworks with rigid layouts that perform poorly on mobile devices.

### 2.2 The Motivation
To build a resilient, modern, visually captivating web platform that enables structured digital preservation, spatial discovery via maps, and community contributions protected by enterprise-grade access control.

---

## 3. OBJECTIVES & SCOPE

### 3.1 Key Objectives
1. **Interactive Geographic Visualization:** Render GPS markers on an interactive Leaflet/Mapbox canvas with dynamic popup links.
2. **Role-Based Content Management:** Allow authenticated users to add heritage items, but restrict modification and deletion exclusively to the author of that item.
3. **Intelligent Search Engine:** Enable instant filtering across title, region, category, and historical description.
4. **Duplicate Prevention Engine:** Block duplicate entries using case-insensitive validation before database persistence.
5. **Aesthetic Excellence:** Use a custom palette inspired by Indian royalty (Deep Plum `#381932` and Warm Milk `#FFF3E6`) with smooth micro-interactions.
6. **Cloud Serverless Deployment:** Host the Django application on Vercel with high availability backed by MongoDB Atlas.

---

## 4. TECHNOLOGY STACK & JUSTIFICATION

| Component | Technology | Description & Justification |
| :--- | :--- | :--- |
| **Backend Framework** | Django 5.0+ | High-productivity Python framework with built-in ORM, security middleware, and authentication. |
| **Database** | MongoDB Atlas (`django-mongodb-backend`) | Cloud NoSQL document database providing dynamic schema flexibility and high scalability. |
| **Frontend Styling** | Tailwind CSS (via CDN) | Utility-first CSS framework enabling bespoke tokens, glassmorphism, and responsive design. |
| **Mapping Engine** | Leaflet.js + Mapbox Tile API | High-performance open-source JavaScript library for interactive mobile-friendly maps. |
| **Icons & Typography** | FontAwesome 6 + Google Fonts | Playfair Display (editorial serif) and Plus Jakarta Sans (clean readability). |
| **Cloud Hosting** | Vercel Serverless | Event-driven serverless WSGI execution with zero server maintenance costs. |

---

## 5. SYSTEM ARCHITECTURE & DATA FLOW

### 5.1 Architecture Overview
```
[ User Browser (Mobile / Desktop) ]
                |
                v  (HTTPS)
    [ Vercel Edge Router ]
                |
                v  (Rewrites from vercel.json)
[ Vercel Serverless Python WSGI Handler (HeritageProject/wsgi.py) ]
                |
   +------------+------------+
   |                         |
[ Django URL Dispatcher ]   [ Authentication Middleware ]
   |                         |
   +------------+------------+
                |
                v
       [ Django Views Engine ]
        - landing()
        - home() (Search + Category Filter + GeoJSON Serialization)
        - add_item() / edit_item() / delete_item() (CRUD + Ownership)
        - register_user() / login_user() / logout_user()
                |
                v
    [ Django ORM / django-mongodb-backend ]
                |  (TLS Connection String)
                v
    [ MongoDB Atlas Cloud Cluster ]
        - auth_user collection
        - culture_hub_heritageitem collection
```

---

## 6. DATABASE DESIGN & DATA MODELING (MONGODB ATLAS)

### 6.1 `HeritageItem` Model (`culture_hub_heritageitem` Collection)

| Field Name | Type | Options | Purpose |
| :--- | :--- | :--- | :--- |
| `id` | ObjectId | Primary Key | Unique MongoDB document identifier. |
| `author` | ForeignKey | `to=User`, `on_delete=CASCADE`, `null=True`, `blank=True` | Links item to the creator for ownership protection. |
| `title` | CharField | `max_length=200` | Cultural name (e.g., "Hawa Mahal", "Diwali"). |
| `category` | CharField | `max_length=100` | Classification (e.g., "Monument", "Festival", "Art Form"). |
| `region` | CharField | `max_length=100` | State or geographic origin (e.g., "Rajasthan"). |
| `description` | TextField | Unlimited text | In-depth historical narrative and cultural significance. |
| `latitude` | FloatField | `null=True`, `blank=True` | WGS84 GPS Latitude for map pin placement. |
| `longitude`| FloatField | `null=True`, `blank=True` | WGS84 GPS Longitude for map pin placement. |

---

## 7. CORE MODULES & IMPLEMENTATION DETAILS

### 7.1 Landing Page Experience (`landing.html`)
The entry point welcomes visitors with a majestic hero section, quick access cards, statistics on Indian heritage, and direct routing to explore the directory or register as a contributor.

### 7.2 Directory & Real-time Search / Filter Engine (`home.html`)
Enables visitors to locate cultural items through:
1. **Free-text search (`q` parameter):** Matches across `title`, `region`, and `description` using Django's `Q` objects (`icontains`).
2. **Category buttons:** Instant category filtering (`Monuments`, `Festivals`, `Dance`, `Cuisine`, etc.).

### 7.3 Geospatial Interactive Mapping
Items containing latitude and longitude coordinates are serialized into a JSON array in the backend:
```python
# culture_hub/views.py
map_items.append({
    'id': str(item.pk),
    'title': item.title,
    'region': item.region,
    'latitude': item.latitude,
    'longitude': item.longitude,
    'url': reverse('item_detail', kwargs={'pk': str(item.pk)}),
})
```
Leaflet.js consumes this array in `home.html`, placing custom-styled markers across India that open popups with direct links to full details.

### 7.4 Authentication & Ownership-based Authorization (RBAC)
- **Registration & Login:** Handled by Django's `UserCreationForm` and `AuthenticationForm`.
- **Protected Actions:** Adding an item requires `@login_required`.
- **Ownership Verification:** Before allowing editing or deletion, `edit_item` and `delete_item` verify:
  ```python
  if item.author and request.user != item.author:
      return HttpResponseForbidden("You do not have permission to modify this item.")
  ```
- **Conditional UI:** "Edit" and "Delete" buttons are only visible to the item's author.

### 7.5 Duplicate Prevention Logic (`forms.py`)
In `HeritageItemForm`:
```python
def clean_title(self):
    title = (self.cleaned_data.get('title') or '').strip()
    qs = HeritageItem.objects.filter(title__iexact=title)
    if self.instance and self.instance.pk:
        qs = qs.exclude(pk=self.instance.pk)
    if qs.exists():
        existing = qs.first()
        raise forms.ValidationError(
            f'"{title}" already exists in the Heritage Directory ({existing.category} in {existing.region}).'
        )
    return title
```

### 7.6 Royal Color Palette
- **Deep Plum:** `#381932` (Primary Brand Color)
- **Milk Cream:** `#FFF3E6` (Secondary Background Color)
- **Accent Ring:** `#381932/15` (Focus shadows and subtle borders)

---

## 8. SECURITY & PRODUCTION CONFIGURATION

1. **Environment Variables:** Credentials (`SECRET_KEY`, `MONGODB_URI`, `MAPBOX_ACCESS_TOKEN`) are separated into `.env` and kept out of Git.
2. **CSRF Protection:** All forms include `{% csrf_token %}` to prevent cross-site request forgery.
3. **Password Security:** Stored using PBKDF2 with SHA-256 password hashing.
4. **SQL/NoSQL Injection Immunity:** Handled by Django ORM parameterized queries.

---

## 9. DEPLOYMENT ARCHITECTURE (VERCEL SERVERLESS WSGI)

- **WSGI Entrypoint:** [HeritageProject/wsgi.py](file:///d:/sem7%20project/HeritageProject/HeritageProject/wsgi.py) exports `app = application`.
- **Configuration:** [vercel.json](file:///d:/sem7%20project/HeritageProject/vercel.json) directs all traffic to the WSGI handler using `@vercel/python`.
- **Database Connection:** Direct TLS connection from Vercel lambdas to MongoDB Atlas cluster.

---

## 10. TEST CASES & VERIFICATION MATRIX

| Test ID | Module | Scenario | Expected Outcome | Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Auth | Registration with valid username/password | Account created; logged in automatically | **PASS** |
| **TC-02** | Auth | Anonymous user visits `/add/` | Redirected to `/login/?next=/add/` | **PASS** |
| **TC-03** | CRUD | Submit new item with GPS coordinates | Document saved in MongoDB; pin renders on map | **PASS** |
| **TC-04** | Form | Add duplicate item (`"taj mahal"` when `"Taj Mahal"` exists) | Blocked with validation error message | **PASS** |
| **TC-05** | Auth | User A attempts to edit User B's post | Returns HTTP 403 Forbidden | **PASS** |
| **TC-06** | Search | Search keyword "Agra" | Filters matching monuments dynamically | **PASS** |
| **TC-07** | Map | Click on marker pin | Displays popup with title, region, and detail link | **PASS** |

---

## 11. CONCLUSION & FUTURE ENHANCEMENTS

### 11.1 Conclusion
The **Indian Cultural Heritage Platform** provides an interactive, community-empowered digital archive that bridges geographic visualization with cultural preservation. Built on Django, MongoDB Atlas, and Vercel, it combines speed, security, and responsive aesthetics.

### 11.2 Future Enhancements
1. **Multi-image Uploads:** Integration with Cloudinary / AWS S3 for user-contributed galleries.
2. **Multilingual Support:** Localization in Hindi, Tamil, Telugu, Bengali, Marathi, and other Indian languages.
3. **Marker Clustering:** Grouping dense clusters of monuments at high zoom levels.
4. **Virtual 360 Tours:** Embedding panoramic 360° views for heritage landmarks.
