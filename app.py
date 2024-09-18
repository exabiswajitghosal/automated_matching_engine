from flask import Flask, jsonify, request
import os
import shutil
from dotenv import load_dotenv
from flask_cors import CORS

import utilities
# Folder Modules
from llm import compare_source_target
# from open_ai import compare_source_target

load_dotenv()
app = Flask(__name__)
CORS(app)


@app.route('/api/upload_target_file', methods=['POST'])
def upload_target_files():
    # Check if the request contains any files
    if 'files' not in request.files:
        return jsonify({'error': 'No files part in the request'}), 400

    files = request.files.getlist('files')

    # Check if any files are selected
    if len(files) == 0:
        return jsonify({'error': 'No files selected'}), 400

    saved_files = []
    upload_folder_path = 'uploads/target'
    if os.path.exists(upload_folder_path):
        shutil.rmtree(upload_folder_path)
    os.makedirs(upload_folder_path)
    if os.path.exists('data/target'):
        shutil.rmtree('data/target')
    for file in files:
        if file.filename == '':
            return jsonify({'error': 'One or more files have no filename'}), 400
        # Check if the uploaded file is an XML file
        # if not file.filename.lower().endswith('.xml'):
        #     return jsonify({'error': 'Only XML files are allowed'}), 400
        # Save the file or process it further
        file.save(f"{upload_folder_path }/{file.filename}")
        utilities.simplify_xml_attributes(filename=file.filename, filetype='target')
        saved_files.append(file.filename)

    return jsonify({'message': 'Files successfully uploaded', 'files': saved_files}), 200



@app.route('/api/upload_source_file', methods=['POST'])
def upload_source_files():
    # Check if the request contains any files
    if 'files' not in request.files:
        return jsonify({'error': 'No files part in the request'}), 400

    files = request.files.getlist('files')

    # Check if any files are selected
    if len(files) == 0:
        return jsonify({'error': 'No files selected'}), 400

    saved_files = []
    upload_folder_path = 'uploads/source'
    if os.path.exists(upload_folder_path):
        shutil.rmtree(upload_folder_path)
    os.makedirs(upload_folder_path)
    if os.path.exists('data/source'):
        shutil.rmtree('data/source')
    for file in files:
        if file.filename == '':
            return jsonify({'error': 'One or more files have no filename'}), 400
        # Check if the uploaded file is an XML file
        # if not file.filename.lower().endswith('.xml'):
        #     return jsonify({'error': 'Only XML files are allowed'}), 400
        # Save the file or process it further
        file.save(f"{upload_folder_path}/{file.filename}")
        utilities.simplify_xml_attributes(filename=file.filename,filetype='source')
        saved_files.append(file.filename)

    return jsonify({'message': 'Files successfully uploaded', 'files': saved_files}), 200


@app.route('/api/upload_previous_file', methods=['POST'])
def upload_previous_files():
    # Check if the request contains any files
    if 'files' not in request.files:
        return jsonify({'error': 'No files part in the request'}), 400

    file = request.files['files']
    # Check if the uploaded file is an XML file
    if not file.filename.lower().endswith('.csv'):
        return jsonify({'error': 'Only XML files are allowed'}), 400
    upload_folder_path = 'data/previous_file'
    if os.path.exists(upload_folder_path):
        shutil.rmtree(upload_folder_path)
    os.makedirs(upload_folder_path)
    file.save(f"{upload_folder_path}/{file.filename}")

    return jsonify({'message': 'Files successfully uploaded', 'files': file.filename}), 200



@app.route('/api/generate_report', methods=['GET'])
def generate_data():
    try:
        response = compare_source_target()
        print(response)
        if not response:
            return jsonify({"message": "No Data Found From the files"}), 200
        return response, 200
    except Exception as e:
        return jsonify({"message": f"Unable to generate response: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
