from flask import Flask, jsonify, make_response
import pandas as pd

app = Flask(__name__)

#Ruta de los datos ya procesados
processed_data_route = ("/data/processed_data/data.npy")
data = pd.DataFrame(processed_data_route)

@app.route('/')
def index():
	response = make_response(jsonify(data), 200)
	response.headers["Content-Type"] = "application/json"
	return response

if __name__ == '__main__':
	app.run(host="0.0.0.0:3001")