import sys
import os
from PyQt6.QtWidgets import QApplication
from gui.main_window import NotaryApp
from database.models import init_db

def main():
    # Initialize database
    init_db()
    
    # Start Application
    app = QApplication(sys.argv)
    
    # Set application style (optional)
    app.setStyle("Fusion")
    
    window = NotaryApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
