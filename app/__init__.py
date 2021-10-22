from flask import Flask, make_response, jsonify, json

app = Flask(__name__)

@app.route('/')
def get_json_file():
    with open("app/static/data/total_count.json") as file:
        data = json.load(file)
        # sort json data by votes
        sortedList = sorted(data, key=lambda cream: cream['votes'], reverse=True)

        # send top five results 
        res = make_response(jsonify(sortedList[:5]),200)
        return res

if __name__ == '__main__':
    app.run(debug=True)