import sys
from app import app

if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except IndexError:
        port = 5000

    app.run(host="0.0.0.0", port=port)
