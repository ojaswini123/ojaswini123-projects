from flask import Flask, render_template, request, redirect, url_for
import pickle
import numpy as np

model = pickle.load(open('model.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        age = int(request.form['age'])
        gender = int(request.form['gender'])
        annual_income = float(request.form['annual_income'])
        num_purchases = int(request.form['num_purchases'])
        product_category = int(request.form['product_category'])
        time_spent = float(request.form['time_spent'])
        loyalty_program = int(request.form['loyalty_program'])
        discounts_availed = int(request.form['discounts_availed'])

        data = np.array([[age, gender, annual_income, num_purchases, product_category, time_spent, loyalty_program, discounts_availed]])

        prediction = model.predict(data)[0]
        purchase_status = "Yes" if prediction == 1 else "No"
        
        gender_name = "Male" if gender == 0 else "Female"
        product_category_name = ["Electronics", "Clothing", "Home Goods", "Beauty", "Sports"][product_category]
        loyalty_program_name = "Yes" if loyalty_program == 1 else "No"
        
        return render_template(
            'result.html',
            age=age,
            gender=gender_name,
            annual_income=annual_income,
            num_purchases=num_purchases,
            product_category=product_category_name,
            time_spent=time_spent,
            loyalty_program=loyalty_program_name,
            discounts_availed=discounts_availed,
            purchase_status=purchase_status
        )
    else:
        return "Only POST requests are allowed"

if __name__ == "__main__":
    app.run(debug=True)
