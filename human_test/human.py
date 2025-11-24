from flask import Flask, render_template, jsonify, request
import random, os, json, time

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
SUBMISSIONS_FOLDER = 'submissions'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SUBMISSIONS_FOLDER, exist_ok=True)

@app.route('/')
def index():
    """渲染前端页面"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_json():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and (file.filename.endswith('.json')):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                return jsonify({'error': f'Invalid JSON line: {str(e)}'}), 400
    
        return jsonify({
            'filename': file.filename,
            'data': data
        })
    
    return jsonify({'error': 'Invalid file type'}), 400
        
        
@app.route('/uselocal', methods=['POST'])
def use_local():
    response = request.get_json()
    local_path = response.get('localdir', None)
    filepath = os.path.join(os.getcwd(), local_path.strip())
    if not os.path.exists(filepath):
        return jsonify({'error': 'File does not exist'}), 404
    
    if not filepath.endswith('.json'):
        return jsonify({'error': 'File is not a JSON file'}), 400
    
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            return jsonify({'error': f'Invalid JSON line: {str(e)}'}), 400
    
    return jsonify({
        'filename': os.path.basename(filepath),
        'data': data,
        'success': True,
    })        
        
        
@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.get('metaData', None)
    filename = request.form.get('filename', 'submission.json')
    filepath = os.path.join(SUBMISSIONS_FOLDER, f"submission_{int(time.time())}.json")
    
    json_data = json.loads(data) 
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    return jsonify({
        'message': 'File submitted successfully',
        'filepath': filepath,
        'success': True,
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', 
            debug=True)