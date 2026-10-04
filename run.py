import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # In production on Vercel, this block will not be executed.
    # Vercel will directly import 'app' from run.py
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
