from flask import Flask, request, jsonify
from flask_cors import CORS
from search_whois_process import work_whois_process
from search_nat104_process import work_nat104_process
from search_target_process import work_target_process
import multiprocessing
from queue import Queue

app = Flask(__name__)
CORS(app)

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
    process_target = multiprocessing.Process(target=work_target_process, args=(0,target_infomation,result_queue))
    process_whois = multiprocessing.Process(target=work_whois_process, args=(1,target_infomation,result_queue))
    process_nat104 = multiprocessing.Process(target=work_nat104_process, args=(2,target_infomation,result_queue))
    processes.extend([process_whois, process_nat104, process_target])
    process_target.start()
    process_whois.start()
    process_nat104.start()

    [process.join() for process in processes]
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
    total_score = 0
    for item in results:
      for key in item:
          if 'score' in key:
              # 將包含 'score' 的值加到總和
              total_score += item[key]
    print("total_score", total_score)
         

    return jsonify(result=results)

if __name__ == '__main__':
    app.run(debug=True)
