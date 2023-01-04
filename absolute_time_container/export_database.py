import mysql.connector

from database import Experiment, Step


def export_database_main(experiment_list: list[Experiment]) -> None:

    try:
        DATABASE = mysql.connector.connect(
            host="sopdifugbqdusfgyfu",  #TODO:
            user="root",
            password="password",
            database="epitaxy_data",
        )
        
    except mysql.connector.ProgrammingError:
        print("Erreur dans les identifiants, veuillez réessayer.")

    if DATABASE.is_connected():
        print("Connexion établie.")

    CURSOR = DATABASE.cursor()


    for experiment in experiment_list:
        experiment_query: str = experiment.get_query()
        # Send query uwu *rawr*

        CURSOR.execute(experiment_query)
        experiment_key: int = CURSOR.fetchall()[0][0]

        # On obtient la clé de l'expérience

        for step in experiment.step_list:
            step_query: str = step.get_query(experiment_key)
            CURSOR.execute(experiment_query)
            step_key: int = CURSOR.fetchall()[0][0]

            # insert the sensor data

    return
