import axios from "axios"
const apiURL = "http://127.0.0.1:5000"
export interface DashboardData {
    employees: number,
    productCategories: number,
    productsSold: number,
    stores: number,
    totalSales: number,
    salesForYear: {month: string, sales: number}[]
    topCategories: {category: string, sales: number}[],
    topCities: {city: string, sales: number}[]
    topProducts: {product: string, sales: number}[]
    topStores: {store: string, sales: number}[]
}

export async function getDashboardData(state: string): Promise<DashboardData> {
    try {
        const serverRes = await axios.get(`${apiURL}/dashboard/${state}`)
        
        if (serverRes.status != 200) {
            console.log(serverRes.data);
            throw "Error Getting Data"
        }

        const json = serverRes.data;
        return {
            employees: json['number_of_employees'] ?? 0,
            productCategories: json['number_of_product_categories'] ?? 0,
            productsSold: json['number_of_products_sold'] ?? 0,
            stores: json['number_of_stores'] ?? 0,
            totalSales: json['total_sales'] ?? 0,
            salesForYear: json['sales_for_year'] ?? [],
            topCategories: json['top_5_categories'] ?? [],
            topCities: json['top_5_cities'] ?? [],
            topProducts: json['top_5_products'] ?? [],
            topStores: json['top_5_stores'] ?? []
        }
    } catch(err) {
        console.log(err);
        throw "Could Not Get Dashboard Data";
    }
}