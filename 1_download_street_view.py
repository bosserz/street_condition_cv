import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Set your API key here
API_KEY = os.getenv("API_KEY")

# Output folder to save images
OUTPUT_FOLDER = "street_view_images"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def get_street_view_image(lat, lon, heading=0, fov=90, pitch=0, save_as="image.jpg"):
    """
    Downloads a Google Street View image for a given latitude and longitude.
    
    Args:
    - lat (float): Latitude
    - lon (float): Longitude
    - heading (int): Camera direction in degrees (0 to 360)
    - fov (int): Field of view (default 90)
    - pitch (int): Camera angle (-90 to 90)
    - save_as (str): Filename to save the image
    """
    
    base_url = "https://maps.googleapis.com/maps/api/streetview"
    
    params = {
        "size": "640x640",  # Max size (640x640 for free tier)
        "location": f"{lat},{lon}",
        "heading": heading,
        "fov": fov,
        "pitch": pitch,
        "key": API_KEY
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        file_path = os.path.join(OUTPUT_FOLDER, save_as)
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Image saved: {file_path}")
    else:
        print(f"Failed to fetch image: {response.status_code}, {response.text}")

# Example: Download a Street View image of a specific location
latitude = 37.7749   # San Francisco latitude
longitude = -122.4194  # San Francisco longitude
get_street_view_image(latitude, longitude, save_as="sf_street.jpg")