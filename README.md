# 🧠 UVA CS Connect

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3-lightgrey)](https://flask.palletsprojects.com/)

> A centralized hub for UVA Computer Science students to **network, collaborate, and discover events**.

---

## 🚀 Project Overview

**UVA CS Connect** is a web application built for UVA Computer Science students to unify the community.  
Currently, collaboration and event discovery occur across **Discord servers, group chats, and email threads**, leading to fragmentation and missed opportunities.

This platform provides a **single hub** where students can:

- 👥 Create detailed profiles with **year, courses, skills, experience, and interests**  
- 🤝 Find peers for **study groups, projects, and hackathons** using a smart matching system  
- 📅 Discover **CS-related events** like workshops, hackathons, lectures, and club activities  
- 🔍 Explore the community through **searching, filtering, and sorting** of profiles and events  

---

## 🎯 Key Features

### Student Profiles
- Create and manage personal profiles with:
  - Year, graduation date, and email
  - Courses and skills
  - Experience and interests
  - Availability schedules

### Smart Matching
- Match students based on:
  - Shared skills
  - Course overlaps
  - Common interests
- Ideal for finding teammates for **projects, hackathons, and study groups**

### Event Discovery
- Browse and register for CS-related events
- Filter by **type, date, and location**
- Integrated with student participation tracking

### Centralized Hub
- A single source for UVA CS community engagement  
- Reduces fragmented communication across multiple platforms

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | HTML5, CSS3, Bootstrap, JavaScript |
| **Backend** | Python 3 + Flask |
| **Database** | MySQL (hosted on Google Cloud Platform) |
| **Authentication** | Werkzeug password hashing |
| **Hosting** | Google Cloud Platform (GCP) |

---

## 🗂️ Database Schema Overview

The platform uses a **relational database** with strong entity relationships:

- **Student** → Profile and personal info  
- **Course / Enrollment** → Academic structure  
- **Event / Attends / Organizes** → Event management  
- **Experience / Skills / Interests** → Profile enrichment  
- **Match / MatchParticipation** → Student connection & collaboration  
- **AvailabilitySlot** → Scheduling system  

> Full SQL schema available in `schema.sql`.

---

## ⚙️ Setup & Installation

Follow these steps to get the project running locally.

# 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/uva-cs-connect.git
cd uva-cs-connect
```

Run the following commands in your project root to set up and launch the application:

# 2️⃣ Create & activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows
```

# 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

# 4️⃣ Create environment variables
```bash
echo "FLASK_APP=app" > .env
echo "FLASK_ENV=development" >> .env
echo "DATABASE_URL=mysql+pymysql://<user>:<password>@<host>/<database>" >> .env
echo "SECRET_KEY=your-secret-key" >> .env
```

# 5️⃣ Initialize the database
```bash
flask shell -c "from app.db import init_db; init_db()"
```

# 6️⃣ Run the application
```bash
flask run
```
