import os
from flask import Flask, make_response, jsonify, json, request, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.json']

def returnSortedList(data):
    # sort json data by votes
    sortedList = sorted(data, key=lambda cream: cream['votes'], reverse=True)
    icecream = sortedList[:5]
    return(icecream)

@app.route('/api/', methods=['GET'])
def get_json_file():
    with open("app/static/data/total_count.json") as file:
        data = json.load(file)

        # send top five results 
        res = make_response(jsonify(returnSortedList(data)),200)
        return res

@app.route('/api/add_votes/', methods=['GET', 'POST'])
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
                    file.seek(0)
                    file.write(json.dumps(data))
                    file.truncate()
                    return redirect(url_for('get_json_file', code=200, icecream=returnSortedList(data)))
            except:
                message = {
                'status': 500,
                'message': 'There was an error reading your file'
            }
            return redirect('update_json_file', message=message), 500
        else: 
            # file is not json file
            message = {
                'status': 400,
                'message': 'Please upload valid JSON file'
            }
            return redirect(url_for('update_json_file', message=message)), 400

    else:
        # if request is a GET route
        # rr = {"some": "data"}
        # res = make_response(jsonify(rr), 200)
        message={
            'status': 400,
            "message": 'Not a valid method for this route'
        }
        return make_response(jsonify(message), 400)


if __name__ == '__main__':
    app.run(debug=True)