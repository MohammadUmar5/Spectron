# 🌍 Spectron

**Spectron** is an offline, self-contained desktop application for detecting land cover and vegetation changes using multi-temporal LISS-4 and Sentinel imagery. Designed for simplicity and accuracy, Spectron enables users to select an Area of Interest and dates, then automatically processes satellite data to generate intelligible, false-alarm–resistant change maps—**no internet connection or remote sensing expertise required.**


## 👥 Team Members

| Name        | GitHub Profile                                   |
| --------------- | ------------------------------------------------ |
| Mohd Umar Warsi  (Lead) | [Link](https://github.com/MohammadUmar5)    |
| Mohd Aqdas Asim      | [Link](https://github.com/MohdAqdasAsim)    |
| Sameer                | [Link](https://github.com/SameerKhan9412)    |
| Saurav Singh      | [Link](https://github.com/South-IN)    |


## 🛠️ Tech Stack

**Frontend**
* React
* Tailwind CSS
* TypeScript
* Leaflet.js

**Backend**
* Python
* FastAPI
* NumPy
* Rasterio
* GDAL
* OpenCV
* SQLite

## 🚀 Features

* 🗺️ **AOI Selection**
  Draw or select your Area of Interest directly on the map.

* 🗓️ **Date-Based Comparison**
  Compare multi-temporal imagery to detect environmental change.

* 📡 **Automated Satellite Image Retrieval**
  Retrieves relevant imagery (LISS-4/Sentinel) based on user input.

* 🚨 **Smart Alerts**
  Get notified of significant vegetation or land cover changes.

* 🍃 **Change Detection**
  Uses NDVI and spectral band differencing for reliable results.

* 📊 **Summarized Reports**
  Generate statistics, summaries, and visual reports of change.

* 📴 **Offline Capable**
  Lightweight and fully functional without internet access.

## 📦 Getting Started

1. **Clone the Repository**

   ```bash
   git clone https://github.com/MohdAqdasAsim/Spectron
   cd Spectron
   ```

2. **Setup Backend**

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # or .venv\\Scripts\\activate on Windows
   pip install -r requirements.txt
   python3 main.py
   ```

3. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 📌 License

This project is for academic and research purposes only. For licensing or deployment inquiries, please contact the authors.
