import os
import pandas
from nptdms import TdmsFile

import mysql.connector


def map_step_to_rel_time(file_path: str):
    """
    Using the path to a 'AXXX Recipe Number Layer.tdms', build a map to link the step number to 
    the relative time start and end.
    
    Step number goes from 0 ('Starting recipe ... with priority x') to n+1 (a step with identical 
    relative start and end to signify the end)
    """
    
    tdms_file = TdmsFile.read(file_path)
    df = tdms_file.as_dataframe()
    
    rel_time_map: dict[int, tuple[float, float]] = {}
    previous_time: float = 0.0
    # len(df.index) gives the number of rows
    for i in range(len(df.index)):
        # df.iloc[i][0] gives the first element of the ith line
        line = df.iloc[i]
        
        step_number = int(line[0])
        layer_start_time = float(line[1])
        if step_number != 1:
            try:
                rel_time_map[step_number - 1] = (previous_time, layer_start_time)
            except KeyError:
                print(f"Recipe Layer Number does not have a n°{step_number - 1}")
        previous_time = layer_start_time

    # Can't detect the end since the end is not consistent with the mbe absolute time step number :)
    rel_time_map[step_number] = (layer_start_time, 9999999999)

    return rel_time_map


def send_rel_time_to_db(code: str, step_to_rel_map: dict[int, tuple[float, float]]):
    """
    Using a map between step number and relative time, sets the relative time
    start and end of every step in the given experiment's list.

    """
    
    DATABASE = mysql.connector.connect(
        host="172.20.0.1",
        user="root",
        port=3306,
        password="123thisisatest!",
        database="epitaxy_db",
    )

    if DATABASE.is_connected():
        print("Connection established.")

    CURSOR = DATABASE.cursor()
    
    # Get the experiment id from the code so we can select the associated steps.
    CURSOR.execute(f"SELECT id FROM experiment WHERE experiment.code = '{code}'")
    experiment_id: int = CURSOR.fetchall()[0][0]
    
    CURSOR.execute(f"SELECT step.id, step.step_number FROM step JOIN experiment ON step.experiment_fk = {experiment_id}")
    step_numbers: list[tuple[int, int]] = CURSOR.fetchall()

    for step in step_numbers:

        # The step 0 is not present in the log file
        if step[1] == 0:
            CURSOR.execute(f"UPDATE step SET rel_start=0, rel_end={step_to_rel_map[1][0]} WHERE id = {step[0]}")
        else:
            try:
                rel_start, rel_end = step_to_rel_map[step[1]]
                CURSOR.execute(f"UPDATE step SET rel_start={rel_start}, rel_end={rel_end} WHERE id = {step[0]}")
            except KeyError:
                pass
    CURSOR.close()
    DATABASE.commit()
    DATABASE.close()


def fill_database_main(code: str):
    filepath: str = os.listdir('files/')[0]
    code = filepath[:5]
    
    # Make a map with each step associated to its relative start and end
    rel_time_map = map_step_to_rel_time(
        file_path='files/'+filepath
    )
    
    # Send it to the DB
    send_rel_time_to_db(code=code, step_to_rel_map=rel_time_map)