#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application import app, manager
from flask_script import Server
from jobs.launcher import runJob
import www

# web server
manager.add_command("runserver", Server(host='0.0.0.0', port=app.config["SERVER_PORT"], use_debugger=True,
                                        use_reloader=True))

manager.add_command("runjob", runJob())


def main():
    app.config['JSON_AS_ASCII'] = False
    manager.run()


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        import sys

        sys.exit(main())
    except Exception as e:
        import traceback

        traceback.print_exc()
