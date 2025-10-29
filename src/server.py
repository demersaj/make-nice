"""
Make Nice Slack App - Server
"""
import os
import logging
from slack_bolt import App
from dotenv import load_dotenv
from llm_handler import LLMHandler

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Slack app
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


@app.command("/make-nice")
def handle_make_nice(ack, respond, command):
    """Handle the /make-nice slash command."""
    ack()
    
    text = command.get('text', '')
    
    if not text:
        respond(
            response_type='ephemeral',
            text='Please provide a message to make nice. Usage: `/make-nice <your message>`'
        )
        return
    
    try:
        # Initialize LLM handler
        llm_endpoint = os.environ.get('LLM_API_ENDPOINT')
        llm_api_key = os.environ.get('LLM_API_KEY')
        llm_model = os.environ.get('LLM_MODEL', 'default')
        llm_api_type = os.environ.get('LLM_API_TYPE', 'openai')
        
        logger.info(f'LLM Config - Endpoint: {llm_endpoint}, Type: {llm_api_type}, Model: {llm_model}')
        
        llm_handler = LLMHandler({
            'endpoint': llm_endpoint,
            'apiKey': llm_api_key,
            'model': llm_model,
            'maxTokens': int(os.environ.get('LLM_MAX_TOKENS', 500)),
            'apiType': llm_api_type
        })
        
        # Transform the message using the LLM
        logger.info(f'Transforming message: {text[:50]}...')
        improved_message = llm_handler.transform_message(text)
        
        # Respond to the Slack channel with the improved message
        respond(
            response_type='in_channel',
            text=improved_message
        )
    
    except ValueError as error:
        error_message = f'Configuration error: {str(error)}'
        logger.error(f'Error in /make-nice command: {error_message}')
        respond(
            response_type='ephemeral',
            text=error_message
        )
    
    except ConnectionError as error:
        error_message = f'Sorry, I encountered an error processing your message. {str(error)}'
        logger.error(f'Error in /make-nice command: {error_message}')
        respond(
            response_type='ephemeral',
            text=error_message
        )
    
    except Exception as error:
        error_message = f'Sorry, I encountered an error processing your message. {str(error)}'
        logger.error(f'Error in /make-nice command: {error_message}', exc_info=True)
        respond(
            response_type='ephemeral',
            text=error_message
        )


@app.error
def global_error_handler(error, body, logger):
    """Global error handler."""
    logger.error(f'Slack app error: {error}')

