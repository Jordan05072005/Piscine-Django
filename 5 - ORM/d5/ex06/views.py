from django.shortcuts import render, redirect
import psycopg2
from django.conf import settings
from .forms.forms import RemoveMovie, UpdateMovie


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
CREATE TABLE IF NOT EXISTS ex06_movies(
    title VARCHAR(64) UNIQUE NOT NULL,
    episode_nb INT PRIMARY KEY,
    opening_crawl TEXT,
    director VARCHAR(32) NOT NULL,
    producer VARCHAR(128) NOT NULL,
    release_date DATE NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT now(),
    updated TIMESTAMP NOT NULL DEFAULT now()
);
CREATE OR REPLACE FUNCTION update_changetimestamp_column()
RETURNS TRIGGER AS $$
BEGIN
NEW.updated = now();
NEW.created = OLD.created;
RETURN NEW;
END;
$$ language 'plpgsql';
CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
    ON ex06_movies FOR EACH ROW EXECUTE PROCEDURE
    update_changetimestamp_column();

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
                                INSERT INTO ex06_movies (episode_nb, title, director, producer, release_date)
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
        cur.execute("""SELECT * FROM ex06_movies""")
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
    titles = []
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""SELECT title FROM ex06_movies""")
        titles = [(row[0], row[0]) for row in cur.fetchall()]
        print(request.method)
        if request.method == "POST":
            form = RemoveMovie(titles, request.POST)
            if form.is_valid():
                cur.execute("DELETE FROM ex06_movies WHERE title = %s;", (form.cleaned_data["title"],))
                conn.commit()
                if conn is not None:
                    conn.close()
                return redirect("/ex06/remove")
        else:
            form = RemoveMovie(titles)
    except Exception as e:
        print("Erreur", e)
    finally:
        if conn is not None:
            conn.close()
    return render(request, "form2.html", {"form" : form, "titles": titles, "nameButton": "Remove"})

def update(request):
    conn = None
    form = None
    titles = []
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""SELECT title FROM ex06_movies""")
        titles = [(row[0], row[0]) for row in cur.fetchall()]
        print(request.method)
        if request.method == "POST":
            form = UpdateMovie(titles, request.POST)
            if form.is_valid():
                print(form.cleaned_data["opening_crawl"], form.cleaned_data["title"])
                cur.execute("UPDATE ex06_movies SET opening_crawl = %s WHERE title = %s;",
                            (form.cleaned_data["opening_crawl"],
                            form.cleaned_data["title"])
                            )
                conn.commit()
                if conn is not None:
                    conn.close()
                return redirect("/ex06/update")
        else:
            form = UpdateMovie(titles)
    except Exception as e:
        print("Erreur", e)
    finally:
        if conn is not None:
            conn.close()
    return render(request, "form2.html", {"form" : form, "titles": titles, "nameButton": "Update"})
