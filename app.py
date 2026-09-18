from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Load the data
file_path = r"C:\Users\audre\Downloads\my_flask_app\data\2024_ExpendituresExtract.csv"
data = pd.read_csv(file_path, encoding='latin1')
filtered_data = data[data['CandidateName'].notna()]
filtered_data = filtered_data[['CandidateName', 'ExpenditureAmount', 'ExpenditureDate', 'LastName', 'FirstName', 'Explanation', 'Purpose']]

@app.route('/')
def index():
    candidates = sorted(filtered_data['CandidateName'].unique(), key=lambda x: x[0] if x else "")
    return render_template('index.html', candidates=candidates)

@app.route('/expenditures', methods=['GET'])
def expenditures():
    candidate = request.args.get('candidate')
    if candidate:
        candidate_data = filtered_data[filtered_data['CandidateName'] == candidate].fillna('')
        total_expenditure = candidate_data['ExpenditureAmount'].sum()
        return render_template('expenditures.html', candidate=candidate, expenditures=candidate_data.to_dict(orient='records'), total_expenditure=total_expenditure)
    return "No candidate selected"

if __name__ == '__main__':
    app.run(debug=True)