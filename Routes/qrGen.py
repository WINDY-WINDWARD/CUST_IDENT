import pyqrcode
from pyqrcode import QRCode
import os

def generateQR(s):
    # get web_page from .env 
    a = os.environ.get('WEB_PAGE')
    a = a+"/getCustomer/login?key="+s
    # Generate QR code
    url = pyqrcode.create(s)
    # Create and save the svg file naming "myqr.svg"
    return url.svg("myqr.svg", scale = 8)