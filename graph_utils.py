import matplotlib.pyplot as plt
import re

# Dynamic piechart that will display the composition of drugs
def plot_composition_pie(composition_str, title = None):
        # All compositions in the dataset are separated byt +, this first splits all elements by +
        components = [comp.strip() for comp in composition_str.split('+')]
        # The lists are to make the pie chart dynamic, some drugs have varying numbers of compositions
        # Labels is the drug composition names (eg. Amoxycillin), values is the strength (eg. 100mg)
        labels = []
        values = []

        for comp in components:
            # This first searches for the composition name and strength and applies the data to 'match'
            match = re.match(r"(.+?)\s*\(([\d\.]+)", comp)
            # If a match is found, attach group1, which is the name to name, attach group2, the strength to amount
            if match:
                name = match.group(1).strip()
                try:
                    amount = float(match.group(2))
                except ValueError:
                     amount = 0
                # This appends them to the previously created lists
                labels.append(name)
                values.append(amount)
            else:
                # Raw component if no match is found or if data is unavailable
                labels.append(comp)
                values.append(0)
        if all(v == 0 for v in values):
            labels = ["No dosage data found"]
            values = [1]

        # !!!!!!!MESS AROUND WITH PART LATER WHEN CLEANING THE WEB PAGE!!!!!!!!
        # Code for the actual pie chart
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')
        if title:
            ax.set_title(title)
        return fig

# Function for cleaning up the treatments column
def clean_treatments(treatments_str):
        # Correcting occasional missing spaces between "Treatment of"
        cleaned_str = re.sub(r'(\w)([A-Z])', r'\1 \2', treatments_str)

        # Insert delimiter for ease of splitting
        cleaned_str = cleaned_str.replace("Treatment of", "|Treatment of")

        # Split by the delimiter and remove "Treatment of" from each piece
        treatments = [
            # Remove "Treatment of" if present
            re.sub(r'^Treatment of\s*', '', t.strip())
            for t in cleaned_str.split("|")
            # Skip empty strings
            if t.strip()  
        ]
        return treatments

# Simple function for returning the common side effects which are separated by a space and then a capital letter
def clean_side_effects(side_effects_str):
    side_effects = re.split(r'\s(?=[A-Z])', side_effects_str)
    return side_effects

# Function that contains a bar chart that shows positive, neutral, and negative reviews based off 100 reviews
def plot_review_bar(positive, neutral, negative, drug_name):
    x = [drug_name]  # Use the drug name as the label
    width = 0.4

    # Create a bar chart
    fig, ax = plt.subplots()
    ax.bar(x, positive, width, label='Positive', color='green')
    ax.bar(x, neutral, width, label='Neutral', color='gray', bottom=positive)
    ax.bar(x, negative, width, label='Negative', color='red', bottom=[p + n for p, n in zip(positive, neutral)])

    # Add labels, title, and legend
    ax.set_ylabel('Percentage')
    ax.set_title('Review Distribution')
    ax.legend()
    return fig