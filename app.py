from flask import Flask, render_template, request
import pandas as pd
import geopy.distance

app = Flask(__name__)

# Load the school data
schools_df = pd.read_csv("grammar_schools_with_catchment.csv")

def calculate_distance(lat1, lon1, lat2, lon2):
    return round(geopy.distance.geodesic((lat1, lon1), (lat2, lon2)).km, 2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    user_postcode = request.form['postcode']
    user_lat = float(request.form['latitude'])
    user_lon = float(request.form['longitude'])
    
    schools_df["Crow Distance"] = schools_df.apply(
        lambda row: calculate_distance(user_lat, user_lon, row["Latitude"], row["Longitude"]), axis=1
    )
    
    valid_schools = schools_df.sort_values(by="Crow Distance")
    
    # Check if school has catchment rules or is fully selective
    valid_schools["In Catchment"] = valid_schools["Catchment Rules"].apply(lambda x: "Yes" if x == "Yes" else "No")
    valid_schools["Fully Selective"] = valid_schools["Fully Selective"].apply(lambda x: "Yes" if x == "Yes" else "No")
    
    return render_template('index.html', schools=valid_schools.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
