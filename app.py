"""
Main entry point for the Make Nice Slack App.
"""
import os
import sys
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler
import logging

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import app after setting up path
from server import app

if __name__ == "__main__":
    app_token = os.environ.get("SLACK_APP_TOKEN")
    
    if not app_token:
        logger.error("SLACK_APP_TOKEN not found in environment variables")
        exit(1)
    
    # Start the app
    handler = SocketModeHandler(app, app_token)
    logger.info('⚡️ Make Nice Slack app is running!')
    handler.start()

