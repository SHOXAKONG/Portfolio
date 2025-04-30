#!/bin/sh
set -e
gunicorn config.wsgi --log-file -