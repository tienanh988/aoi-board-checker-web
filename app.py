from flask import Flask, render_template, request, jsonify
import os, csv, uuid
app = Flask(__name__)
UPLOAD = 'uploads'; RESULT = 'results'
os.makedirs(UPLOAD, exist_ok=True); os.makedirs(RESULT, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    f=request.files['image']
    fname=str(uuid.uuid4())+'_'+f.filename
    path=os.path.join(UPLOAD,fname)
    f.save(path)
    return jsonify({'filename':fname})

@app.route('/save', methods=['POST'])
def save():
    data=request.json
    fname=os.path.join(RESULT, f"{data['image']}.csv")
    with open(fname,'w',newline='') as csvf:
        w=csv.writer(csvf); w.writerow(['x','y','w','h','label'])
        for b in data['boxes']: w.writerow([b['x'],b['y'],b['w'],b['h'],b['label']])
    return jsonify({'status':'ok'})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
