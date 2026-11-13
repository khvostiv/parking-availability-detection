# Hackatoon Parking Lot Project

## Project Overview
This project is designed to help users locate available parking spots in real time. It combines frontend and backend functionalities, utilizing geolocation and Google Maps API to display nearby parking lots, with Flask serving as the backend and Node.js for managing server-side functionality.

## Features
- Real-time user geolocation to display nearby parking lots
- Google Maps integration for an interactive map with search and autocomplete functionality
- Visual markers for parking locations and custom icons for better UX
- Video feed and image display for parking lot status using Flask
- Backend integration for processing parking-related data

## Project layout

```
app.js                         Express map server (port 3000)
frontend/                      Map page, CSS, JS, and marker icons
backend/app.py                Flask camera page (port 5000)
backend/detector.py           Occupancy detection on the lot video
backend/data/media/           Sample lot video and still image
backend/data/CarParkPos.pkl   Saved stall coordinates
backend/tools/pick_spaces.py  Tool to mark stalls on the still image
backend/templates/            Flask HTML
backend/static/               Flask CSS
docs/                          Usage instructions
scripts/run-flask.js           Starts Flask with the local Python
```

## Setup and Installation

### Prerequisites
- Python 3.x
- Node.js and npm
- Google Maps API key
- Flask, OpenCV, and cvzone (installed from `backend/requirements.txt`)

1. Clone this repository and open the project folder in your editor.
2. Open a terminal in the project root.
3. Install Python packages:

   ```bash
   pip install -r backend/requirements.txt
   ```

4. Install Node packages:

   ```bash
   npm install
   ```

5. Start the Flask camera and the map server together:

   ```bash
   npm start
   ```

6. Open [http://localhost:3000](http://localhost:3000) for the map.
7. Open [http://localhost:5000](http://localhost:5000) for the parking-lot video feed.

[docs/Usage_Instructions.docx](docs/Usage_Instructions.docx) has the same run steps in Word format.

To re-mark stall boxes on the sample image:

```bash
python backend/tools/pick_spaces.py
```

Left-click adds a stall, right-click removes one, and `q` saves and quits.

## Future Improvements
- Real-time Tracking of Parking Availability: Use live video feeds and machine learning to automatically update parking availability in real-time.
- Integration with Database: Store and retrieve parking data for a more persistent experience.
- User Authentication: Allow users to log in and save their parking history.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE).

## Acknowledgements
- Google Maps API for providing mapping and geolocation services.
- Flask and Node.js communities for backend support.
