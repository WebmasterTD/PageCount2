from flask import Flask

app = Flask(__name__)

from app import views
from app import event


if __name__ == "__main__":
    myapp.run(host='0.0.0.0')
