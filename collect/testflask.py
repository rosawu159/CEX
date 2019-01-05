from flask import Flask, request,jsonify
from flask_cors import CORS
from testsearchforwin import searchall

app = Flask(__name__)
CORS(app, resources=r'/*')

@app.route('/', methods=['POST'])
def helloWorld():
  return "Hello, cross-origin-world!"

@app.route('/dataconvector', methods=['POST'])
def dataConvector():
    mydata = request.get_json(force=True)
    msg=mydata['url']
    print msg
    a = searchall(msg)
    print a
    return jsonify(result=a)

if __name__ == '__main__':
    app.run()
