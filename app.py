from flask import Flask, request, render_template
import pandas as pd
import os

app = Flask(__name__)

# Load grammar school data
CSV_FILE = os.path.join(os.path.dirname(__file__), "grammar_schools.csv")
schools_df = pd.read_csv(CSV_FILE)

@app.route("/", methods=["GET", "POST"])
def home():
    results = None
    if request.method == "POST":
        postcode = request.form.get("postcode", "").strip().upper()
        if postcode:
            results = schools_df[schools_df["Postcode"].str.startswith(postcode[:4])]
    
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
