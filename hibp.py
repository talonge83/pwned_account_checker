import requests
import hashlib, binascii
import os

from dotenv import load_dotenv
load_dotenv()

#####TODO add email and pw to a SQL database

API_KEY = os.getenv("API_KEY")

pw_check_headers = {
     "Add-Padding": "True"
}

print("""
                    What would you like to search for? 
                    1. email
                    2. Password
                    """)
email_or_pw = input("Please select a number: ")

##Check if an email has been compromised

if email_or_pw == "1":
     user_email = input("What is the email you would like to check? ")

     headers = {
     "hibp-api-key": API_KEY
     }

     response = requests.get(url=f"https://haveibeenpwned.com/api/v3/breachedaccount/{user_email}", headers=headers)

     if response.status_code == 200:
          print("Sorry, your account has been compromised :(")
     elif response.status_code == 404:
          print("Your account is safe! Check back regularly to keep track!")
     elif response.status_code == 401:
          print("Sorry, your API key is invalid or you need to pay for a subscription to use this feature")

     print(type(response))
     print(response.text["name"])
     print(type(response.text))

##Check if a password has been compromised

elif email_or_pw == "2":
     pw = input("Please enter a password to check: ")
     pw_encoded = pw.encode("utf_8", "strict")
     pw_hashed = hashlib.sha1(pw_encoded).hexdigest()
     hash_prefix = pw_hashed[:5]
     hash_suffix = pw_hashed[5:]
     response = requests.get(url=f"https://api.pwnedpasswords.com/range/{hash_prefix}", headers=pw_check_headers)
     if response.status_code == 200:
          ## Check for entire hash value
          if hash_suffix.upper() in response.text:
               print("Sorry, this password has been compromised")
               ##Add password to SQL DB
          else:
               print("This password is still good to use!")


