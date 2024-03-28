import psycopg2
import configparser


def read_config(filename='db.ini'):
    config = configparser.ConfigParser()
    config.read(filename)
    return config['database']


def connect_to_database(config):
    try:
        connection = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password']
        )
        return connection
    except Exception as e:
        print("Error connecting to database:", e)
        return None


def fetch_parameters(connection, parameters):
    variables = {param: [] for param in parameters}
    try:
        cursor = connection.cursor()
        for parameter in parameters:
            cursor.execute(f"SELECT {parameter} FROM your_table_name;")
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
    config = read_config("db.ini")
    parameters = ["param1", "param2", "param3"]  # Замените на список параметров, которые вы хотите извлечь
    connection = connect_to_database(config)
    if connection:
        fetch_parameters(connection, parameters)
