from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('popup.html')
@app.route('/d', methods=['GET'])
def dataConvector():
    data = json.loads(request.form.get('data'))
    mydata['msg'] = "Hello Javascript."
    print(mydata)
    return jsonify(result=mydata+data)
if __name__ == "__main__":
    app.run(debug=True)
