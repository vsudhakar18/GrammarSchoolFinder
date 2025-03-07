from flask import Flask, request, render_template
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

app = Flask(__name__)

# Load grammar schools data
schools_df = pd.read_csv("grammar_schools.csv")

def get_lat_lon(postcode):
    """Get latitude and longitude of a postcode using Nominatim."""
    geolocator = Nominatim(user_agent="geo_finder")
    location = geolocator.geocode(postcode)
    if location:
        return (location.latitude, location.longitude)
    return None

def find_schools_in_catchment(user_postcode, radius_miles=10):
    """Find grammar schools within a radius of the given postcode."""
    user_location = get_lat_lon(user_postcode)
    if not user_location:
        return []

    in_catchment = []
    for _, row in schools_df.iterrows():
        school_location = (row["Latitude"], row["Longitude"])
        distance = geodesic(user_location, school_location).miles
        if distance <= radius_miles:
            in_catchment.append({"name": row["Name"], "postcode": row["Postcode"], "distance_miles": round(distance, 2)})

    return in_catchment

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_postcode = request.form["postcode"]
        radius = int(request.form["radius"])
        schools = find_schools_in_catchment(user_postcode, radius)
        return render_template("index.html", schools=schools, postcode=user_postcode, radius=radius)
    return render_template("index.html", schools=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
