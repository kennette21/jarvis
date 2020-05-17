from selenium import webdriver
import json

with open('secrets.json') as json_file:
    secrets = json.load(json_file)

# open a chrome window
driver = webdriver.Chrome()

# go to audible library
driver.get("https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&") # location of audible library page

# probably need to log in
user = secrets["audible_user"]
pwd = secrets["audible_pwd"]

user_input = driver.find_element_by_id("ap_email")
user_input.send_keys(user)

continue_btn = driver.find_element_by_id("continue")
continue_btn.submit()

pwd_input = driver.find_element_by_id("ap_password")
pwd_input.send_keys(pwd)

signin_btn = driver.find_element_by_id("signInSubmit")
signin_btn.submit()

### BAH. no shot. Security captcha asks you to read the image. Thought that would happen.
### Ah well. nice dable in selenium, and turns out I can just install an Alexa on the Pi anyway.
### Alexa and Jarvis will live together. I don't see why not. Might have to have Jarvis activate some alexa comands.


# click on listen now of first book 
## eventual improvment would be to parse and list all book titles