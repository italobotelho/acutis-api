## The Acutis API: The Open-Source Catholic Database

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

**The Acutis API** is a global, open-source RESTful API providing structured, historically accurate data about the Catholic Church, including Saints, Popes, Patronages, and Miracles. 

By offering a clean, relational database accessible via standard JSON endpoints, this project empowers developers around the world to build Catholic apps, websites, AI recommendation systems, and educational tools without having to scrape the web from scratch.

---

### 💡 The Inspiration

This project is deeply inspired by **Blessed Carlo Acutis**, the "Cyberapostle of the Eucharist." Carlo used his passion for computer science and web development in the early days of the internet to catalog Eucharistic miracles and evangelize globally. 

In his spirit, this API seeks to use modern technology (Data Engineering, Relational Databases, and AI-ready structures) to make the rich history and wisdom of the Church accessible to the next generation of digital creators.

---

### 🚀 Core Features

- **Saints & Blesseds:** Deep biographical data, liturgical feast days, and canonical status.
- **Papal History:** Complete lineage of the Popes, including pontificate dates, origins, and religious orders.
- **Patronages (N:N Mapping):** An associative engine linking saints to their respective causes, professions, and places, perfect for recommendation algorithms.
- **Miracles & Geography:** Validated miracles mapped with precise latitude and longitude for global visualization.

---

### 💻 Quick Start & API Endpoints

The API follows standard REST conventions. Here are a few examples of how developers can consume the data:

**1. Get a specific Saint by Name**
GET /api/v1/saints?name=carlo_acutis

    {
      "data": {
        "id": "e4b3c9a2-5f6a-4b8c-9d1e-2f3a4b5c6d7e",
        "official_name": "Blessed Carlo Acutis",
        "baptism_name": "Carlo Acutis",
        "gender": "M",
        "current_status": "Blessed",
        "feast_day": 12,
        "feast_month": 10,
        "birth_date": "1991-05-03",
        "is_doctor_of_church": false,
        "short_bio": "An Italian teenager and amateur computer programmer, best known for documenting Eucharistic miracles.",
        "patronages": [
          {
            "cause": "Internet",
            "justification": "Used technology and website creation to catalog miracles and evangelize."
          }
        ]
      }
    }

**2. Discover Patron Saints by Cause**
GET /api/v1/patronages?cause=students

**3. Map Historical Miracles**
GET /api/v1/miracles?type=eucharistic

---

### 🏗️ Architecture & Tech Stack

- **Scraping & Data Mining:** Python (BeautifulSoup/Scrapy)
- **Backend API:** Python (FastAPI) / Node.js
- **Database:** PostgreSQL (Relational schema designed for scale)

---

### 🤝 Contributing

This is a community-driven project! We need developers, data engineers, and historians from all over the world to help us expand the database, optimize the code, and map more relationships.

Please read our CONTRIBUTING.md to learn about our Git Flow, code style, and how to submit a Pull Request.

---
*“To always be close to Jesus, that’s my life plan.” — Blessed Carlo Acutis*