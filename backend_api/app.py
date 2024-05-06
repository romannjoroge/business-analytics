from flask import Flask, jsonify, request
from models import Session, engine, text
import pandas as pd
from data_getters import get_states, get_dashboard_data
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/counties', methods=['GET'])
def counties():
    if request.method == "GET":
        states = get_states()
        return jsonify(states)
    
@app.route('/dashboard/<state>', methods=['GET'])
def dashboard(state):
    if request.method == "GET":
        state = str(state)
        dashboard_data = get_dashboard_data(state)
        return jsonify(dashboard_data)


@app.route("/data", methods=['GET'])
def data():
    if request.method == "GET":
        # Get some test data from db
        sales = []
        with Session(engine) as session:
            total_sales_query = "SELECT co.name AS county, SUM(f.quantity * f.price) FROM fact_sales f JOIN dim_stores s ON s.id = f.store_id JOIN dim_cities ci ON ci.id = s.city_id JOIN dim_counties co ON co.id = ci.county_id GROUP BY co.name"
            statement = text(total_sales_query)
            res = session.execute(statement).fetchall()
            
            for r in res:
                sales.append({"county": r[0], "sales": r[1]})

        return jsonify(sales)


@app.route('/test')
def test():
    return 'Route is reachable'