import logging

logging.basicConfig(
    filename='game.log',  # Log file name
    level=logging.INFO,  # Logging level
    format='%(asctime)s - %(levelname)s - %(message)s'
)