from flask import Flask, request,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources=r'/*')

@app.route('/', methods=['POST'])
def helloWorld():
  return "Hello, cross-origin-world!"

@app.route('/dataconvector', methods=['POST'])
def dataConvector():
    #mydata = json.loads(request.args.get('mykey'))
    mydata = request.get_json(force=True)
    msg=mydata['url']
    #mydata['msg'] = "Hello Javascript."
    print msg
    return jsonify(result=msg)

if __name__ == '__main__':
    app.run()
