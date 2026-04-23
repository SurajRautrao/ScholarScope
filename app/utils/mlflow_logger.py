import mlflow

def init_mlflow():
    mlflow.set_experiment("Research_Assistant")

def start_run():
    return mlflow.start_run()
