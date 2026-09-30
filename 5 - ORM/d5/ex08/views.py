from django.shortcuts import render, redirect
import psycopg2
from django.conf import settings


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
                        climate VARCHAR(),
                        diameter INTEGER,
                        orbital_period INTEGER,
                        population BIGINT,
                        rotation_period INTEGER,
                        surface_water REAL,
                        terrain: VARCHAR(128),
                        );
                    CREATE TABLE IF NOT EXISTS ex08_planets(
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(64) UNIQUE NOT NULL,
                        birth_year VARCHAR(32),
                        gender VARCHAR(32),
                        eye_color VARCHAR(32),
                        hair_color VARCHAR(32),
                        heigth INTEGER,
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
            with open("./ex08/ressources/planets.csv", "r") as f:
                try:
                    ligne = f.readline().split(" ")
                    print(ligne)
                    cur.execute("""
                                INSERT INTO ex08_planets (name, climate, diameter, orbital_period, population, rotation_period, surface_water, terrain)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
                                , ligne)
                    conn.commit()
                    results.append("OK")
                except Exception as e:
                    conn.rollback()
                    results.append(f"{ligne[1]} : {e}")
            with open("./ex08/ressources/people.csv") as f:
                try:
                    ligne = f.readline().split(" ")
                    cur.execute("""
                                INSERT INTO ex08_people (name, birth_year, gender, eye_color, hair_color, height, mass, homeworld)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
                                , ligne)
                    conn.commit()
                    results.append("OK")
                except Exception as e:
                    conn.rollback()
                    results.append(f"{ligne[1]} : {e}")
    except Exception as e:
        # la connexion elle-même a échoué
        results.append(str(e))
    finally:
        if conn is not None:
            conn.close()
    return render(request, "index2.html", {"message": results})
#
# def display(request):
#     conn = None
#     rows = []
#     header = []
#     try:
#         conn = connect()
#         cur = conn.cursor()
#         cur.execute("""SELECT * FROM ex06_movies""")
#         rows = cur.fetchall()
#         header = [col[0] for col in cur.description]
#     except Exception as e:
#         print(e)
#     finally:
#         if conn is not None:
#             conn.close()
#     return render(request, "display.html", {"header" : header ,"rows": rows})
#
#
# def remove(request):
#     conn = None
#     form = None
#     titles = []
#     try:
#         conn = connect()
#         cur = conn.cursor()
#         cur.execute("""SELECT title FROM ex06_movies""")
#         titles = [(row[0], row[0]) for row in cur.fetchall()]
#         print(request.method)
#         if request.method == "POST":
#             form = RemoveMovie(titles, request.POST)
#             if form.is_valid():
#                 cur.execute("DELETE FROM ex06_movies WHERE title = %s;", (form.cleaned_data["title"],))
#                 conn.commit()
#                 if conn is not None:
#                     conn.close()
#                 return redirect("/ex06/remove")
#         else:
#             form = RemoveMovie(titles)
#     except Exception as e:
#         print("Erreur", e)
#     finally:
#         if conn is not None:
#             conn.close()
#     return render(request, "form2.html", {"form" : form, "titles": titles, "nameButton": "Remove"})
#
# def update(request):
#     conn = None
#     form = None
#     titles = []
#     try:
#         conn = connect()
#         cur = conn.cursor()
#         cur.execute("""SELECT title FROM ex06_movies""")
#         titles = [(row[0], row[0]) for row in cur.fetchall()]
#         print(request.method)
#         if request.method == "POST":
#             form = UpdateMovie(titles, request.POST)
#             if form.is_valid():
#                 print(form.cleaned_data["opening_crawl"], form.cleaned_data["title"])
#                 cur.execute("UPDATE ex06_movies SET opening_crawl = %s WHERE title = %s;",
#                             (form.cleaned_data["opening_crawl"],
#                              form.cleaned_data["title"])
#                             )
#                 conn.commit()
#                 if conn is not None:
#                     conn.close()
#                 return redirect("/ex06/update")
#         else:
#             form = UpdateMovie(titles)
#     except Exception as e:
#         print("Erreur", e)
#     finally:
#         if conn is not None:
#             conn.close()
#     return render(request, "form2.html", {"form" : form, "titles": titles, "nameButton": "Update"})
