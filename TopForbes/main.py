import urllib
import json
from urllib import request
import sqlite3

headers = {'cookie': 'notice_gdpr_prefs'}  # required cookie that needs to be sent to view the data

url_forbes = r"https://www.forbes.com/forbesapi/person/billionaires/2021/position/true.json?limit=2"


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Opened database!")
        return conn
    except Exception as ex:
        print(ex)

    return conn


def create_table(conn, statement):
    try:
        c = conn.cursor()
        c.execute(statement)
        print("Table created!")
    except Exception as ex:
        print(ex)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        req = urllib.request.Request(url_forbes, None, headers)
        resp = urllib.request.urlopen(req)
        data = resp.read().decode('utf-8')
        json_obj = json.loads(data)
        #dictionary with list of billionaires and total count
        person_list_dict = json_obj["personList"]
        # list of billionaires (every billionaire is a dictionary)
        persons_lists = person_list_dict["personsLists"] #list of billionaires
        for p in persons_lists:
            print(p)
    except Exception as e:
        print("Error : ", e)

    con = create_connection('forbes.db')
    stmt = """ CREATE TABLE IF NOT EXISTS billionaires (
                                        rank integer PRIMARY KEY,
                                        personName text NOT NULL,
                                        age integer NOT NULL,
                                        country text NOT NULL,
                                        countryOfCitizenship text NOT NULL,
                                        philanthropyScore integer NOT NULL
                                    ); """

    create_table(con, stmt)

