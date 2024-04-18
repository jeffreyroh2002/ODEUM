from api import create_app, db
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)