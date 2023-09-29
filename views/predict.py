from flask import Flask, jsonify, request, Response,json,render_template
from flask_mongoengine import MongoEngine
from mongoengine import *
from werkzeug.utils import secure_filename
import os,os.path
from bson.dbref import DBRef
from datetime import datetime
from h2o.automl import H2OAutoML
from flask_swagger_ui import get_swaggerui_blueprint
import h2o
from h2o.automl import H2OAutoML
from flask_cors import CORS  # Import CORS from flask_cors


app = Flask(__name__)
CORS(app)
## swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger_predict.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Workspaces_H2O_Flask-REST-Api"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

@app.route('/predict/<model>',methods=['POST'])    # prediction by choosing the model key
def predict(model):
         h2o.init()
         item_dict = {}
         model_name = os.path.join("ML_models", model)
         uploaded_model = h2o.load_model(model_name)   
         testing= request.get_json() 
         test = h2o.H2OFrame(testing)
         pred_ans = uploaded_model.predict(test).as_data_frame()
         item_dict['Prediction'] = pred_ans.predict.values[0]
         print(item_dict)
         return jsonify(item_dict)   # return the result /the prediction
        
if __name__ == "__main__":
    app.run(debug=True, port=5004)