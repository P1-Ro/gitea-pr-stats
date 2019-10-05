try:
    import config
except ImportError:
    print("Create config.py first")

from app import app  # NOQA

app.run(port=config.port, host="0.0.0.0", debug=True)
