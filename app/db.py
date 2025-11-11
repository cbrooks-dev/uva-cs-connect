# app/db.py
import mysql.connector, os
from dotenv import load_dotenv
from flask import g, current_app
import click
from pathlib import Path
load_dotenv()

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=int(os.getenv('DB_PORT', '3306')),
            autocommit=False,
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None and db.is_connected():
        db.close()

def execute(query, params=None, *, fetchone=False, fetchall=False, commit=False, multi=False):
    db = get_db()
    cursor = db.cursor(dictionary=True, buffered=True)  
    try:
        if multi:
            for statement in query.split(';'):
                stmt = statement.strip()
                if stmt:
                    cursor.execute(stmt)
        else:
            cursor.execute(query, params or ())


        result = None
        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()

        if commit:
            db.commit()

        return result
    finally:
        cursor.close()

def init_db():
    schema_path = Path(current_app.root_path) / 'schema.sql'
    sql = schema_path.read_text(encoding='utf-8')
    execute(sql, multi=True, commit=True)

@click.command('init-db')
def init_db_command():
    with current_app.app_context():
        init_db()
    click.echo('Initialized the database.')