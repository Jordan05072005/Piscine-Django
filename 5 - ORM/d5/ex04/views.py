from django.shortcuts import render, redirect
import psycopg2
from django.conf import settings
from .forms.forms import RemoveMovie


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
CREATE TABLE IF NOT EXISTS ex04_movies(
    title VARCHAR(64) UNIQUE NOT NULL,
    episode_nb INT PRIMARY KEY,
    opening_crawl TEXT,
    director VARCHAR(32) NOT NULL,
    producer VARCHAR(128) NOT NULL,
    release_date DATE NOT NULL
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

MOVIES = [
    (1, "The Phantom Menace", "George Lucas", "Rick McCallum", "1999-05-19"),
    (2, "Attack of the Clones", "George Lucas", "Rick McCallum", "2002-05-16"),
    (3, "Revenge of the Sith", "George Lucas", "Rick McCallum", "2005-05-19"),
    (4, "A New Hope", "George Lucas", "Gary Kurtz, Rick McCallum", "1977-05-25"),
    (5, "The Empire Strikes Back", "Irvin Kershner", "Gary Kutz, Rick McCallum", "1980-05-17"),
    (6, "Return of the Jedi", "Richard Marquand", "Howard G. Kazanjian, George Lucas, Rick McCallum", "1983-05-25"),
    (7, "The Force Awakens", "J. J. Abrams", "Kathleen Kennedy, J. J. Abrams, Bryan Burk", "2015-12-11"),
]

def populate(request):
    results = []
    conn = None
    try:
        conn = connect()
        with conn.cursor() as cur:
            for movie in MOVIES:
                try:
                    cur.execute("""
                                INSERT INTO ex04_movies (episode_nb, title, director, producer, release_date)
                                   VALUES (%s, %s, %s, %s, %s);"""
                                , movie)
                    conn.commit()
                    results.append("OK")
                except Exception as e:
                    conn.rollback()
                    results.append(f"{movie[1]} : {e}")
    except Exception as e:
        # la connexion elle-même a échoué
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
        cur.execute("""SELECT * FROM ex04_movies""")
        rows = cur.fetchall()
        header = [col[0] for col in cur.description]
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()
    return render(request, "display.html", {"header" : header ,"rows": rows})


def remove(request):
    conn = None
    form = None
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""SELECT title FROM ex04_movies""")
        titles = [(row[0], row[0]) for row in cur.fetchall()]
        print(request.method)
        if request.method == "POST":
            form = RemoveMovie(titles, request.POST)
            if form.is_valid():
                cur.execute("DELETE FROM ex04_movies WHERE title = %s;", (form.cleaned_data["title"],))
                conn.commit()
                if conn is not None:
                    conn.close()
                return redirect("/ex04/remove")


        else:
            form = RemoveMovie(titles)
    except Exception as e:
        print("Erreur", e)
    finally:
        if conn is not None:
            conn.close()
    return render(request, "form.html", {"form" : form, "titles": titles})







