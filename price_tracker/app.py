from flask import Flask, request, jsonify, render_template
import os
import traceback
from modules.price_checker import check_price

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_price', methods=['POST'])
def check_price_route():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        result = check_price(data)
        print(f"check_price returned: {result}")  
        
        
        if isinstance(result, tuple) and len(result) == 2:
            return jsonify(result[0]), result[1]
        else:
            raise ValueError(f"check_price returned unexpected value: {result}")
            
    except Exception as e:
        print(f"Error in check_price_route: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)