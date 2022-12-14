import mysql.connector
from database import Experiment, Step


def export_database_main(experiment: Experiment) -> None:

    DATABASE = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123thisisatest!",
        database="epitaxy_db",
    )

    if DATABASE.is_connected():
        print("Connection established.")

    CURSOR = DATABASE.cursor()

    experiment_query: str = experiment.get_insert_query()
    print(experiment_query)

    CURSOR.execute(experiment_query)
    experiment_key: int = CURSOR.lastrowid

    # On obtient la clé de l'expérience

    for step in experiment.step_list:
        print(step.rel_start)
        step_query: str = step.get_step_insert_query(experiment_key)
        print(step_query)
        CURSOR.execute(step_query.replace("\"", "'"))
        
        step_key: int = CURSOR.lastrowid
        
        # TODO: add Layer / OtherStep data

        # insert the sensor data
    
    CURSOR.close()
    DATABASE.commit()
    DATABASE.close()

    return
