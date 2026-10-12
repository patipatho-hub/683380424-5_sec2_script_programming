# main.py
import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base_dir, 'src'))

try:
    from src.utils import setup_logging
except ImportError:
    from utils import setup_logging

logger = setup_logging(__name__)

from config_parser import ConfigParser
from spreadsheet_agent import SpreadsheetAgent

def main():
    config_file_path = os.path.join(base_dir, 'configs', 'example_spreadsheet_config.json')
    try:
        os.makedirs(os.path.join(base_dir, 'data'), exist_ok=True)
        logger.info(f"Loading configuration from: {config_file_path}")
        config_parser = ConfigParser(config_file_path)
        config = config_parser.load_config()
        
        # Ensure relative paths are resolved relative to base_dir
        if not os.path.isabs(config.get("input_file", "")):
            config["input_file"] = os.path.normpath(os.path.join(base_dir, config["input_file"]))
        if not os.path.isabs(config.get("output_file", "")):
            config["output_file"] = os.path.normpath(os.path.join(base_dir, config["output_file"]))

        input_file_path = config.get("input_file")
        if not os.path.exists(input_file_path):
            logger.critical(f"Input file not found: '{input_file_path}'")
            return
        
        logger.info("Initializing Spreadsheet Agent...")
        agent = SpreadsheetAgent(config)
        logger.info("Running Spreadsheet Agent...")
        agent.run()
    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)

if __name__ == "__main__":
    main()
