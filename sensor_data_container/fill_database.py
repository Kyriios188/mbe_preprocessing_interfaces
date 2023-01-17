import mysql.connector
import math
import pandas as pd
from nptdms import TdmsFile


def get_step_id_for_rel_time(rel_time: float, cursor):
    cursor.execute(f"SELECT id FROM step WHERE rel_start <= {rel_time} AND rel_end >= {rel_time};")
    return cursor.fetchone()[0]


def get_query_from_values_list(values_list: list[tuple]):
    
    values_list_str: str = ""
    for i, vals in enumerate(values_list):
        values_list_str += f"('{vals[0]}', '{vals[1]}', '{vals[2]}', '{vals[3]}')"
        
        if i != len(values_list) - 1:
            values_list_str += ', '
    
    query: str = f"""
    INSERT INTO reflectivity
        (step_fk,
        rel_time,
        nm_value,
        reflectivity_value)
    VALUES
        {values_list_str};
    
    """
    
    return query


def extract_data(file_path: str, icol: int, data_type: str):
    
    db_table_name_map = {
        'Wafer Temperature': 'wafer_temperature',
        'Curvature': 'curvature',
        'Roughness': 'roughness',
        'Reflectivity': 'reflectivity'
    }
    
    DATABASE = mysql.connector.connect(
        host="172.20.0.10",
        user="root",
        port=3306,
        password="123thisisatest!",
        database="epitaxy_db",
    )

    if DATABASE.is_connected():
        print("Connection established.")

    CURSOR = DATABASE.cursor()
    
    tdms_file = TdmsFile.read(file_path)
    df = tdms_file.as_dataframe()
    
    for i_line in range(len(df.index)):  # len(df.index)
        tab: list[str] = df.iloc[i_line]
        
        if i_line % 100 == 0 and data_type == 'Reflectivity':
            print(f"Ligne {i_line}/{len(df.index)}")
        
        if tab[0] is None or tab[0] == '' or math.isnan(tab[0]) \
        or tab[icol] is None or tab[icol] == '' or math.isnan(tab[icol]):              
            continue
        
        rel_time: float = float(tab[0])
        
        # To go fast, we search the right step near where the previous rel_time was
        step_id: int = get_step_id_for_rel_time(
            rel_time=rel_time,
            cursor=CURSOR
        )

        if data_type != 'Reflectivity':
            data: float = float(tab[icol])
            
            query: str = f"""
            INSERT INTO {db_table_name_map[data_type]}
                (step_fk,
                rel_time,
                value)
            VALUES
                ('{step_id}',
                '{rel_time}',
                '{data}');
            
            """
            CURSOR.execute(query)

        # Pour la réflectivité, à un mesure en nanomètre correspond 
        # une colonne de Raw R et la colonne de temps.
        # On va donc avoir à chaque itération un dictionnaire avec pour clé une valeur
        # en nanomètres et pour value le tuple (temps, valeur) de la ligne en cours.
        else:
            
            # Pour chaque valeur en nanomètre (colonne C), on va ajouter 
            # le temps et les valeurs de la ligne en cours
            nm_column_name = df.columns[icol]
            values_list: list[tuple] = []
            for i, nm_value in enumerate(df[nm_column_name]):
                
                if pd.isnull(nm_value):
                    continue
                
                # La valeur en nanomètre pour i=0 correspond à Raw R0 soit la colonne D i.e. à 3
                # donc l'index de colonne est i+3
                reflectivity_float_value: float = float(tab[i+3])
                nm_float_value: float = float(nm_value)
                
                values_list.append((step_id, rel_time, nm_float_value, reflectivity_float_value))
            
            query: str = get_query_from_values_list(values_list)
            CURSOR.execute(query)
    
    DATABASE.commit()
    CURSOR.close()
    DATABASE.close()


def tdms_extraction_main(code: str):
    
    data_file_name: dict[str, int] = {
        'Wafer Temperature': (1, f'{code}_wafer_temperature.tdms'),
        'Curvature': (2, f'{code}_curvature.tdms'),
        'Roughness': (1, f'{code}_roughness.tdms'),
        'Reflectivity': (1, f'{code}_reflectivity.tdms')
    }
    for file in data_file_name.items():
        tdms_file: str = file[1][1]
        data_name: str = file[0]
        
        if code not in ['A1417', 'A1418', 'A1419', 'A1420']:
            continue
        print(f"{code}: {data_name}")
        
        extract_data(
            file_path='files/'+tdms_file,
            icol=file[1][0],
            data_type=data_name
        )
