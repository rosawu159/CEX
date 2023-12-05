from flask import Flask, request,jsonify
from flask_cors import CORS
from testsearchforwin import searchall
from search_whois_process import work_whois_process
from search_nat104_process import work_nat104_process
import multiprocessing

app = Flask(__name__)
CORS(app, resources=r'/*')

@app.route('/', methods=['POST'])
def helloWorld():
  return "Hello, cross-origin-world!"

@app.route('/dataconvector', methods=['POST'])
def dataConvector():
    target_website = request.get_json(force=True)
    target_infomation=target_website['url']
    #a = searchall(target_infomation)
     
    result_queue = multiprocessing.Queue()
    processes = []
    process_whois = multiprocessing.Process(target=work_whois_process, args=(0,target_infomation,result_queue))
    process_nat104 = multiprocessing.Process(target=work_nat104_process, args=(1,target_infomation,result_queue))
    processes.extend([process_whois, process_nat104])
    process_whois.start()
    process_nat104.start()

    [process.join() for process in processes]
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    return jsonify(result=sum(results))

if __name__ == '__main__':
    app.run(threaded=True)
