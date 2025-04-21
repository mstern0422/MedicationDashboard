from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import base64
from io import BytesIO
import graph_utils

app = Flask(__name__)

# Load the drug data once when the app starts
data = pd.read_csv('Medicine_Details.csv')

@app.route('/')
def index():
    return render_template('index.html')

# Utility function to convert matplotlib figure to base64
def fig_to_base64(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close(fig) 
    return image_base64

@app.route('/search', methods=['POST'])
def search():
    # Contains the drug name searched by the user from the search bar
    drug_name = request.form['drug_name']
    # Contains drug information from dataset
    drug_info = data[data['Medicine Name'].apply(lambda x: drug_name.lower() in x.lower())]
    
    if not drug_info.empty:
        row = drug_info.iloc[0]

        # Check if the Composition column is NaN or empty
        if pd.isna(row['Composition']) or row['Composition'].strip() == "":
            return render_template('index.html', error="Composition data is missing for this drug.")

    # Both pie chart with drug composition and bar plot with reviews
        fig_composition = graph_utils.plot_composition_pie(row['Composition'], title = row['Medicine Name'])
        fig_reviews = graph_utils.plot_review_bar([row["Excellent Review %"]],
                                                [row["Average Review %"]],
                                                [row["Poor Review %"]],
                                                row['Medicine Name'])

    # Convert the figs to base64
        composition_img = fig_to_base64(fig_composition)
        reviews_img = fig_to_base64(fig_reviews)

    # Cleaned up list of treatments
        list_treatments = graph_utils.clean_treatments(row['Uses'])

    # Cleaned up list of side effects
        list_side_effects = graph_utils.clean_side_effects(row['Side_effects'])

    # Image of the drug 
        drug_image = row['Image URL']

        return render_template(
            'index.html',
            drug_name = row['Medicine Name'],
            composition_img = composition_img,
            reviews_img = reviews_img,
            treatments = list_treatments,
            side_effects = list_side_effects,
            drug_image = drug_image
        )
    else:
        return render_template('index.html', not_found = True)  # No results found

if __name__ == '__main__':
    app.run(debug=True)