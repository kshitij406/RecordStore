# RecordStore Website

A responsive web-based record store developed as part of my coursework. The project combines front-end web development with Python-based API integration to dynamically generate an XML dataset used by the website.

## Project Overview

This project simulates an online record store where users can browse music records and collections through a clean and responsive interface. Album data is not hardcoded. Instead, a Python script fetches real-world music metadata from external APIs and generates a structured XML file that the website consumes.

The project demonstrates separation between data generation and presentation logic, along with practical API usage and XML transformation.

## Features

* Home page showcasing featured records
* Collections page displaying albums in a grid layout
* Album details including artist, cover art, pricing, and Spotify embeds
* XML-driven content using XSLT
* Responsive design for desktop and mobile devices
* Clean and consistent UI styling
* Coursework-ready structure and documentation

## Tech Stack

**Frontend**

* HTML5
* CSS3
* JavaScript

**Data Generation**

* Python
* Deezer API for album metadata and cover images
* Spotify Web API for album embeds
* XML, DTD, and XSLT for structured data and transformation

**Tools**

* Git and GitHub for version control
* Vercel for deployment

## Project Structure

```
.
│   .gitignore
│   about.html
│   index.html
│   Links.txt
│   README.md
│   styles.css
│
├── images/
│   ├── about_record.gif
│   ├── collection_player.gif
│   ├── Facebook.png
│   ├── instagram.png
│   ├── Record_Store.gif
│   ├── search-icon(white).png
│   ├── store_logo.png
│   └── Street_Vinyl.gif
│
├── PythonScript/
│   ├── .env
│   └── records.py
│
└── XML/
    ├── records.dtd
    ├── records.xml
    └── records.xsl
```

## Data Pipeline (Python → XML)

Album data is generated using a Python script located in the `PythonScript` directory. The script:

* Fetches album metadata and cover images from the Deezer API
* Retrieves Spotify album IDs and generates embeddable player links
* Generates realistic pricing values programmatically
* Avoids duplicate records by checking existing XML entries
* Outputs a validated `records.xml` file using a DTD
* Supports XSLT transformation for frontend rendering

This XML file is then used by the website to display album collections dynamically.

## How to Run Locally

### Frontend

1. Clone the repository:

   ```
   git clone https://github.com/your-username/recordstore.git
   ```
2. Open `index.html` in a web browser.

### XML Generation (Optional)

1. Install required Python packages:

   ```
   pip install requests python-dotenv
   ```
2. Set Spotify API credentials in `PythonScript/.env`:

   ```
   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret
   ```
3. Run the script:

   ```
   python PythonScript/records.py
   ```

This will generate or update `XML/records.xml`.

## Deployment

The project is deployed using Vercel.

Live Demo:
https://recordstore-nine.vercel.app/

## Learning Outcomes

* API integration using Python
* XML data modeling with DTD validation
* XSLT-based content transformation
* Responsive UI development
* Clear separation of data and presentation layers
* Version-controlled coursework submission

## Author

Kshitij Jha
BSc Computer Science
