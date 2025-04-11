import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import pyshorteners
import os

IMAGE_DIR = "static/images"

def send_email(email, product_name, current_price, url):
    try:
        short_url = pyshorteners.Shortener().tinyurl.short(url)

        msg = MIMEMultipart()
        msg['From'] = 'hellomano225@gmail.com'
        msg['To'] = email
        msg['Subject'] = f'Price Alert for {product_name}'

        body = f"""
        <html>
        <body>
            <h3>Price Alert!</h3>
            <p>The price for <strong>{product_name}</strong> has dropped below your expected price.</p>
            <p><strong>Current Price:</strong> ₹{current_price}</p>
            <p><a href="{short_url}">Check the product here</a></p>
        </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        with open(os.path.join(IMAGE_DIR, 'price_trend.png'), 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-Disposition', 'attachment', filename='price_trend.png')
            msg.attach(img)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('hellomano225@gmail.com', 'mlpzufoqzpzikvvd')
            server.sendmail(msg['From'], msg['To'], msg.as_string())

        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")
