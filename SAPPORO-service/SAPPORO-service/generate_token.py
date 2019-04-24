# coding: utf-8
import secrets
from pathlib import Path

TOKEN_FILE = Path(__file__).absolute().parent.parent.joinpath("config").joinpath("token_list.txt")
l_token = []

if TOKEN_FILE.exists() is True:
    with TOKEN_FILE.open(mode="r") as f:
        for token in f.read().split("\n"):
            if token == "":
                continue
            l_token.append(token)

token = secrets.token_urlsafe(32)
l_token.append(token)
print("Your Token is: {}".format(token))

with TOKEN_FILE.open(mode="w") as f:
    f.write("\n".join(l_token))
