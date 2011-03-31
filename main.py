# -*- coding: utf-8 -*-
from bottle import run, debug

import controllers

DEBUG = True

debug(DEBUG)
run(host='localhost', port=8080, reloader=DEBUG)

