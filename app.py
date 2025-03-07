from flask import Flask, request
import pandas as pd

app = Flask(__name__)

# Load grammar school data (Make sure grammar_schools.csv is in the same folder)
df = pd.read_csv("grammar_schools.csv")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_postcode = request.form.get("postcode", "").strip()
        radius = request.form.get("radius", "10")  # Default radius to 10 miles

        # Filter the schools based on postcode (Dummy filtering logic for now)
        schools = df[df["Postcode"].str.startswith(user_postcode[:4])]

        # Read index.html and insert school data dynamically
        with open("index.html", "r") as f:
            html_content = f.read()

        school_list = "<ul>"
        for _, row in schools.iterrows():
            school_list += f"<li>{row['School Name']} - {row['Postcode']}</li>"
        school_list += "</ul>"

        html_content = html_content.replace("{{SCHOOL_LIST}}", school_list)

        return html_content

    # Serve the index.html page
    return open("index.html").read()

if __name__ == "__main__":
    app.run(debug=True)
