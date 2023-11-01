#!/bin/bash

python3 -m ensurepip --upgrade

python3 -m venv .venv

source .venv/bin/activate

.venv/bin/pip3 install -r requirements.txt

uvicorn main:app --host 127.0.0.1 --port 5000