# Require a project dependency
import flask


app = flask.Flask(__name__)

    # Define a simple route
@app.route('/')
def home():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)