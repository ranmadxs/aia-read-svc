from dotenv import load_dotenv
import os
load_dotenv()
print(os.environ['YAHOO_USER'])
print(os.environ['YAHOO_PASSWORD'])