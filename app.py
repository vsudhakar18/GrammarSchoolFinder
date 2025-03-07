from flask import Flask, render_template, request
import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

app = Flask(__name__)

def get_coordinates(postcode):
    """Get latitude and longitude for a given postcode."""
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(postcode)
    if location:
        return (location.latitude, location.longitude)
    return None

def calculate_distances(user_postcode, schools_df):
    """Calculate distances and return sorted school list."""
    user_coords = get_coordinates(user_postcode)
    if not user_coords:
        return []
    
    schools_df['Distance'] = schools_df.apply(lambda row: geodesic(user_coords, (row['Latitude'], row['Longitude'])).miles, axis=1)
    return schools_df.sort_values(by='Distance').to_dict(orient='records')

# Load updated school data
schools_df = pd.read_csv("data/grammar_schools.csv")

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    error = None
    
    if request.method == 'POST':
        postcode = request.form.get('postcode', '').strip()
        if postcode:
            results = calculate_distances(postcode, schools_df)
            if not results:
                error = "Invalid postcode or no schools found."
    
    return render_template('index.html', results=results, error=error, disclaimer="Data sourced from various educational and governmental sources. Admission criteria and cut-off scores vary annually. Please refer to official school websites for the most accurate and up-to-date information.")

if __name__ == '__main__':
    app.run(debug=True)
