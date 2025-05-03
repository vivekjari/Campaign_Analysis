import os
import pandas as pd
from flask import Flask, request, jsonify
from data_processing import generate_insights

app = Flask(__name__)

# Route to process campaign data and generate insights
@app.route('/process', methods=['POST'])
def process_data():
    file = request.files.get('file')
    
    if not file:
        return jsonify({"error": "No file provided"}), 400

    try:
        # Read the uploaded file as a pandas dataframe
        df = pd.read_csv(file)

        # Generate insights using the data processing logic
        insights = generate_insights(df)

        # Return the generated insights as a JSON response
        return jsonify(insights)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

