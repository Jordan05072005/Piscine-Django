from django.shortcuts import render
import psycopg2
import os
from django.conf import settings


def init(context):
    conn, cur = None, None
    try:
        conn = psycopg2.connect(
        dbname=settings.DATA_ENV["POSTGRES_DB"],
        user=settings.DATA_ENV["POSTGRES_USER"],
        password=settings.DATA_ENV["POSTGRES_PASSWORD"],
        host="localhost",
        )
        cur = conn.cursor()
        cur.execute("""
CREATE TABLE IF NOT EXISTS ex00_movies(
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
    return render(context, "index.html", {"message": mess})


    # cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")




