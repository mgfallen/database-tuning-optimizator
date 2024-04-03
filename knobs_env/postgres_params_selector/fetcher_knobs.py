import psycopg2
import configparser

import knobs_env.knobs as k


def read_config(filename='../../db.ini'):
    config = configparser.ConfigParser()
    config.read(filename)
    return config['database']


def connect_to_database(config):
    try:
        connection = psycopg2.connect(**config)
        return connection
    except Exception as e:
        print("Error connecting to database:", e)
        # print(config['host'], config['port'], config['database'], config['user'], config['password'])
        return None


def fetch_parameters(connection, parameters):
    variables = {param: [] for param in parameters}
    try:
        cursor = connection.cursor()
        for parameter in parameters:
            cursor.execute(f"SHOW {parameter};")
            result = cursor.fetchall()
            for row in result:
                variables[parameter].append(row[0])
    except Exception as e:
        print("Error fetching parameters:", e)
    finally:
        if connection:
            connection.close()
    return variables


if __name__ == "__main__":
    config = read_config("../../db.ini")
    connection = connect_to_database(config)
    knobs_dict = k.Knobs().knobs
    # parame ters = knobs_dict.keys()
    parameters = ["wal_buffers"]
    if connection:
        a = fetch_parameters(connection, parameters)
        print(a)
