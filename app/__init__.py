import os
from flask import Flask, make_response, jsonify, json, request, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.json']

@app.route('/')
def get_json_file():
    with open("app/static/data/total_count.json") as file:
        data = json.load(file)
        # sort json data by votes
        sortedList = sorted(data, key=lambda cream: cream['votes'], reverse=True)

        # send top five results 
        res = make_response(jsonify(sortedList[:5]),200)
        return res

@app.route('/add_votes')
def update_json_file():
    if request.method == "POST":
        upload_file = request.files['file_upload']
    
        # get file extension of upload file
        file_ext = os.path.splitext(upload_file.filename)[1]

        if file_ext in app.config['UPLOAD_EXTENSIONS']:
            try:
                read_file = upload_file.read()
                json_file = json.loads(read_file)
                
                # loop through local file and match flavor to new json file
                with open("app/static/data/total_count.json", 'r+') as file:
                    data = json.load(file)
                    
                    # find more efficient method of looping through files later
                    for oldvotes in data:
                        for updatedvotes in json_file:
                            if oldvotes['flavor'] == updatedvotes['flavor']:
                                oldvotes['votes'] += updatedvotes['votes']
                    sortedList = sorted(data, key=lambda cream: cream['votes'], reverse=True)
                    file.seek(0)
                    file.write(json.dumps(data))
                    file.truncate()
                    return redirect(url_for('get_json_file', code=200, icecream=sortedList[:5]))
            except:
                message = {
                'status': 500,
                'message': 'There was an error reading your file'
            }
            return redirect('update_json_file', message=message), 500
        else: 
            message = {
                'status': 400,
                'message': 'Please upload valid JSON file'
            }
            return redirect(url_for('update_json_file', message=message)), 400

    else:
        return redirect(url_for(update_json_file))


if __name__ == '__main__':
    app.run(debug=True)