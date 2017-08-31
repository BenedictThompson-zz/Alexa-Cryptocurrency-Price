 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import logging, os, sys, config, ngrok
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from coinmarketcap import Market
coinmarketcap = Market()
reload(sys)
crypto = config.crypto
os.spawnl(os.P_DETACH, 'ngrok http 5000')
ngrok.client.BASE_URL = "http://localhost:5000"
tunnel = ngrok.client.get_tunnels()[-1]
url = tunnel['public_url']
print "Public URL is: " + url
sys.setdefaultencoding('utf8')
app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)
quitkeywords = ['quit', 'exit', 'cancel', 'leave']

@ask.launch

def start():
    print "here"

    welcome_msg = render_template('welcome', crypto = crypto)

    return question(welcome_msg)


@ask.intent("YesIntent", convert={'yon': str})
def menu(yon):
    print yon
    round_msg = render_template('round_msg', crypto = crypto)
    help = render_template('help', crypto = crypto)
    if yon == 'help':
        print "here"
        return question(help)
    if yon in quitkeywords:
        return statement("")
    return question(round_msg)

        

@ask.intent("AnswerIntent")

def response():
        price = coinmarketcap.ticker(crypto, limit=1)
        price = price[0]
        price = str(price["price_usd"])
        priceresponse = render_template('priceresponse', crypto = crypto , price = price)
        return statement(priceresponse) \
            .simple_card(title=crypto.title()+' Price', content="The " + crypto + " price is " + price + " dollars")
@ask.session_ended
def session_ended():
    return statement("")
if __name__ == "__main__":
    app.run(debug=True)