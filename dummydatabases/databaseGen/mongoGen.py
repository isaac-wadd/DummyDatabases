
import os, random as r
from pathlib import Path
from .models import *
from datetime import datetime
from string import ascii_letters, digits
from django.conf import settings

ALL_CHARS = ascii_letters + digits
BASE_DIR = Path(__file__).resolve().parent.parent

def generateMongodbFile(schema, tableData):
    return
