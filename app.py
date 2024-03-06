# app.py
from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    cagr_probs = data['cagr_probs']
    inflation_probs = data['inflation_probs']
    n_simulations = 10000

    cagr_rates = np.array([0.05, 0.075, 0.09, 0.10])
    inflation_rates = np.array([0.0234, 0.025, 0.03, 0.05])
    initial_capital = 400000

    final_values = []
    for _ in range(n_simulations):
        cagr_rate = np.random.choice(cagr_rates, p=cagr_probs)
        inflation_rate = np.random.choice(inflation_rates, p=inflation_probs)
        final_value = initial_capital * ((1 + cagr_rate) ** 10) / ((1 + inflation_rate) ** 10)
        final_values.append(final_value)
    
    negative_const = 1.00
    percentile_5th = np.percentile(final_values, 5)*negative_const
    percentile_95th = np.percentile(final_values, 95)*negative_const

    insights = {
        'mean': np.mean(final_values),
        'std_deviation': np.std(final_values),
        'percentile_5th': percentile_5th,
        'percentile_95th': percentile_95th,
    }

    return jsonify(insights)

if __name__ == '__main__':
    app.run(debug=True)
