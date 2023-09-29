from flask import Flask,request
from flask_mongoengine import MongoEngine
from werkzeug.utils import secure_filename
import os,os.path
from models.models import Workspace
from models.models import Models
from flask_swagger_ui import get_swaggerui_blueprint
import h2o
from h2o.automl import H2OAutoML
from models.models import File
import pandas as pd



app = Flask(__name__)
## swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Workspaces_H2O_Flask-REST-Api"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###
app.config['MONGODB_SETTINGS'] = {
    'db':'db_name',
    'host':'localhost',
    'port':'27017'
}


app.config['MONGODB_SETTINGS'] = {
    'host':'mongodb://localhost:27017'}
db=MongoEngine(app)
@app.route('/models', methods=['GET'])  
def get_models():  
        obj=Models()
        return (obj.read())
@app.route('/models/<id>', methods=['DELETE'])
def delete_model(id):
    obj=Models()
    return (obj.Delete(id))

@app.route('/workspaces/models/<id>', methods=['POST']) #add a model  by id of workspace
def add_model(id):    
        workspace = Workspace.objects.get_or_404(id=id)
        m=Models()
        fd= request.files['file']
        m.model_name=fd.filename
        m.path=os.path.join(os.path.abspath('ML_models'), fd.filename)
        filename = secure_filename(fd.filename)
        fd.save( filename)
        m.save()
        workspace.models.append(m)
        workspace.save()
        return("model added successefully")


@app.route('/train/<id>', methods=['POST']) #train models using a file /id : the idi of a file)
def apload(id):
    h2o.init()
    json_data = request.json
    a_value = json_data["a_key"]
    file = File.objects.get_or_404(id=id)
    data = h2o.import_file(path=file.path, destination_frame="train")
    train, test = data.split_frame(ratios=[0.8])
    x = train.columns
    print(x)
    y = a_value
    x.remove(y)
    train[y] = train[y].asfactor()
    test[y] = test[y].asfactor()
    aml = H2OAutoML(max_models=20, seed=1)
    aml.train(x=x, y=y, training_frame=train)
    lb = aml.leaderboard

    model_ids = list(lb['model_id'].as_data_frame().iloc[:, 0])
    model_ids_df = pd.DataFrame({'model_id': model_ids})
    out_path = "ML_models"
    for m_id in model_ids: # save all models locally
        mdl = h2o.get_model(m_id)
        h2o.save_model(model=mdl, path=out_path, force=True)
    h2o.export_file(lb, os.path.join(out_path, file.filename + 'algorithms'), force=True)
    lbdf = lb.head(rows=10).as_data_frame()
    js = lbdf.to_json()
    return (js) # return all the models version with their performance

if __name__ == "__main__":
    app.run(port=5005, debug=True)