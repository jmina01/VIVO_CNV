#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)

sys.path.insert(0, "/home/jmina/VIVO_CNV")
from app import app as application
