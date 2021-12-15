import urllib
import json
from urllib import request
import sqlite3

headers = {'cookie': 'notice_gdpr_prefs'}  # required cookie that needs to be sent to view the data

url_forbes = r"https://www.forbes.com/forbesapi/person/billionaires/2021/position/true.json?limit=200"


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


def insert_row(conn, values):
    stmt = ''' INSERT INTO billionaires
                (rank, personName, age, country, countryOfCitizenship, philanthropyScore, finalWorth)
                 VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(stmt, values)
    conn.commit()
    return cur.lastrowid


def top_10_yougest(conn):
    stmt = '''SELECT personName, age FROM billionaires
                WHERE age IS NOT NULL
                ORDER BY age LIMIT 10'''

    cur = conn.cursor()
    cur.execute(stmt)

    rows = cur.fetchall()

    print("Top 10 youngest billionaires")
    for row in rows:
        print(row)


def count_american_citizenship(conn):
    stmt = '''SELECT COUNT(*) FROM billionaires
            WHERE countryOfCitizenship LIKE 'United States' '''

    cur = conn.cursor()
    cur.execute(stmt)

    count = cur.fetchone()

    print("Billionaires with american citizenship:", count[0])
    print("Billionaires with other citizenship:", 200 - count[0])


def top_10_philantropic_score(conn):
    stmt = '''SELECT personName, philanthropyScore FROM billionaires
                    WHERE philanthropyScore IS NOT NULL
                    ORDER BY philanthropyScore DESC LIMIT 10'''

    cur = conn.cursor()
    cur.execute(stmt)

    rows = cur.fetchall()

    print("Top 10 by philantropic score: ")
    for row in rows:
        print(row)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    con = create_connection('forbes.db')
    cursor = con.cursor()
    cursor.execute("DROP TABLE billionaires")
    stmt_create = """ CREATE TABLE IF NOT EXISTS billionaires (
                                            rank integer NOT NULL,
                                            personName text NOT NULL,
                                            age integer,
                                            country text NOT NULL,
                                            countryOfCitizenship text NOT NULL,
                                            philanthropyScore integer,
                                            finalWorth real NOT NULL
                                        ); """

    create_table(con, stmt_create)

    try:
        req = urllib.request.Request(url_forbes, None, headers)
        resp = urllib.request.urlopen(req)
        data = resp.read().decode('utf-8')
        json_obj = json.loads(data)
        # dictionary with list of billionaires and total count
        person_list_dict = json_obj["personList"]
        # list of billionaires (every billionaire is a dictionary)
        persons_lists = person_list_dict["personsLists"]  # list of billionaires
        for p in persons_lists:
            values_to_insert = (p.get('rank'), p.get('personName'), p.get('age'), p.get('country'),
                                p.get('countryOfCitizenship'), p.get('philanthropyScore'), p.get('finalWorth'))
            insert_row(con, values_to_insert)

        top_10_yougest(con)
        count_american_citizenship(con)
        top_10_philantropic_score(con)

    except Exception as e:
        print("Error : ", e)
