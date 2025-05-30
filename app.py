import csv
import os

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
    
    traits = {
        "Openness": [],
        "Conscientiousness": [],
        "Extraversion": [],
        "Agreeableness": [],
        "Neuroticism": []
    }

    # Extract and organize answers by trait
    for key, value in data.items():
        trait, idx = key.split("_")
        traits[trait].append(int(value))

    results = {}
    csv_row = []

    for trait, scores in traits.items():
        avg = sum(scores) / len(scores)
        if avg >= 4:
            level = "High"
            careers = {
                "Openness": ["Creative Director", "Research Scientist"],
                "Conscientiousness": ["Data Analyst", "Engineer"],
                "Extraversion": ["Sales Manager", "Public Speaker"],
                "Agreeableness": ["Counselor", "Non-Profit Manager"],
                "Neuroticism": ["Artist", "Writer"]
            }[trait]
            description = {
                "Openness": "You are imaginative and open to new experiences.",
                "Conscientiousness": "You are highly organized and reliable.",
                "Extraversion": "You are outgoing and thrive in social settings.",
                "Agreeableness": "You are empathetic and get along well with others.",
                "Neuroticism": "You tend to be emotionally reactive and sensitive."
            }[trait]
        elif avg >= 2.5:
            level = "Moderate"
            careers = {
                "Openness": ["Graphic Designer", "Marketing Specialist"],
                "Conscientiousness": ["Project Coordinator", "Teacher"],
                "Extraversion": ["Customer Support", "Teacher"],
                "Agreeableness": ["Mediator", "Journalist"],
                "Neuroticism": ["Therapist", "Musician"]
            }[trait]
            description = {
                "Openness": "You are somewhat imaginative and open to trying new things.",
                "Conscientiousness": "You are reasonably dependable and organized.",
                "Extraversion": "You enjoy social activities in moderation.",
                "Agreeableness": "You are generally cooperative with occasional assertiveness.",
                "Neuroticism": "You occasionally feel stressed but usually handle emotions well."
            }[trait]
        else:
            level = "Low"
            careers = {
                "Openness": ["Technician", "Data Entry Clerk"],
                "Conscientiousness": ["Artist", "Musician"],
                "Extraversion": ["Writer", "Software Developer"],
                "Agreeableness": ["Lawyer", "Debater"],
                "Neuroticism": ["Pilot", "Surgeon"]
            }[trait]
            description = {
                "Openness": "You prefer routine over novelty and like practical ideas.",
                "Conscientiousness": "You may prefer flexibility and spontaneity.",
                "Extraversion": "You enjoy solitude and prefer quiet environments.",
                "Agreeableness": "You are assertive and prioritize logic over emotions.",
                "Neuroticism": "You are calm and emotionally stable."
            }[trait]

        results[trait] = {
            "level": level,
            "description": description,
            "careers": careers
        }

        # For CSV: level + comma-separated career list
        csv_row.append(level)
        csv_row.append(", ".join(careers))

    # Add original answers to the CSV (Q0 to Q19)
    all_answers = [str(data[f"{trait}_{i}"]) for trait in traits for i in range(4)]
    csv_row = all_answers + csv_row

    # Save to CSV
    file_exists = os.path.isfile("responses.csv")
    with open("responses.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            header = [f"{trait}_{i}" for trait in traits for i in range(4)]
            header += [f"{trait}_level" for trait in traits]
            header += [f"{trait}_careers" for trait in traits]
            writer.writerow(header)
        writer.writerow(csv_row)

    return jsonify(results)


def calculate_personality(data):
    traits = {"Openness": [], "Conscientiousness": [], "Extraversion": [], "Agreeableness": [], "Neuroticism": []}
    
    for key, val in data.items():
        trait = key.split("_")[0]
        traits[trait].append(int(val))
    
    results = {}
    for trait, values in traits.items():
        if values:  # Prevent division by zero
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

    return results

if __name__ == "__main__":
    app.run(debug=True)
