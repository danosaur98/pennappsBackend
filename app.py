from flask import Flask

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'curatordb'
app.config['MONGO_URI'] = 'mongodb://admin:password@ds125906.mlab.com:25906/curatordb'


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)
