# Hackatoon Parking Lot Project

## Project Overview
This project is designed to help users locate available parking spots in real time. It combines frontend and backend functionalities, utilizing geolocation and Google Maps API to display nearby parking lots, with Flask serving as the backend and Node.js for managing server-side functionality.

## Features
- Real-time user geolocation to display nearby parking lots
- Google Maps integration for an interactive map with search and autocomplete functionality
- Visual markers for parking locations and custom icons for better UX
- Video feed and image display for parking lot status using Flask
- Backend integration for processing parking-related data


## Setup and Installation
1.	Extract the Hackatoon project folder and open it in Visual Studio Code or your preferred code editor. 
2.	Open Terminal.
3.  Run 'npm install' to install node_modules
4.	Install concurrently (it is used to run the frontend and backend servers at the same time.):
        npm install concurrently --save-dev
5.	Start both the frontend and backend servers using concurrently:
        npm run start
6.	Open a browser and go to http://localhost:3000 to access the web app interface
7.	To view the parking lot video feed and check real-time parking availability, go to http://localhost:5000 


### Prerequisites
- Python 3.x
- Node.js and npm
- Google Maps API key
- Flask (Python package)

## Future Improvements
- Real-time Tracking of Parking Availability: Use live video feeds and machine learning to automatically update parking availability in real-time.
- Integration with Database: Store and retrieve parking data for a more persistent experience.
- User Authentication: Allow users to log in and save their parking history.

## License
This project is licensed under the MIT License.

## Acknowledgements
- Google Maps API for providing mapping and geolocation services.
- Flask and Node.js communities for backend support.
