"""

Sample bot that echoes back messages.

This is the simplest possible bot and a great place to start if you want to build your own bot.

"""

from __future__ import annotations

from typing import AsyncIterable

import fastapi_poe as fp
from modal import Image, Stub, asgi_app
import json
from GoogleNews import GoogleNews
import re
import cohere
import json
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import numpy as np
from brief import getGoogleNewsData, getArticles

class EchoBot(fp.PoeBot):
    async def get_response(
        self, request: fp.QueryRequest
    ) -> AsyncIterable[fp.PartialResponse]:
        last_message = request.query[-1].content
        input = last_message.split()
        newsdata = getGoogleNewsData(input[0], input[1])
        articles = getArticles(newsdata)
        reputed = articles["reputed"]
        unreputed = articles["unreputed"]

        out1 = "Reputed Articles --- \n"
        for article in reputed:
            out1 += "- " + article["media"] + " | " + article["title"] + " (" + article["link"] + ")\n"

        out2 = "Unreputed Articles --- \n"
        for article in unreputed:
            out2 += "- " + article["media"] + " | " + article["title"] + " (" + article["link"] + ")\n"

        yield fp.PartialResponse(text=out1 + "\n")
        yield fp.PartialResponse(text=out2)


REQUIREMENTS = ["lxml-html-clean==0.1.1", "requests==2.31.0", "fastapi-poe==0.0.36", "beautifulsoup4==4.12.3", "newspaper3k==0.2.8", "GoogleNews==1.6.14", "numpy==1.26.4", "cohere==4.34"]
image = Image.debian_slim().pip_install(*REQUIREMENTS)
stub = Stub("echobot-poe")


@stub.function(image=image)
@asgi_app()
def fastapi_app():
    bot = EchoBot()
    # Optionally, provide your Poe access key here:
    # 1. You can go to https://poe.com/create_bot?server=1 to generate an access key.
    # 2. We strongly recommend using a key for a production bot to prevent abuse,
    # but the starter examples disable the key check for convenience.
    # 3. You can also store your access key on modal.com and retrieve it in this function
    # by following the instructions at: https://modal.com/docs/guide/secrets
    # POE_ACCESS_KEY = ""
    # app = make_app(bot, access_key=POE_ACCESS_KEY)
    app = fp.make_app(bot, allow_without_key=True)
    return app
