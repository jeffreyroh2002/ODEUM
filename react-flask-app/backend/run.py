from api import create_app, db
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = create_app()

if __name__ == "__main__":
    if os.environ.get("FLASK_ENV") == "production":
        # Determine the number of worker processes based on available CPU cores
        num_workers = os.cpu_count() * 2 + 1 if os.cpu_count() else 1

        # Start the Gunicorn server
        bind_address = '0.0.0.0:' + str(os.environ.get("PORT", 5000))
        os.system(f'gunicorn -w {num_workers} -b {bind_address} "run:create_app()"')
    else:
        # For development, run the Flask development server
        debug = True
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port, debug=debug)