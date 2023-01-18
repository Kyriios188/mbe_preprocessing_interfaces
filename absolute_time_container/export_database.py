import mysql.connector
from database import Experiment, Step


def export_database_main(experiment: Experiment) -> None:

    DATABASE = mysql.connector.connect(
        host="172.20.0.10",
        user="root",
        password="123thisisatest!",
        database="epitaxy_db",
    )

    if DATABASE.is_connected():
        print("Connection established.")

    CURSOR = DATABASE.cursor()

    experiment_query: str = experiment.get_insert_query()

    CURSOR.execute(experiment_query)
    experiment_key: int = CURSOR.lastrowid

    # On obtient la clé de l'expérience

    for step in experiment.step_list:
        # Insert Step
        step_query: str = step.get_step_insert_query(experiment_key)
        CURSOR.execute(step_query)
        
        step_key: int = CURSOR.lastrowid
        layer_query: str = step.get_insert_query(step_id=step_key)
        CURSOR.execute(layer_query)
    
    CURSOR.close()
    DATABASE.commit()
    DATABASE.close()

    return
