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
- Then,find the model you want to register. models will appear as the image shows ![image](https://drive.google.com/file/d/1adiEECkn1KgRT1GeD4EVs-2-rYNQKdmF/view?usp=drive_link)
- After that click the model and it will show the overview like the image ![image](https://drive.google.com/file/d/1nJRH8Rz9vs31sGzq20YOjOxAVGmwWrsN/view?usp=sharing)
- Go to the artifact folder and you will find a register model button beside the model path as demonstrated in the image ![image](https://drive.google.com/file/d/1dS-uu48dOppNVTr4PvJg7LA9ofqvcgqt/view?usp=sharing)
- Finally go to the models registered page and add descriptions,tags,aliases as needed ![image](https://drive.google.com/file/d/10GGbNLxkvZz4PL0keq7Z-cSBFx82U7Ud/view?usp=sharing)



