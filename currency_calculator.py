import requests
import csv
from flask import Flask, render_template, request

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
rates = data[0]["rates"]
file_name = "rates.csv"

with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["currency", "code", "bid", "ask"], delimiter=";")
    writer.writeheader()
    for rate in rates:
        writer.writerow(rate)

def load_currencies_from_csv(file_name):
    currencies = {}
    with open(file_name, newline="", encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        next(reader)
        for row in reader:
            currency_name = row[1]
            exchange_rate = float(row[3])
            currencies[currency_name] = exchange_rate
    return currencies

def convert_currency(amount, to_currency, currencies):
    exchange_rate = currencies[to_currency]
    result = amount * exchange_rate
    return result

currencies = load_currencies_from_csv('rates.csv')

app = Flask(__name__)

@app.route('/calculator', methods=['GET', 'POST'])
def currency_calculator():
    if request.method == 'GET':
       print("We received GET")
       return render_template("calculator_template.html", currencies=currencies)
    elif request.method == 'POST':
        data = list(request.form.values())
        amount = data[0]
        to_currency = data[1]
        result = convert_currency(float(amount), to_currency, currencies)
        return  render_template("calculator_template.html", result=result, currencies=currencies)

if __name__ == '__main__':
    app.run(debug=True)