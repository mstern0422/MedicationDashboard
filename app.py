from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import base64
from io import BytesIO
import re
import pdfplumber

app = Flask(__name__)

# Load the drug data once when the app starts
data = pd.read_csv('Medicine_Details.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    drug_name = request.form['drug_name']
    # data = medi
    drug_info = data[data['Medicine Name'].str.contains(drug_name, case = False, na = False)]
    
    if not drug_info.empty:
        # If drug info found, will transform the info to a dictionary. This step may not be needed
        drug_info = drug_info.iloc[0].to_dict()

    # First plot: Side effects, word cloud?
    

    # Second plot: Graph plot with positive, neutral, negative reviews

    # Third plot: Drug composition, Pie chart 

    # Fourth plot: Side effects, this will just be a list of most common to least

    # Not a plot, but item containing image of the medication

    # Different dataset will be utilized here to show drug/drug interactions

    # Convert plot to base64 string

        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        plot_data = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
    else:
        drug_info = None  # No results found
    
    return render_template('index.html', plot_data=plot_data)

if __name__ == '__main__':
    app.run(debug=True)