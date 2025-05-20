from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

insights = {
    "Openness": {
        "Low": ["You prefer traditional and familiar experiences.", ["Operations Assistant", "Bookkeeper"]],
        "Moderate": ["You enjoy a balance of new and familiar experiences.", ["Project Manager", "Business Analyst"]],
        "High": ["You are imaginative and open to new experiences.", ["Creative Director", "Research Scientist"]]
    },
    "Conscientiousness": {
        "Low": ["You may prefer flexibility over structure.", ["Freelancer", "Artist"]],
        "Moderate": ["You are fairly reliable and organized.", ["Team Lead", "Content Strategist"]],
        "High": ["You are highly organized and reliable.", ["Data Analyst", "Engineer"]]
    },
    "Extraversion": {
        "Low": ["You enjoy solitude and reflective activities.", ["Archivist", "Librarian"]],
        "Moderate": ["You enjoy social activities in moderation.", ["Customer Support", "Teacher"]],
        "High": ["You are outgoing and energetic.", ["Sales Manager", "Event Coordinator"]]
    },
    "Agreeableness": {
        "Low": ["You may be more skeptical of others' motives.", ["Lawyer", "Critic"]],
        "Moderate": ["You are generally cooperative with occasional assertiveness.", ["Mediator", "Journalist"]],
        "High": ["You are compassionate and cooperative.", ["Nurse", "Social Worker"]]
    },
    "Neuroticism": {
        "Low": ["You are calm and emotionally stable.", ["Pilot", "Surgeon"]],
        "Moderate": ["You experience occasional stress.", ["Manager", "Developer"]],
        "High": ["You are sensitive and experience emotional highs and lows.", ["Writer", "Artist"]]
    }
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    traits = {"Openness": [], "Conscientiousness": [], "Extraversion": [], "Agreeableness": [], "Neuroticism": []}
    
    for key, val in data.items():
        trait = key.split("_")[0]
        traits[trait].append(int(val))
    
    results = {}
    for trait, values in traits.items():
        avg = sum(values) / len(values)
        if avg >= 3.5:
            level = "High"
        elif avg > 2.5:
            level = "Moderate"
        else:
            level = "Low"
        description, careers = insights[trait][level]
        results[trait] = {
            "level": level,
            "description": description,
            "careers": careers
        }

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
