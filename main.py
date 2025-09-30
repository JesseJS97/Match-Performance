"""
Created by Jesse Scully
Date: 15/09/2025
Influenced by: Python Website Full Tutorial by Tech With Tim
Link: https://www.youtube.com/watch?v=dam0GPOAvVI
"""

# Execute/Run the web server
from website import create_app

app = create_app()

# Ensure web server is only run if main.py is executed
if __name__ == '__main__':
    app.run(debug=True)