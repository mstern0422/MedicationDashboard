from flask import Flask, render_template
import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    # Create sample visualizations
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    # Either create a figure with subplots, or will create different plots altogether
    plt.figure(figsize=(10, 5))
    
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
    
    return render_template('index.html', plot_data=plot_data)

if __name__ == '__main__':
    app.run(debug=True)