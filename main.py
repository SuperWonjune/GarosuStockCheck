import requests
from email.message import EmailMessage
import smtplib
import time

# Global variables
# Check a pickup-availability every INTERVAL seconds.
INTERVAL = 10

# Model name to consider.
# macbook air gold
# 'MWTJ2KH/A'

# 16 silver
# 'MVVK2KH/A'
MODEL = 'MWTJ2KH/A'

# Request url
# Reference : https://nuridol.net/stock_pad_kr.html
URL = 'https://www.apple.com/kr/shop/retail/pickup-message?pl=true&searchNearby=true&store=R692&parts.0=MWTJ2KH/A&parts.1=MWTL2KH/A&parts.2=MVVK2KH/A&_=1601286930637'


def is_pickup_possible(model):
  r = requests.get(URL)
  d = r.json()
  print(d['body']['stores'][0]["partsAvailability"][model])
  if r.status_code == 200 and d is not None:
    try:
      product_info = d['body']['stores'][0]["partsAvailability"][model]
      product_selection_enabled = product_info['storeSelectionEnabled']
      if product_selection_enabled:
        return True
      else:
        return False
    except Exception as e:
      print(e)
      return False
  else:
    return False
  
  
def mail_me(model):
  msg = EmailMessage()
  msg.set_content('재고가 입고되었다. : %s'% model)
  msg['Subject'] = '가로수길 애플 재고 입고 알람 : %s' % model
  msg['From'] = 'frommail'
  msg['To'] = 'tomail'

  # connect to SMTP server
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login('myemail', 'mypassword')

  # Send the message via our own SMTP server.
  server.send_message(msg)
  server.quit()
  

def main():
  while is_pickup_possible(MODEL) == False:
    time.sleep(INTERVAL)
  mail_me(MODEL)
  print('sending mail is complete.')
  
  
if __name__ == '__main__':
  main()