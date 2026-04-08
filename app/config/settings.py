import os
from dotenv import load_dotenv

load_dotenv()

THREADS_API_KEY = os.getenv("THREADS_API_KEY")
OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")