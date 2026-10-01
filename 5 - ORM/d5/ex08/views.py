from django.shortcuts import render, redirect
import psycopg2
from django.conf import settings
import os


def connect():
    conn = psycopg2.connect(
        dbname=settings.DATA_ENV["POSTGRES_DB"],
        user=settings.DATA_ENV["POSTGRES_USER"],
        password=settings.DATA_ENV["POSTGRES_PASSWORD"],
        host="localhost",
    )
    return conn

def init(context):
    conn, cur = None, None
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS ex08_planets(
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(64) UNIQUE NOT NULL,
                        climate VARCHAR,
                        diameter INTEGER,
                        orbital_period INTEGER,
                        population BIGINT,
                        rotation_period INTEGER,
                        surface_water REAL,
                        terrain VARCHAR(128)
                        );
                    CREATE TABLE IF NOT EXISTS ex08_people(
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(64) UNIQUE NOT NULL,
                        birth_year VARCHAR(32),
                        gender VARCHAR(32),
                        eye_color VARCHAR(32),
                        hair_color VARCHAR(32),
                        height INTEGER,
                        mass REAL,
                        homeworld VARCHAR(64),
                        FOREIGN KEY (homeworld) REFERENCES ex08_planets(name)
                        );
                    """)
        conn.commit()
        mess = "OK"
    except Exception as e:
        mess = str(e)
    finally:
        if conn is not None:
            conn.close()
            cur.close()
    return render(context, "index2.html", {"message": [mess]})

def populate(request):
    results = []
    conn = None
    try:
        conn = connect()
        with conn.cursor() as cur:
            files = [
                ("planets.csv", "ex08_planets",
                 ("name", "climate", "diameter", "orbital_period",
                  "population", "rotation_period", "surface_water", "terrain")),
                ("people.csv", "ex08_people",
                 ("name", "birth_year", "gender", "eye_color",
                  "hair_color", "height", "mass", "homeworld")),
            ]
            for filename, table, columns in files:
                try:
                    with open(os.path.join("ex08/ressources", filename), "r") as f:
                        cur.copy_from(f, table, sep="\t", null="NULL", columns=columns)
                    conn.commit()
                    results.append("OK")
                except Exception as e:
                    conn.rollback()
                    results.append(f"{table} : {e}")
    except Exception as e:
        results.append(str(e))
    finally:
        if conn is not None:
            conn.close()
    return render(request, "index2.html", {"message": results})


def display(request):
    conn = None
    rows = []
    header = []
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""SELECT ex08_people.name, ex08_people.homeworld, ex08_planets.climate FROM ex08_people 
                        JOIN ex08_planets ON ex08_people.homeworld = ex08_planets.name
                        WHERE ex08_planets.climate LIKE '%windy%'
                        ORDER BY ex08_people.name""")
        rows = cur.fetchall()
        header = [col[0] for col in cur.description]
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()
    return render(request, "display.html", {"header" : header ,"rows": rows})
