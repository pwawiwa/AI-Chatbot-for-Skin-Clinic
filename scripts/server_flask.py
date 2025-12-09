#!/usr/bin/env python
"""
Flask server entry point — run WhatsApp webhook and chatbot server
"""
import sys
from pathlib import Path
import os

# Ensure project root is on sys.path so `src` can be imported when running script directly
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.server_flask import app


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    print(f"🚀 Starting server on port {port}")
    print(f"📡 Server will be available at: http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
#!/usr/bin/env python
"""
Flask server entry point — run WhatsApp webhook and chatbot server
"""
from src.server_flask import app

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8080))
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    print(f"🚀 Starting server on port {port}")
    print(f"📡 Server will be available at: http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
