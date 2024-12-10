# relaxy-ai-engineer-task
# how to setup the task to run the experiments
- first follow the steps that are mentioned in the task readme to have a initial setup
- Then change the code firstly fix the dataset path, secondly fix issues in the model_trainer file and changed the train-test split for better f1-score.
- upgrade the mlflow with the command "pip install mlflow --upgrade"
- then use mlflow to log the experiment
- set the enviorment varaible using this command "export MLFLOW_TRACKING_URI=sqlite:///mlruns.db" to store the logs in sqlite database.
- finally run the main.py file to track and run the experiment and log it into database.
# how to register the model
- first start the server using this command "mlflow ui --port <port_number> --backend-store-uri sqlite:///mlruns.db"
- Then,find the model you want to register. models will appear as the image shows ![image](https://github.com/Ridwanursustswe18/relaxy-ai-engineer-task/blob/master/Screenshot%202024-12-05%20184436.png)
- After that click the model and it will show the overview like the image ![image](https://github.com/Ridwanursustswe18/relaxy-ai-engineer-task/blob/master/Screenshot%202024-12-05%20184604.png)
- Go to the artifact folder and you will find a register model button beside the model path as demonstrated in the image ![image](https://github.com/Ridwanursustswe18/relaxy-ai-engineer-task/blob/master/Screenshot%202024-12-05%20184648.png)
- Finally go to the models registered page and add descriptions,tags,aliases as needed ![image](https://github.com/Ridwanursustswe18/relaxy-ai-engineer-task/blob/master/Screenshot%202024-12-05%20184712.png)
# tracking the registered model and serving it as a server
- now we are going to serve the model to access it and use it to make api calls to make prediction.
- Firstly, we need to setup the correct pyenv module execute the commands given in the file[file_link](https://drive.google.com/file/d/1CZnXKcUUuC82tcL97i-tlJi8Zm-lBWne/view?usp=sharing)
- Secondly, set the tracking uri using these command "export MLFLOW_TRACKING_URI=<uri>"
- Thirdly, serve the model using following command "mlflow models serve -m "models:/<model_name>/<model_version>" --port <port-number>"
- Finally, use the server and make api using flask and flask server.


