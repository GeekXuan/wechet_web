# -*- coding: utf-8 -*-
# filename: main.py
import web
from handle import Handle

urls = (
    r'^/wx$', 'Handle',
)

if __name__ == '__main__':
    web.config.debug = False
    app = web.application(urls, globals())
    app.run()
