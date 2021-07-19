#!/bin/bash

pyenv local
export FLASK_ENV=development
app1="python server.py 5000"
app2="python server.py 5001"
app3="python server.py 5002"
app4="python server.py 5003"

(trap 'kill 0' SIGINT; $app1 & $app2 & $app3 & $app4)
