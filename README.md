# Gems & Stones

### Created by: Victor Wybon

## Project Overview

**Gems & Stones** is a simple Flask web application designed to manage and showcase a personal collection of gems, stones, and fossils. This app serves as a practical project to practice Flask development, while also offering an organized way to keep track of an ever-growing collection.

While the repository contains only a few sample images (due to storage considerations), this app is fully equipped to handle and display a larger library if hosted locally with the complete image set.

## Features

- **Stone Listing**: Displays a full list of all gems, stones, and fossils in the collection.
- **Stone Details**: Each item includes detailed information like comments, origin, acquisition date, purchase price, weight, additional info, and storage box details.
- **Search Functionality**: Allows users to search for specific stones by name.
- **Add New Stone**: Users can add new stones to the collection by filling out a form with relevant information.

## Project Structure

The app follows a standard Flask application structure:

- **`app.py`**: The main Flask application file that defines the routes and core logic.
- **`templates/`**: Contains the HTML templates for various views (`index.html`, `stone_detail.html`, `add_stone.html`, etc.).
- **`static/`**: Holds the CSS styles and any static images used by the app.
- **`resources/`**: A folder to include database files or configuration files if needed.
- **`bd/`**: Database file (if using SQLite) or other necessary backend files for storing stone data.

## Installation & Setup

- **Python 3.7 or more**
- **Flask**: Install Flask.
