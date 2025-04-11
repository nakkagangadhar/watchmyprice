from modules.price_parser import parse_product_page
from modules.price_history import generate_historical_prices
from modules.email_service import send_email

def check_price(data):
    if not all(k in data for k in ['url', 'expected_price', 'email']):
        return {"error": "Missing required fields"}, 400

    url = data.get('url')
    try:
        expected_price = float(data.get('expected_price'))
    except (ValueError, TypeError):
        return {"error": "Invalid expected_price"}, 400
    user_email = data.get('email')

    product_name, current_price = parse_product_page(url)

    if current_price is None:
        return {"error": "Could not retrieve product price"}, 500

    historical_prices, img_path = generate_historical_prices(current_price)

    if current_price <= expected_price:
        send_email(user_email, product_name, current_price, url)

    return {
        "product_name": product_name,
        "current_price": current_price,
        "graph_url": f"/{img_path}",
        "message": "Product data retrieved successfully."
    }, 200