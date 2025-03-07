from flask import Flask, render_template, request
import pandas as pd
import geopy.distance

app = Flask(__name__)

def load_schools():
    df = pd.read_csv("data/grammar_schools.csv")
    return df

schools_df = load_schools()

def get_distance(postcode1, postcode2):
    # Dummy function to calculate crow-fly distance (replace with real geolocation lookup)
    return round(geopy.distance.geodesic((51.0, 0.0), (51.5, 0.5)).km, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    explanation = ""
    
    if request.method == 'POST':
        postcode = request.form.get('postcode', '').strip().upper()
        
        if postcode:
            schools_df['Distance'] = schools_df['Postcode'].apply(lambda x: get_distance(postcode, x))
            results = schools_df.sort_values(by='Distance').to_dict(orient='records')
            
            if not results:
                explanation = "No grammar schools found for this postcode. Some schools do not have strict catchment rules."
    
    return render_template('index.html', results=results, explanation=explanation)

if __name__ == '__main__':
    app.run(debug=True)
