import pandas as pd
import matplotlib.pyplot as plt
import ast
import csv
import pandas as pd
import matplotlib.pyplot as plt

# Define all column names (20 questions + 5 traits × 2)
trait_names = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']
columns = [f"Q{i+1}" for i in range(20)]
for trait in trait_names:
    columns.append(f"{trait}_Level")
    columns.append(f"{trait}_Careers")

# Load the data
df = pd.read_csv("responses.csv", header=None)
df.columns = columns

# Example analysis: Count how many people scored High/Moderate/Low for each trait
for trait in trait_names:
    counts = df[f"{trait}_Level"].value_counts()
    counts.plot(kind="bar", title=f"{trait} Level Distribution", color='skyblue')
    plt.xlabel("Level")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()



# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score

# X = df[['Q1', 'Q2', 'Q3', 'Q4', 'Q5']]
# y = df['Personality']

# # Convert categorical answers to numbers
# X_encoded = pd.get_dummies(X)
# y_encoded = y.astype('category').cat.codes

# X_train, X_test, y_train, y_test = train_test_split(X_encoded, y_encoded, test_size=0.2, random_state=42)

# model = RandomForestClassifier()
# model.fit(X_train, y_train)

# predictions = model.predict(X_test)
# print("Accuracy:", accuracy_score(y_test, predictions))
