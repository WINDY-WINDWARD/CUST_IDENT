import pyqrcode
from pyqrcode import QRCode
import os
from dotenv import load_dotenv
import io

load_dotenv()
def generateQR(s):
    # get web_page from .env 
    a = os.environ.get('WEB_PAGE')
    print(a)
    a = a+"getCustomer/signUp?key="+s
    # Generate QR code
    url = pyqrcode.create(a)
    buffer = io.BytesIO()
    url.svg(buffer, scale=8)
    return buffer.getvalue()

# generateQR("1234567890")