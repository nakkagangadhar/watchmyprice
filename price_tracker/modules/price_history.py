import matplotlib
matplotlib.use('Agg')  # Must be before importing pyplot
import matplotlib.pyplot as plt
import random
import os
from datetime import datetime, timedelta
import uuid

IMAGE_DIR = "static/images"

def generate_historical_prices(current_price):
    prices = [current_price + random.uniform(-100, 100) for _ in range(30)]
    dates = [(datetime.now() - timedelta(days=i)).strftime('%d-%m') for i in range(30)][::-1]

    fig, ax = plt.subplots()
    ax.plot(dates, prices, marker='o')
    ax.set_title('Price Trend for Product')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (₹)')
    plt.xticks(rotation=45)

    os.makedirs(IMAGE_DIR, exist_ok=True)
    unique_filename = f'price_trend_{uuid.uuid4().hex}.png'
    img_path = os.path.join(IMAGE_DIR, unique_filename)

    plt.tight_layout()
    plt.savefig(img_path)
    plt.close(fig)

    return prices, img_path