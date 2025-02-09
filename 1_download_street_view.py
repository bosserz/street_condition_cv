import requests
import os
import polyline
from dotenv import load_dotenv
load_dotenv()

# Set your API key here
API_KEY = os.getenv("API_KEY")


# Download a Street View image 100 points in Atlanta Midtown Area
# Define start and end locations (14th Street NW/NE)
start_lat, start_lng = 33.747124, -84.396622
end_lat, end_lng = 33.786576, -84.383170

# Output directory
OUTPUT_FOLDER = "street_view_peachtree_st"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Function to get waypoints along the route using Google Directions API
def get_route_waypoints(start, end, mode="driving"):
    directions_url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": f"{start[0]},{start[1]}",
        "destination": f"{end[0]},{end[1]}",
        "mode": mode,
        "key": API_KEY
    }
    response = requests.get(directions_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            # Extract polyline points
            route_polyline = data["routes"][0]["overview_polyline"]["points"]
            waypoints = polyline.decode(route_polyline)  # Decode into (lat, lon) points
            return waypoints
    print(f"Error fetching route: {data.get('status')}")
    return []

# Function to download Street View images at given coordinates
def download_street_view_image(lat, lon, heading=0, save_as="image.jpg"):
    street_view_url = "https://maps.googleapis.com/maps/api/streetview"
    params = {
        "size": "640x640",  # Max free size
        "location": f"{lat},{lon}",
        "heading": heading,  # Adjust heading to follow the road direction
        "fov": 90,  # Field of View
        "pitch": 0,  # Camera angle
        "key": API_KEY
    }
    
    response = requests.get(street_view_url, params=params)
    
    if response.status_code == 200:
        file_path = os.path.join(OUTPUT_FOLDER, save_as)
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Image saved: {file_path}")
    else:
        print(f"Failed to fetch image: {response.status_code}, {response.text}")

# Get waypoints along 14th Street NW/NE
waypoints = get_route_waypoints((start_lat, start_lng), (end_lat, end_lng))

# Download images at each waypoint
for i, (lat, lon) in enumerate(waypoints):
    download_street_view_image(lat, lon, save_as=f"peachtree_st_{i}.jpg")