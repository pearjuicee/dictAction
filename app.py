from flask import Flask
from views import views

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'

    app.register_blueprint(views)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)

