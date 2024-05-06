from typing import List
from models import Session, engine, text, select, DimCounty

def get_states() -> List[str]:
    states = []
    with Session(engine) as session:
        res = session.execute(
            select(DimCounty.name).order_by(DimCounty.name)
        ).fetchall()
        
        for r in res:
            states.append(r[0])

    return states

def get_dashboard_data(state: str):
    total_sales = 0
    number_of_products_sold = 0
    number_of_stores = 0
    number_of_product_categories = 0
    number_of_employees = 0
    sales_for_year = []
    top_5_products = []
    top_5_stores = []
    top_5_categories = []
    top_5_cities = []

    # Get total sales for a county
    with Session(engine) as session:
        total_sales_query = text("SELECT SUM(quantity * price) FROM fact_sales f JOIN dim_stores s ON s.id = f.store_id JOIN dim_cities ci ON ci.id = s.city_id JOIN dim_counties co ON co.id = ci.county_id WHERE co.name = :county")
        res = session.execute(total_sales_query, {"county": state}).fetchall()
        total_sales = res[0][0]

        # Get number of products sold
        number_products_sold_query = text("SELECT SUM(f.quantity) FROM fact_sales f JOIN dim_stores s ON s.id = f.store_id JOIN dim_cities ci ON ci.id = s.city_id JOIN dim_counties co ON co.id = ci.county_id WHERE co.name = :county")
        res = session.execute(number_products_sold_query, {"county": state}).fetchall()
        number_of_products_sold = res[0][0]

        # Get number of stores
        number_of_stores_query = text("SELECT COUNT(*) FROM dim_stores s JOIN dim_cities ci ON ci.id = s.city_id JOIN dim_counties co ON co.id = ci.county_id WHERE co.name = :county")
        res = session.execute(number_of_stores_query, {"county": state}).fetchall()
        number_of_stores = res[0][0]

        # Get number of product categories
        number_of_product_categories_query = text("SELECT COUNT(DISTINCT ca.id) FROM fact_sales f JOIN dim_products p ON p.id = f.product_id JOIN dim_product_categories ca ON ca.id = p.category_id JOIN dim_stores s ON f.store_id = s.id JOIN dim_cities ci ON ci.id = s.city_id JOIN dim_counties co ON co.id = ci.county_id WHERE co.name = :county")
        res = session.execute(number_of_product_categories_query, {"county": state}).fetchall()
        number_of_product_categories = res[0][0]

        # Get number of employees
        number_of_employees_query = text("SELECT COUNT(*) FROM dim_employees e JOIN dim_stores s ON s.id = e.store_id JOIN dim_cities ci ON ci.id = s.city_id JOIN dim_counties co ON co.id = ci.county_id WHERE co.name = :county")
        res = session.execute(number_of_employees_query, {"county": state}).fetchall()
        number_of_employees = res[0][0]

        # Sales for year
        sales_for_year_query = text("SELECT SUM(quantity * price) as sales, TO_CHAR(DATE_TRUNC('month', TO_DATE(time, 'MM/DD/YYYY')), 'Month') AS month FROM fact_sales f JOIN dim_stores s ON s.id = f.store_id JOIN dim_cities ci ON ci.id = s.city_id JOIN dim_counties co ON co.id = ci.county_id WHERE co.name = :county GROUP BY month ORDER BY month DESC LIMIT 5")
        res = session.execute(sales_for_year_query, {"county": state}).fetchall()
        for r in res:
            sales_for_year.append({"sales": r[0], "month":r[1]})

        # Top 5 products
        top_5_products_query = text("SELECT p.name, SUM(quantity * price) AS sales FROM fact_sales f JOIN dim_products p ON p.id = f.product_id JOIN dim_stores s ON s.id = f.store_id JOIN dim_cities ci ON ci.id = s.city_id JOIN dim_counties co ON co.id = ci.county_id WHERE co.name = :county GROUP BY p.name ORDER BY sales DESC LIMIT 5")
        res = session.execute(top_5_products_query, {"county": state}).fetchall()
        for r in res:
            top_5_products.append({"product": r[0], "sales": r[1]})

        # Top 5 stores
        top_5_stores_query = text("SELECT s.name, SUM(quantity * price) AS sales FROM fact_sales f JOIN dim_stores s ON s.id = f.store_id JOIN dim_cities ci ON ci.id = s.city_id JOIN dim_counties co ON co.id = ci.county_id WHERE co.name = :county GROUP BY s.name ORDER BY sales DESC LIMIT 5")
        res = session.execute(top_5_stores_query, {"county": state}).fetchall()
        for r in res:
            top_5_stores.append({"store": r[0], "sales": r[1]})

        # Top 5 categories
        top_5_categories_query = text("SELECT ca.name, SUM(quantity * price) AS sales FROM fact_sales f JOIN dim_products p ON p.id = f.product_id JOIN dim_product_categories ca ON ca.id = p.category_id JOIN dim_stores s ON s.id = f.store_id JOIN dim_cities ci ON ci.id = s.city_id JOIN dim_counties co ON co.id = ci.county_id WHERE co.name = :county GROUP BY ca.name ORDER BY sales DESC LIMIT 5")
        res = session.execute(top_5_categories_query, {"county": state}).fetchall()
        for r in res:
            top_5_categories.append({"category": r[0], "sales": r[1]})

        # Top 5 cities
        top_5_cities_query = text("SELECT ci.name, SUM(quantity * price) AS sales FROM fact_sales f JOIN dim_stores s ON s.id = f.store_id JOIN dim_cities ci ON ci.id = s.city_id JOIN dim_counties co ON co.id = ci.county_id WHERE co.name = :county GROUP BY ci.name ORDER BY sales DESC LIMIT 5")
        res = session.execute(top_5_cities_query, {"county": state}).fetchall()
        for r in res:
            top_5_cities.append({"city": r[0], "sales": r[1]})

    return {
        "total_sales": total_sales,
        "number_of_products_sold": number_of_products_sold,
        "number_of_stores": number_of_stores,
        "number_of_product_categories": number_of_product_categories,
        "number_of_employees": number_of_employees,
        "sales_for_year": sales_for_year,
        "top_5_products": top_5_products,
        "top_5_stores": top_5_stores,
        "top_5_categories": top_5_categories,
        "top_5_cities": top_5_cities
    }
