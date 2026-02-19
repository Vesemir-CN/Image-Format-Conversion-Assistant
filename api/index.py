# Vercel Python Flask Entry Point
import os
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel requires the app object to be exposed
handler = app
