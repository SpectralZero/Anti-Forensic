#!/usr/bin/env python3
"""
main.py
ANTI-FORENSIC TOOLKIT 
Standalone digital forensic countermeasure tool
"""

import sys
import os
import logging
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ui.main_window import AntiForensicApp

def setup_logging():
    """Setup comprehensive logging"""
    log_dir = project_root / "logs"
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "anti_forensic_toolkit.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Main entry point"""
    setup_logging()
    
    try:
        app = AntiForensicApp()
        app.run()
    except Exception as e:
        logging.critical(f"Application failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()