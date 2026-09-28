import sqlite3
import json

from backend.config import DATABASE_PATH


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


# ==========================================
# INITIALIZE DATABASE
# ==========================================

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()


    # ======================================
    # CREATORS TABLE
    # ======================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS creators (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            creator_type TEXT NOT NULL,

            region TEXT,

            language TEXT,

            bio TEXT,

            tradition TEXT,

            social_link TEXT

        )
        """
    )


    # ======================================
    # CREATIVE WORKS TABLE
    # ======================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS works (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            creator_id INTEGER NOT NULL,

            title TEXT NOT NULL,

            category TEXT,

            creator_description TEXT,

            cultural_context TEXT,

            tags TEXT,

            image_path TEXT,

            FOREIGN KEY (creator_id)
                REFERENCES creators(id)

        )
        """
    )


    connection.commit()

    connection.close()


# ==========================================
# CREATE CREATOR
# ==========================================

def create_creator(data):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        INSERT INTO creators
        (
            name,
            creator_type,
            region,
            language,
            bio,
            tradition,
            social_link
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.name,
            data.creator_type,
            data.region,
            data.language,
            data.bio,
            data.tradition,
            data.social_link
        )
    )


    creator_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return creator_id


# ==========================================
# GET ALL CREATORS
# ==========================================

def get_creators():

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM creators
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


# ==========================================
# GET ONE CREATOR
# ==========================================

def get_creator(creator_id):

    connection = get_connection()

    row = connection.execute(
        """
        SELECT *
        FROM creators
        WHERE id = ?
        """,
        (creator_id,)
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)


# ==========================================
# CREATE WORK
# ==========================================

def create_work(data, image_path=""):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        INSERT INTO works
        (
            creator_id,
            title,
            category,
            creator_description,
            cultural_context,
            tags,
            image_path
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.creator_id,
            data.title,
            data.category,
            data.creator_description,
            data.cultural_context,
            json.dumps(data.tags),
            image_path
        )
    )


    work_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return work_id


# ==========================================
# GET ALL WORKS
# ==========================================

def get_works():

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            works.*,
            creators.name AS creator_name

        FROM works

        JOIN creators
            ON works.creator_id = creators.id

        ORDER BY works.id DESC
        """
    ).fetchall()

    connection.close()


    results = []


    for row in rows:

        item = dict(row)

        try:

            item["tags"] = json.loads(
                item.get("tags") or "[]"
            )

        except Exception:

            item["tags"] = []


        results.append(item)


    return results