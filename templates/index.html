from flask import Flask, render_template, request
import pandas as pd
import geopy.distance

app = Flask(__name__)

def load_schools():
    return pd.read_csv("data/grammar_schools.csv")

def get_distance(postcode, school_location):
    return round(geopy.distance.geodesic(postcode, school_location).km, 2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    postcode = request.form['postcode']
    schools = load_schools()
    results = []
    
    for _, row in schools.iterrows():
        distance = get_distance(postcode, row['Location'])
        results.append({
            "School Name": row['School Name'],
            "Location": row['Location'],
            "Crow Distance": distance,
            "In Catchment": row['In Catchment'],
            "Fully Selective": row['Fully Selective'],
            "Website": row['Website']
        })
    
    results = sorted(results, key=lambda x: x['Crow Distance'])
    return render_template('index.html', schools=results)

if __name__ == '__main__':
    app.run(debug=True)
