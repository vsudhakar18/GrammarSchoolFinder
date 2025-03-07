from flask import Flask, render_template, request
import pandas as pd
from geopy.distance import geodesic
import requests

app = Flask(__name__)

# Load grammar schools data
schools_df = pd.read_csv("grammar_schools.csv")

# Function to get latitude & longitude of a postcode
def get_lat_lon(postcode):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={postcode}"
    response = requests.get(url).json()
    if response:
        return float(response[0]['lat']), float(response[0]['lon'])
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    
    if request.method == "POST":
        postcode = request.form.get("postcode")
        radius = float(request.form.get("radius"))

        user_location = get_lat_lon(postcode)
        if user_location:
            user_lat, user_lon = user_location

            for _, row in schools_df.iterrows():
                school_location = (row["Latitude"], row["Longitude"])
                distance = geodesic(user_location, school_location).miles
                
                if distance <= radius:
                    results.append({
                        "name": row["School Name"],
                        "postcode": row["Postcode"],
                        "distance": round(distance, 2),
                        "type": row["Type"],
                        "website": row["Website"]
                    })

            results.sort(key=lambda x: x["distance"])  # Sort by nearest school

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
