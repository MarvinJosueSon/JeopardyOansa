import sqlite3
from pathlib import Path

DB_NAME = "preguntas.db"

SQL_CREATE = """
CREATE TABLE IF NOT EXISTS preguntas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    categoria TEXT NOT NULL,
    dificultad INTEGER NOT NULL,   -- 100,200,300,400,500
    tipo TEXT NOT NULL,            -- 'opcion', 'vf', 'completar'

    enunciado TEXT NOT NULL,

    opcion_a TEXT,
    opcion_b TEXT,
    opcion_c TEXT,
    opcion_d TEXT,

    respuesta_correcta TEXT NOT NULL,

    usada INTEGER DEFAULT 0
);
"""

SQL_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_cat_dif_usada
ON preguntas (categoria, dificultad, usada);

CREATE INDEX IF NOT EXISTS idx_tipo
ON preguntas (tipo);
"""

def connect():
    return sqlite3.connect(DB_NAME)

def crear_db():
    with connect() as con:
        cur = con.cursor()
        cur.execute(SQL_CREATE)
        for stmt in SQL_INDEXES.strip().split(";"):
            s = stmt.strip()
            if s:
                cur.execute(s)
        con.commit()

def agregar_pregunta(con, categoria, dificultad, tipo, enunciado,
                     a=None, b=None, c=None, d=None, correcta=""):
    con.execute(
        """
        INSERT INTO preguntas
        (categoria, dificultad, tipo, enunciado, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (categoria, dificultad, tipo, enunciado, a, b, c, d, correcta)
    )

def cargar_ejemplos():
    with connect() as con:
        # Opción múltiple
        agregar_pregunta(
            con,
            categoria="Personajes",
            dificultad=300,
            tipo="opcion",
            enunciado="¿Quién negó a Jesús tres veces?",
            a="Pedro", b="Juan", c="Judas", d="Tomás",
            correcta="Pedro"
        )

        # Verdadero/Falso
        agregar_pregunta(
            con,
            categoria="Historia",
            dificultad=100,
            tipo="vf",
            enunciado="Moisés abrió el Mar Rojo.",
            a="Verdadero", b="Falso",
            correcta="Verdadero"
        )

        # Completar
        agregar_pregunta(
            con,
            categoria="Versículos",
            dificultad=200,
            tipo="completar",
            enunciado="Jesús es el camino, la verdad y la ____.",
            a="vida", b="luz", c="salvación",
            correcta="vida"
        )

        con.commit()

def main():
    # (Opcional) borrarla y recrearla limpio:
    # Path(DB_NAME).unlink(missing_ok=True)

    crear_db()
    cargar_ejemplos()
    print("✅ Base creada y ejemplos insertados en preguntas.db")

if __name__ == "__main__":
    main()
