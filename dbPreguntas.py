#dbPreguntas.py
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_NAME = BASE_DIR / "dbPreguntas.db"


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
        (categoria, int(dificultad), tipo, enunciado, a, b, c, d, correcta)
    )


def borrar_todo():
    with connect() as con:
        con.execute("DELETE FROM preguntas")
        con.commit()


# =========================
# Helpers para cargar rápido
# =========================
def op(con, cat, dif, enun, a, b, c, d, correcta):
    agregar_pregunta(con, cat, dif, "opcion", enun, a, b, c, d, correcta)


def vf(con, cat, dif, enun, correcta):
    agregar_pregunta(con, cat, dif, "vf", enun, "Verdadero", "Falso", None, None, correcta)


def comp(con, cat, dif, enun, a, b, c, correcta):
    agregar_pregunta(con, cat, dif, "completar", enun, a, b, c, None, correcta)


# =========================
# BANCO 200 PREGUNTAS
# 5 categorías × 5 dificultades × 8 = 200
# =========================
def cargar_banco_200():
    with connect() as con:
        # ---------- HISTORIA ----------
        # 100
        vf(con, "Historia", 100, "Noé construyó un arca.", "Verdadero")
        vf(con, "Historia", 100, "Moisés recibió los Diez Mandamientos.", "Verdadero")
        op(con, "Historia", 100, "¿Quién fue tragado por un gran pez?", "Jonás", "Pablo", "Pedro", "Noé", "Jonás")
        op(con, "Historia", 100, "¿Quién fue el primer hombre?", "Adán", "Abraham", "Moisés", "David", "Adán")
        comp(con, "Historia", 100, "Dios creó el mundo en ____ días.", "7", "3", "10", "7")
        comp(con, "Historia", 100, "Jesús nació en ____.", "Belén", "Nazaret", "Jerusalén", "Belén")
        vf(con, "Historia", 100, "David derrotó a Goliat.", "Verdadero")
        op(con, "Historia", 100, "¿Quién construyó el arca?", "Noé", "Moisés", "Isaías", "Saúl", "Noé")

        # 200
        op(con, "Historia", 200, "¿Cuántos años estuvo Israel en el desierto?", "20", "40", "70", "100", "40")
        vf(con, "Historia", 200, "El Mar Rojo fue cruzado por el pueblo de Israel.", "Verdadero")
        comp(con, "Historia", 200, "Moisés fue encontrado en una ____.", "canasta", "casa", "cueva", "canasta")
        op(con, "Historia", 200, "¿Quién interpretó sueños en Egipto?", "José", "Daniel", "Nehemías", "Ester", "José")
        vf(con, "Historia", 200, "Sansón era conocido por su gran fuerza.", "Verdadero")
        comp(con, "Historia", 200, "Dios prometió a Abraham una gran ____.", "descendencia", "torre", "armadura", "descendencia")
        op(con, "Historia", 200, "¿Quién guió a Israel después de Moisés?", "Josué", "Caleb", "Saúl", "Elías", "Josué")
        vf(con, "Historia", 200, "Salomón fue conocido por su sabiduría.", "Verdadero")

        # 300
        op(con, "Historia", 300, "¿Qué cayó del cielo para alimentar a Israel?", "Maná", "Pan", "Uvas", "Peces", "Maná")
        comp(con, "Historia", 300, "Jericó cayó cuando tocaron las ____.", "trompetas", "campanas", "cuerdas", "trompetas")
        vf(con, "Historia", 300, "Elías enfrentó a profetas de Baal en el Carmelo.", "Verdadero")
        op(con, "Historia", 300, "¿Quién fue lanzado al foso de los leones?", "Daniel", "José", "Jeremías", "Samuel", "Daniel")
        comp(con, "Historia", 300, "Dios abrió el Mar ____.", "Rojo", "Muerto", "Azul", "Rojo")
        vf(con, "Historia", 300, "Ester fue reina y ayudó a su pueblo.", "Verdadero")
        op(con, "Historia", 300, "¿Quién construyó el templo en Jerusalén?", "Salomón", "Saúl", "David", "Nehemías", "Salomón")
        vf(con, "Historia", 300, "Gedeón venció con un ejército pequeño.", "Verdadero")

        # 400
        op(con, "Historia", 400, "¿Quién reconstruyó los muros de Jerusalén?", "Nehemías", "Esdras", "Daniel", "Josué", "Nehemías")
        vf(con, "Historia", 400, "Josías fue un rey que promovió reformas.", "Verdadero")
        comp(con, "Historia", 400, "El profeta que fue llevado en un torbellino fue ____.", "Elías", "Eliseo", "Amós", "Elías")
        op(con, "Historia", 400, "¿Qué instrumento tocaba David?", "Arpa", "Flauta", "Tambor", "Trompeta", "Arpa")
        vf(con, "Historia", 400, "Jonás predicó en Nínive.", "Verdadero")
        comp(con, "Historia", 400, "La torre famosa en Génesis se llama torre de ____.", "Babel", "Sion", "Cedro", "Babel")
        op(con, "Historia", 400, "¿Quién fue vendido por sus hermanos?", "José", "Moisés", "Isaac", "Jacob", "José")
        vf(con, "Historia", 400, "El arca del pacto estaba relacionada al tabernáculo.", "Verdadero")

        # 500
        op(con, "Historia", 500, "¿Cuál fue el nombre del rey babilónico asociado al cautiverio?", "Nabucodonosor", "Herodes", "César", "Faraón", "Nabucodonosor")
        comp(con, "Historia", 500, "El profeta que escribió Lamentaciones fue ____.", "Jeremías", "Isaías", "Ezequiel", "Jeremías")
        vf(con, "Historia", 500, "Ezequiel fue profeta durante el exilio.", "Verdadero")
        op(con, "Historia", 500, "¿Qué libro relata el retorno con Zorobabel y Esdras?", "Esdras", "Rut", "Jueces", "Amós", "Esdras")
        comp(con, "Historia", 500, "El padre de Juan el Bautista se llamaba ____.", "Zacarías", "Simeón", "Ananías", "Zacarías")
        vf(con, "Historia", 500, "El rey Saúl fue el primer rey de Israel.", "Verdadero")
        op(con, "Historia", 500, "¿Quién fue juez y también profeta?", "Samuel", "Salomón", "Aarón", "Job", "Samuel")
        comp(con, "Historia", 500, "El pacto con Noé incluyó el ____ como señal.", "arcoíris", "candelabro", "aceite", "arcoíris")

        # ---------- PERSONAJES ----------
        # 100
        op(con, "Personajes", 100, "¿Quién construyó el arca?", "Noé", "Moisés", "Pedro", "Juan", "Noé")
        op(con, "Personajes", 100, "¿Quién derrotó a Goliat?", "David", "Saúl", "Sansón", "Elías", "David")
        vf(con, "Personajes", 100, "Moisés fue un líder del pueblo de Israel.", "Verdadero")
        vf(con, "Personajes", 100, "Pedro fue uno de los discípulos de Jesús.", "Verdadero")
        comp(con, "Personajes", 100, "El amigo de Daniel en el horno fue ____ (uno de ellos).", "Sadrac", "Jonás", "Timoteo", "Sadrac")
        op(con, "Personajes", 100, "¿Quién fue madre de Jesús?", "María", "Marta", "Sara", "Rebeca", "María")
        comp(con, "Personajes", 100, "El hermano de Moisés se llamaba ____.", "Aarón", "Josué", "Isaac", "Aarón")
        vf(con, "Personajes", 100, "Jonás intentó huir de la misión de Dios.", "Verdadero")

        # 200
        op(con, "Personajes", 200, "¿Quién interpretó sueños del faraón?", "José", "Daniel", "Samuel", "Ester", "José")
        vf(con, "Personajes", 200, "Sansón tenía gran fuerza.", "Verdadero")
        comp(con, "Personajes", 200, "El padre de Isaac fue ____.", "Abraham", "Jacob", "Moisés", "Abraham")
        op(con, "Personajes", 200, "¿Quién fue la esposa de Abraham?", "Sara", "Rebeca", "Rut", "Ester", "Sara")
        vf(con, "Personajes", 200, "Ruth era moabita.", "Verdadero")
        comp(con, "Personajes", 200, "El rey sabio fue ____.", "Salomón", "Saúl", "Herodes", "Salomón")
        op(con, "Personajes", 200, "¿Quién fue pastor antes de ser rey?", "David", "Saúl", "Salomón", "Ciro", "David")
        vf(con, "Personajes", 200, "Ester arriesgó su vida para ayudar a su pueblo.", "Verdadero")

        # 300
        op(con, "Personajes", 300, "¿Quién negó a Jesús tres veces?", "Pedro", "Juan", "Judas", "Tomás", "Pedro")
        vf(con, "Personajes", 300, "Pablo antes se llamaba Saulo.", "Verdadero")
        comp(con, "Personajes", 300, "El discípulo amado se identifica como ____.", "Juan", "Pedro", "Andrés", "Juan")
        op(con, "Personajes", 300, "¿Quién fue vendido por sus hermanos?", "José", "Benjamín", "Isaac", "Elías", "José")
        vf(con, "Personajes", 300, "Marta y María eran hermanas.", "Verdadero")
        comp(con, "Personajes", 300, "El rey que pidió sabiduría a Dios fue ____.", "Salomón", "Saúl", "David", "Salomón")
        op(con, "Personajes", 300, "¿Quién bautizaba en el Jordán?", "Juan el Bautista", "Pedro", "Felipe", "Mateo", "Juan el Bautista")
        vf(con, "Personajes", 300, "Samuel ungió a David.", "Verdadero")

        # 400
        op(con, "Personajes", 400, "¿Quién escribió muchos Salmos?", "David", "Moisés", "Isaías", "Ester", "David")
        vf(con, "Personajes", 400, "Eliseo fue discípulo de Elías.", "Verdadero")
        comp(con, "Personajes", 400, "El profeta que vio un valle de huesos secos fue ____.", "Ezequiel", "Amós", "Jonás", "Ezequiel")
        op(con, "Personajes", 400, "¿Quién fue esposo de Rut?", "Booz", "Elcana", "Ciro", "Aarón", "Booz")
        vf(con, "Personajes", 400, "Nehemías fue copero del rey.", "Verdadero")
        comp(con, "Personajes", 400, "El hombre más fuerte (por voto nazareo) fue ____.", "Sansón", "Saúl", "Gedeón", "Sansón")
        op(con, "Personajes", 400, "¿Quién fue lanzado al foso de los leones?", "Daniel", "José", "Moisés", "Isaías", "Daniel")
        vf(con, "Personajes", 400, "Jeremías es conocido como el profeta llorón.", "Verdadero")

        # 500
        op(con, "Personajes", 500, "¿Quién tuvo un encuentro con Jesús camino a Damasco?", "Saulo", "Pedro", "Juan", "Lucas", "Saulo")
        vf(con, "Personajes", 500, "Bernabé acompañó a Pablo en viajes misioneros.", "Verdadero")
        comp(con, "Personajes", 500, "El suegro de Moisés se llamaba ____.", "Jetro", "Labán", "Ciro", "Jetro")
        op(con, "Personajes", 500, "¿Quién fue la profetisa que juzgó a Israel?", "Débora", "Ester", "Rut", "Ana", "Débora")
        vf(con, "Personajes", 500, "Timoteo fue un colaborador joven de Pablo.", "Verdadero")
        comp(con, "Personajes", 500, "El amigo de David que le fue fiel fue ____.", "Jonatán", "Saúl", "Absalón", "Jonatán")
        op(con, "Personajes", 500, "¿Quién escribió Apocalipsis?", "Juan", "Pablo", "Pedro", "Marcos", "Juan")
        vf(con, "Personajes", 500, "Zacarías era sacerdote y padre de Juan el Bautista.", "Verdadero")

        # ---------- LUGARES ----------
        # 100
        op(con, "Lugares", 100, "¿Dónde nació Jesús?", "Belén", "Nazaret", "Jerusalén", "Roma", "Belén")
        vf(con, "Lugares", 100, "Jerusalén es una ciudad mencionada en la Biblia.", "Verdadero")
        comp(con, "Lugares", 100, "Jesús fue criado en ____.", "Nazaret", "Belén", "Jericó", "Nazaret")
        op(con, "Lugares", 100, "¿En qué río fue bautizado Jesús?", "Jordán", "Nilo", "Éufrates", "Tigris", "Jordán")
        vf(con, "Lugares", 100, "El Mar de Galilea aparece en los evangelios.", "Verdadero")
        comp(con, "Lugares", 100, "Noé construyó el arca antes del ____.", "diluvio", "desierto", "templo", "diluvio")
        op(con, "Lugares", 100, "¿Dónde vivía el faraón?", "Egipto", "Babilonia", "Grecia", "Israel", "Egipto")
        vf(con, "Lugares", 100, "Belén está relacionada al nacimiento de Jesús.", "Verdadero")

        # 200
        op(con, "Lugares", 200, "¿Dónde cruzó Israel el Mar Rojo?", "Entre Egipto y el desierto", "En Canaán", "En Roma", "En Grecia", "Entre Egipto y el desierto")
        vf(con, "Lugares", 200, "Jericó era una ciudad amurallada.", "Verdadero")
        comp(con, "Lugares", 200, "El monte donde Moisés recibió la ley fue el monte ____.", "Sinaí", "Carmelo", "Horeb", "Sinaí")
        op(con, "Lugares", 200, "¿A qué ciudad fue Jonás a predicar?", "Nínive", "Belén", "Jerusalén", "Tiro", "Nínive")
        vf(con, "Lugares", 200, "Nazaret está en la región de Galilea.", "Verdadero")
        comp(con, "Lugares", 200, "Jesús caminó por la región de ____.", "Galilea", "Persia", "India", "Galilea")
        op(con, "Lugares", 200, "¿Dónde estaba el templo principal de Israel?", "Jerusalén", "Belén", "Nazaret", "Nínive", "Jerusalén")
        vf(con, "Lugares", 200, "Babilonia fue un imperio importante en la Biblia.", "Verdadero")

        # 300
        op(con, "Lugares", 300, "¿Dónde cayó Zaqueo del árbol? (ciudad)", "Jericó", "Belén", "Capernaúm", "Nazaret", "Jericó")
        vf(con, "Lugares", 300, "Capernaúm aparece como un lugar del ministerio de Jesús.", "Verdadero")
        comp(con, "Lugares", 300, "Pablo viajó a la ciudad de ____ en Macedonia (una de ellas).", "Filipos", "Nínive", "Belén", "Filipos")
        op(con, "Lugares", 300, "¿Dónde estuvo Daniel en cautiverio?", "Babilonia", "Egipto", "Roma", "Antioquía", "Babilonia")
        vf(con, "Lugares", 300, "El Jordán es un río del área de Israel.", "Verdadero")
        comp(con, "Lugares", 300, "El sermón del monte se asocia a un ____.", "monte", "río", "palacio", "monte")
        op(con, "Lugares", 300, "¿Dónde vivía Abraham cuando Dios lo llamó? (región/ciudad)", "Ur", "Roma", "Jericó", "Belén", "Ur")
        vf(con, "Lugares", 300, "La tierra prometida es Canaán.", "Verdadero")

        # 400
        op(con, "Lugares", 400, "¿En qué isla naufragó Pablo según Hechos?", "Malta", "Creta", "Patmos", "Chipre", "Malta")
        vf(con, "Lugares", 400, "Patmos se relaciona con Juan.", "Verdadero")
        comp(con, "Lugares", 400, "Jesús fue crucificado en el monte ____.", "Calvario", "Sinaí", "Carmelo", "Calvario")
        op(con, "Lugares", 400, "¿Dónde fue llevado Jesús de bebé para protegerlo?", "Egipto", "Roma", "Babilonia", "Nínive", "Egipto")
        vf(con, "Lugares", 400, "Sodoma y Gomorra eran ciudades antiguas.", "Verdadero")
        comp(con, "Lugares", 400, "El profeta Elías se asocia al monte ____.", "Carmelo", "Sinaí", "Oreb", "Carmelo")
        op(con, "Lugares", 400, "¿Dónde se dio el concilio de Hechos 15?", "Jerusalén", "Antioquía", "Roma", "Éfeso", "Jerusalén")
        vf(con, "Lugares", 400, "Éfeso fue una ciudad donde Pablo ministró.", "Verdadero")

        # 500
        op(con, "Lugares", 500, "¿En qué ciudad se ubicaba una de las 7 iglesias llamada Laodicea?", "Asia Menor", "Egipto", "Grecia", "Persia", "Asia Menor")
        vf(con, "Lugares", 500, "El Éufrates es un río mencionado en la Biblia.", "Verdadero")
        comp(con, "Lugares", 500, "El profeta Jonás huyó hacia ____.", "Tarsis", "Roma", "Belén", "Tarsis")
        op(con, "Lugares", 500, "¿Dónde escribió Juan Apocalipsis?", "Patmos", "Roma", "Jerusalén", "Antioquía", "Patmos")
        vf(con, "Lugares", 500, "El monte Sinaí está asociado al pacto de la ley.", "Verdadero")
        comp(con, "Lugares", 500, "La ciudad donde los discípulos fueron llamados cristianos por primera vez fue ____.", "Antioquía", "Belén", "Nínive", "Antioquía")
        op(con, "Lugares", 500, "¿En qué ciudad estuvo el templo de Artemisa?", "Éfeso", "Roma", "Jerusalén", "Filipos", "Éfeso")
        vf(con, "Lugares", 500, "Belén está en Judea.", "Verdadero")

        # ---------- MILAGROS ----------
        # 100
        vf(con, "Milagros", 100, "Jesús sanó enfermos.", "Verdadero")
        op(con, "Milagros", 100, "¿Qué convirtió Jesús en vino?", "Agua", "Leche", "Aceite", "Miel", "Agua")
        comp(con, "Milagros", 100, "Jesús calmó la ____ en el mar.", "tormenta", "nieve", "arena", "tormenta")
        vf(con, "Milagros", 100, "Jesús alimentó a mucha gente con pocos panes y peces.", "Verdadero")
        op(con, "Milagros", 100, "¿Qué hizo Jesús con Lázaro?", "Lo resucitó", "Lo envió", "Lo escondió", "Lo expulsó", "Lo resucitó")
        comp(con, "Milagros", 100, "Jesús caminó sobre el ____.", "agua", "fuego", "hielo", "agua")
        vf(con, "Milagros", 100, "Jesús hizo milagros.", "Verdadero")
        op(con, "Milagros", 100, "¿Quién abrió el Mar Rojo por poder de Dios?", "Moisés", "David", "Elías", "Pablo", "Moisés")

        # 200
        op(con, "Milagros", 200, "¿Cuántos panes se mencionan en la alimentación de los 5 mil?", "5", "7", "12", "2", "5")
        vf(con, "Milagros", 200, "Eliseo hizo milagros también.", "Verdadero")
        comp(con, "Milagros", 200, "Jesús sanó a un ciego llamado ____ (en un relato).", "Bartimeo", "Zaqueo", "Lázaro", "Bartimeo")
        op(con, "Milagros", 200, "¿Qué multiplicó Jesús para alimentar a la multitud?", "Panes y peces", "Uvas y miel", "Carne y agua", "Aceite y trigo", "Panes y peces")
        vf(con, "Milagros", 200, "Jesús sanó a un paralítico.", "Verdadero")
        comp(con, "Milagros", 200, "Jesús expulsó demonios y dio ____ a personas.", "libertad", "oro", "armas", "libertad")
        op(con, "Milagros", 200, "¿Qué sanó Jesús al tocarlo (en un relato)?", "Un leproso", "Un rey", "Un soldado", "Un juez", "Un leproso")
        vf(con, "Milagros", 200, "Dios hizo caer maná del cielo.", "Verdadero")

        # 300
        op(con, "Milagros", 300, "¿En qué evento Jesús convirtió agua en vino?", "Bodas en Caná", "Cena en Jerusalén", "Fiesta en Roma", "Bautismo en el Jordán", "Bodas en Caná")
        vf(con, "Milagros", 300, "Pedro caminó sobre el agua por un momento.", "Verdadero")
        comp(con, "Milagros", 300, "Jesús sanó a la suegra de ____.", "Pedro", "Juan", "Mateo", "Pedro")
        op(con, "Milagros", 300, "¿Qué hizo Jesús con la higuera sin fruto?", "La secó", "La plantó", "La cortó", "La regó", "La secó")
        vf(con, "Milagros", 300, "Elías hizo caer fuego del cielo.", "Verdadero")
        comp(con, "Milagros", 300, "Dios abrió el Jordán con ____ (líder).", "Josué", "Saúl", "Jonás", "Josué")
        op(con, "Milagros", 300, "¿Quién fue sanada al tocar el manto de Jesús?", "Mujer con flujo de sangre", "Marta", "Sara", "Rebeca", "Mujer con flujo de sangre")
        vf(con, "Milagros", 300, "Jesús resucitó a la hija de Jairo.", "Verdadero")

        # 400
        op(con, "Milagros", 400, "¿Qué milagro ocurrió en Pentecostés?", "Lenguas", "Oscuridad", "Terremoto", "Lluvia", "Lenguas")
        vf(con, "Milagros", 400, "Pablo y Silas cantaron y hubo un terremoto en la cárcel.", "Verdadero")
        comp(con, "Milagros", 400, "El profeta que sanó a Naamán fue ____.", "Eliseo", "Elías", "Isaías", "Eliseo")
        op(con, "Milagros", 400, "¿Qué cayó de los ojos de Pablo cuando recuperó la vista?", "Como escamas", "Ceniza", "Arena", "Lágrimas", "Como escamas")
        vf(con, "Milagros", 400, "Jesús expulsó una legión de demonios (relato).", "Verdadero")
        comp(con, "Milagros", 400, "Jesús resucitó al hijo de la viuda de ____.", "Naín", "Belén", "Jericó", "Naín")
        op(con, "Milagros", 400, "¿Qué instrumento usó Moisés para señales? (en relatos)", "Vara", "Espada", "Arpa", "Corona", "Vara")
        vf(con, "Milagros", 400, "Dios detuvo el sol en tiempos de Josué (relato).", "Verdadero")

        # 500
        op(con, "Milagros", 500, "¿Qué vio Ezequiel en visión que volvió a la vida?", "Huesos secos", "Árboles", "Montañas", "Ríos", "Huesos secos")
        vf(con, "Milagros", 500, "Eliseo hizo flotar un hacha (relato).", "Verdadero")
        comp(con, "Milagros", 500, "Pedro sanó a un cojo en la puerta llamada ____.", "Hermosa", "Santa", "Dorada", "Hermosa")
        op(con, "Milagros", 500, "¿Quién fue resucitada por Pedro (Hechos)?", "Tabita", "Ester", "Rut", "María", "Tabita")
        vf(con, "Milagros", 500, "Jesús sanó a diez leprosos en un relato.", "Verdadero")
        comp(con, "Milagros", 500, "Jesús multiplicó pan y peces y sobraron ____ cestas (5 mil).", "12", "7", "3", "12")
        op(con, "Milagros", 500, "¿Qué profeta fue alimentado por cuervos? (relato)", "Elías", "Eliseo", "Jonás", "Amós", "Elías")
        vf(con, "Milagros", 500, "Moisés hizo brotar agua de la roca (relato).", "Verdadero")

        # ---------- VERSÍCULOS ----------
        # 100
        comp(con, "Versículos", 100, "Dios es ____.", "amor", "sueño", "miedo", "amor")
        vf(con, "Versículos", 100, "La Biblia enseña a amar al prójimo.", "Verdadero")
        comp(con, "Versículos", 100, "Jesús dijo: Yo soy la ____ del mundo.", "luz", "espada", "roca", "luz")
        op(con, "Versículos", 100, "¿Qué dijo Jesús que Él es? (una opción)", "El camino", "El dinero", "El miedo", "La duda", "El camino")
        comp(con, "Versículos", 100, "El Señor es mi ____.", "pastor", "juez", "enemigo", "pastor")
        vf(con, "Versículos", 100, "La fe es importante en la Biblia.", "Verdadero")
        op(con, "Versículos", 100, "‘En el principio creó Dios los ____ y la tierra.’", "cielos", "mares", "montes", "ríos", "cielos")
        comp(con, "Versículos", 100, "Todo lo puedo en ____ que me fortalece.", "Cristo", "yo", "nadie", "Cristo")

        # 200
        comp(con, "Versículos", 200, "El Señor es mi pastor, nada me ____.", "faltará", "temerá", "callará", "faltará")
        vf(con, "Versículos", 200, "‘No temas’ aparece muchas veces en la Biblia.", "Verdadero")
        op(con, "Versículos", 200, "‘Honra a tu padre y a tu ____.’", "madre", "vecino", "amigo", "juez", "madre")
        comp(con, "Versículos", 200, "Ama a tu prójimo como a ti ____.", "mismo", "hijo", "padre", "mismo")
        vf(con, "Versículos", 200, "‘Jehová es mi luz y mi salvación’ es una frase bíblica.", "Verdadero")
        op(con, "Versículos", 200, "‘La oración del justo puede mucho.’ ¿a qué se refiere?", "Oración", "Dinero", "Fuerza", "Miedo", "Oración")
        comp(con, "Versículos", 200, "El fruto del Espíritu es ____ (uno).", "amor", "enojo", "pereza", "amor")
        vf(con, "Versículos", 200, "Los Salmos están en el Antiguo Testamento.", "Verdadero")

        # 300
        op(con, "Versículos", 300, "‘El justo por la ____ vivirá.’", "fe", "vista", "fuerza", "espada", "fe")
        comp(con, "Versículos", 300, "‘Buscad primero el reino de Dios y su ____.’", "justicia", "casa", "espada", "justicia")
        vf(con, "Versículos", 300, "‘El gozo del Señor es mi fortaleza’ es una idea bíblica.", "Verdadero")
        op(con, "Versículos", 300, "‘Yo soy la vid, vosotros los ____.’", "pámpanos", "troncos", "ríos", "montes", "pámpanos")
        comp(con, "Versículos", 300, "‘Lámpara es a mis pies tu ____.’", "palabra", "oro", "miedo", "palabra")
        vf(con, "Versículos", 300, "‘Dios resiste a los soberbios’ es una enseñanza bíblica.", "Verdadero")
        op(con, "Versículos", 300, "‘El amor es ____.’ (opción correcta)", "paciente", "orgulloso", "cruel", "duro", "paciente")
        comp(con, "Versículos", 300, "‘Fiel es Dios’ (completa): ‘que no os dejará ser tentados más de lo que podáis ____.’", "resistir", "correr", "olvidar", "resistir")

        # 400
        op(con, "Versículos", 400, "‘Bienaventurados los de limpio ____.’", "corazón", "brazo", "cuerpo", "rumor", "corazón")
        comp(con, "Versículos", 400, "‘La paga del pecado es ____.’", "muerte", "oro", "honor", "muerte")
        vf(con, "Versículos", 400, "‘Por gracia sois salvos’ es una enseñanza del Nuevo Testamento.", "Verdadero")
        op(con, "Versículos", 400, "‘En todo tiempo ama el ____.’", "amigo", "oro", "enemigo", "juez", "amigo")
        comp(con, "Versículos", 400, "‘El principio de la sabiduría es el temor de ____.’", "Dios", "hombre", "tierra", "Dios")
        vf(con, "Versículos", 400, "‘No os conforméis a este siglo’ es un consejo bíblico.", "Verdadero")
        op(con, "Versículos", 400, "‘El que perseverare hasta el fin, éste será ____.’", "salvo", "rico", "fuerte", "temido", "salvo")
        comp(con, "Versículos", 400, "‘La fe viene por el oír, y el oír por la palabra de ____.’", "Dios", "hombre", "rey", "Dios")

        # 500
        op(con, "Versículos", 500, "‘El verbo se hizo ____.’", "carne", "oro", "cielo", "mar", "carne")
        comp(con, "Versículos", 500, "‘Yo sé los ____ que tengo acerca de vosotros’ (idea bíblica).", "planes", "miedos", "castigos", "planes")
        vf(con, "Versículos", 500, "‘Todo tiene su tiempo’ es una idea de Eclesiastés.", "Verdadero")
        op(con, "Versículos", 500, "‘El Señor dará ____ a su pueblo; el Señor bendecirá a su pueblo con paz.’", "fuerza", "miedo", "tristeza", "noche", "fuerza")
        comp(con, "Versículos", 500, "‘Si Dios es por nosotros, ¿quién contra ____?’", "nosotros", "ellos", "nadie", "nosotros")
        vf(con, "Versículos", 500, "‘El amor nunca deja de ser’ es una frase de 1 Corintios 13.", "Verdadero")
        op(con, "Versículos", 500, "‘El que habita al abrigo del Altísimo morará bajo la sombra del ____.’", "Omnipotente", "faraón", "césar", "juez", "Omnipotente")
        comp(con, "Versículos", 500, "‘Vengan a mí todos los que están trabajados y cargados, y yo los haré ____.’", "descansar", "correr", "caer", "descansar")

        con.commit()

def cargar_extra_100():
    """+100 preguntas (4 por cada categoria+dificultad) para llegar a 300."""
    with connect() as con:

        # ===== HISTORIA (extra) =====
        # 100
        op(con, "Historia", 100, "¿Quién creó el mundo?", "Dios", "Moisés", "Noé", "David", "Dios")
        vf(con, "Historia", 100, "Adán y Eva vivían en el Edén.", "Verdadero")
        comp(con, "Historia", 100, "Jesús nació de la virgen ____.", "María", "Marta", "Sara", "María")
        op(con, "Historia", 100, "¿Quién fue el primer rey de Israel?", "Saúl", "David", "Salomón", "Samuel", "Saúl")

        # 200
        vf(con, "Historia", 200, "El arca del pacto era un objeto sagrado para Israel.", "Verdadero")
        op(con, "Historia", 200, "¿Qué plaga ocurrió en Egipto? (una)", "Langostas", "Nieve", "Tormenta de arena", "Volcanes", "Langostas")
        comp(con, "Historia", 200, "El rey que pidió sabiduría fue ____.", "Salomón", "Saúl", "Ciro", "Salomón")
        op(con, "Historia", 200, "¿Quién fue sacado de Egipto siendo bebé en una canasta?", "Moisés", "José", "Samuel", "Isaías", "Moisés")

        # 300
        vf(con, "Historia", 300, "Jericó cayó después de rodearla varios días.", "Verdadero")
        op(con, "Historia", 300, "¿Quién derrotó a los madianitas con 300 hombres?", "Gedeón", "Sansón", "Saúl", "Eliseo", "Gedeón")
        comp(con, "Historia", 300, "Dios habló a Moisés desde una zarza ____.", "ardiente", "seca", "verde", "ardiente")
        op(con, "Historia", 300, "¿Quién construyó los muros de Jerusalén?", "Nehemías", "Esdras", "Daniel", "Josué", "Nehemías")

        # 400
        vf(con, "Historia", 400, "El pueblo de Judá fue llevado al exilio en Babilonia (relato).", "Verdadero")
        op(con, "Historia", 400, "¿Qué profeta desafió a los profetas de Baal?", "Elías", "Jonás", "Amós", "Zacarías", "Elías")
        comp(con, "Historia", 400, "La reina que ayudó a su pueblo en Persia fue ____.", "Ester", "Rut", "Débora", "Ester")
        op(con, "Historia", 400, "¿Quién interpretó sueños en Babilonia?", "Daniel", "José", "Samuel", "Pablo", "Daniel")

        # 500
        vf(con, "Historia", 500, "Zorobabel estuvo relacionado con el retorno del exilio (relato).", "Verdadero")
        op(con, "Historia", 500, "¿Qué libro habla del regreso y reconstrucción tras el exilio? (uno)", "Nehemías", "Rut", "Jonás", "Job", "Nehemías")
        comp(con, "Historia", 500, "El profeta llevado cautivo a Babilonia fue ____.", "Daniel", "Amós", "Oseas", "Daniel")
        op(con, "Historia", 500, "¿Quién fue el rey que permitió el retorno (relato)?", "Ciro", "Saúl", "Herodes", "Faraón", "Ciro")

        # ===== PERSONAJES (extra) =====
        # 100
        op(con, "Personajes", 100, "¿Quién era el padre de Isaac?", "Abraham", "Jacob", "José", "Moisés", "Abraham")
        vf(con, "Personajes", 100, "Jesús tuvo discípulos.", "Verdadero")
        comp(con, "Personajes", 100, "El gigante derrotado por David fue ____.", "Goliat", "Herodes", "Nabucodonosor", "Goliat")
        op(con, "Personajes", 100, "¿Quién fue tragado por un gran pez?", "Jonás", "Pedro", "Pablo", "Samuel", "Jonás")

        # 200
        vf(con, "Personajes", 200, "Josué tomó el liderazgo después de Moisés.", "Verdadero")
        op(con, "Personajes", 200, "¿Quién fue juez y profetisa?", "Débora", "Ester", "Rut", "María", "Débora")
        comp(con, "Personajes", 200, "El amigo fiel de David fue ____.", "Jonatán", "Absalón", "Saúl", "Jonatán")
        op(con, "Personajes", 200, "¿Quién fue rey y conocido por su sabiduría?", "Salomón", "Saúl", "David", "Ciro", "Salomón")

        # 300
        vf(con, "Personajes", 300, "Mateo fue uno de los doce discípulos.", "Verdadero")
        op(con, "Personajes", 300, "¿Quién escribió muchas cartas del NT?", "Pablo", "Noé", "Abraham", "Isaías", "Pablo")
        comp(con, "Personajes", 300, "El que bautizaba en el Jordán era Juan el ____.", "Bautista", "Amado", "Sabio", "Bautista")
        op(con, "Personajes", 300, "¿Quién traicionó a Jesús?", "Judas", "Pedro", "Juan", "Tomás", "Judas")

        # 400
        vf(con, "Personajes", 400, "Booz fue pariente redentor en el libro de Rut (relato).", "Verdadero")
        op(con, "Personajes", 400, "¿Quién fue lanzado al horno de fuego con otros?", "Sadrac", "Pedro", "Ester", "Esdras", "Sadrac")
        comp(con, "Personajes", 400, "El profeta que fue tragado por un pez fue ____.", "Jonás", "Amós", "Joel", "Jonás")
        op(con, "Personajes", 400, "¿Quién fue copero del rey y reconstruyó muros?", "Nehemías", "Daniel", "Josué", "Saúl", "Nehemías")

        # 500
        vf(con, "Personajes", 500, "Apolos fue un predicador mencionado en Hechos (relato).", "Verdadero")
        op(con, "Personajes", 500, "¿Quién escribió muchos proverbios?", "Salomón", "David", "Moisés", "Ester", "Salomón")
        comp(con, "Personajes", 500, "El padre de Juan el Bautista se llamaba ____.", "Zacarías", "Simeón", "Ananías", "Zacarías")
        op(con, "Personajes", 500, "¿Quién recibió la visión en Patmos?", "Juan", "Pablo", "Pedro", "Lucas", "Juan")

        # ===== LUGARES (extra) =====
        # 100
        op(con, "Lugares", 100, "¿En qué ciudad nació Jesús?", "Belén", "Nazaret", "Jerusalén", "Éfeso", "Belén")
        vf(con, "Lugares", 100, "El río Jordán existe en relatos bíblicos.", "Verdadero")
        comp(con, "Lugares", 100, "Jesús fue criado en ____.", "Nazaret", "Belén", "Roma", "Nazaret")
        op(con, "Lugares", 100, "¿Dónde vivía el faraón? (país)", "Egipto", "Israel", "Grecia", "Persia", "Egipto")

        # 200
        vf(con, "Lugares", 200, "Jericó era una ciudad amurallada (relato).", "Verdadero")
        op(con, "Lugares", 200, "¿A qué ciudad fue Jonás a predicar?", "Nínive", "Belén", "Jerusalén", "Roma", "Nínive")
        comp(con, "Lugares", 200, "Moisés recibió la ley en el monte ____.", "Sinaí", "Carmelo", "Sion", "Sinaí")
        op(con, "Lugares", 200, "¿Dónde estaba el templo principal de Israel?", "Jerusalén", "Belén", "Nazaret", "Jericó", "Jerusalén")

        # 300
        vf(con, "Lugares", 300, "Capernaúm fue un lugar del ministerio de Jesús.", "Verdadero")
        op(con, "Lugares", 300, "¿Dónde estuvo Daniel en cautiverio?", "Babilonia", "Egipto", "Roma", "Grecia", "Babilonia")
        comp(con, "Lugares", 300, "El sermón del monte se asocia a un ____.", "monte", "río", "desierto", "monte")
        op(con, "Lugares", 300, "¿En qué región se menciona el Mar de Galilea?", "Galilea", "Roma", "Persia", "India", "Galilea")

        # 400
        vf(con, "Lugares", 400, "Patmos se relaciona con Juan (Apocalipsis).", "Verdadero")
        op(con, "Lugares", 400, "¿A dónde huyó José con María y Jesús para protegerlo?", "Egipto", "Roma", "Babilonia", "Nínive", "Egipto")
        comp(con, "Lugares", 400, "El monte asociado con Elías frente a Baal es ____.", "Carmelo", "Sinaí", "Hermón", "Carmelo")
        op(con, "Lugares", 400, "¿Dónde se celebró un concilio importante en Hechos 15?", "Jerusalén", "Éfeso", "Filipos", "Roma", "Jerusalén")

        # 500
        vf(con, "Lugares", 500, "El Éufrates es un río mencionado en la Biblia.", "Verdadero")
        op(con, "Lugares", 500, "¿En qué isla estuvo Juan cuando recibió Apocalipsis?", "Patmos", "Malta", "Creta", "Chipre", "Patmos")
        comp(con, "Lugares", 500, "La ciudad donde llamaron cristianos por primera vez a los discípulos fue ____.", "Antioquía", "Belén", "Nínive", "Antioquía")
        op(con, "Lugares", 500, "¿En qué ciudad estaba el templo de Artemisa?", "Éfeso", "Roma", "Jerusalén", "Belén", "Éfeso")

        # ===== MILAGROS (extra) =====
        # 100
        vf(con, "Milagros", 100, "Jesús calmó una tormenta (relato).", "Verdadero")
        op(con, "Milagros", 100, "¿Qué convirtió Jesús en vino?", "Agua", "Aceite", "Leche", "Miel", "Agua")
        comp(con, "Milagros", 100, "Jesús caminó sobre el ____.", "agua", "fuego", "hielo", "agua")
        op(con, "Milagros", 100, "¿A quién resucitó Jesús en Betania?", "Lázaro", "Zaqueo", "Bartimeo", "Jairo", "Lázaro")

        # 200
        vf(con, "Milagros", 200, "Jesús sanó a un leproso (relato).", "Verdadero")
        op(con, "Milagros", 200, "¿Cuántos panes se mencionan en la alimentación de 5,000? (relato)", "5", "7", "12", "2", "5")
        comp(con, "Milagros", 200, "Jesús sanó a un ciego llamado ____ (relato).", "Bartimeo", "Natanael", "Felipe", "Bartimeo")
        op(con, "Milagros", 200, "¿Qué multiplicó Jesús para alimentar a la multitud?", "Panes y peces", "Uvas y miel", "Carne y agua", "Aceite y trigo", "Panes y peces")

        # 300
        vf(con, "Milagros", 300, "Pedro caminó sobre el agua por un momento (relato).", "Verdadero")
        op(con, "Milagros", 300, "¿Dónde convirtió Jesús agua en vino?", "Caná", "Belén", "Jericó", "Roma", "Caná")
        comp(con, "Milagros", 300, "Jesús sanó a la suegra de ____.", "Pedro", "Juan", "Mateo", "Pedro")
        op(con, "Milagros", 300, "¿Qué hizo Jesús con la higuera sin fruto? (relato)", "La secó", "La plantó", "La cortó", "La regó", "La secó")

        # 400
        vf(con, "Milagros", 400, "Pablo y Silas cantaron y hubo un terremoto en la cárcel (relato).", "Verdadero")
        op(con, "Milagros", 400, "¿Qué cayó de los ojos de Pablo cuando recuperó la vista? (relato)", "Como escamas", "Ceniza", "Arena", "Lágrimas", "Como escamas")
        comp(con, "Milagros", 400, "El profeta que sanó a Naamán fue ____.", "Eliseo", "Elías", "Isaías", "Eliseo")
        op(con, "Milagros", 400, "¿Qué milagro ocurrió en Pentecostés? (relato)", "Lenguas", "Oscuridad", "Lluvia", "Hambre", "Lenguas")

        # 500
        vf(con, "Milagros", 500, "Eliseo hizo flotar un hacha (relato).", "Verdadero")
        op(con, "Milagros", 500, "¿Quién fue resucitada por Pedro en Hechos? (relato)", "Tabita", "Rut", "Ester", "María", "Tabita")
        comp(con, "Milagros", 500, "Pedro sanó a un cojo en la puerta llamada ____.", "Hermosa", "Santa", "Dorada", "Hermosa")
        op(con, "Milagros", 500, "¿Qué profeta fue alimentado por cuervos? (relato)", "Elías", "Eliseo", "Jonás", "Amós", "Elías")

        # ===== VERSÍCULOS (extra) =====
        # 100
        comp(con, "Versículos", 100, "Dios es ____.", "amor", "miedo", "duda", "amor")
        op(con, "Versículos", 100, "Completa: 'Todo lo puedo en ____ que me fortalece.'", "Cristo", "mí", "nadie", "todos", "Cristo")
        vf(con, "Versículos", 100, "La Biblia enseña a amar al prójimo.", "Verdadero")
        comp(con, "Versículos", 100, "El Señor es mi ____.", "pastor", "enemigo", "temor", "pastor")

        # 200
        comp(con, "Versículos", 200, "El Señor es mi pastor, nada me ____.", "faltará", "temerá", "callará", "faltará")
        op(con, "Versículos", 200, "Completa: 'Honra a tu padre y a tu ____.'", "madre", "amigo", "vecino", "juez", "madre")
        vf(con, "Versículos", 200, "Los Salmos están en el Antiguo Testamento.", "Verdadero")
        comp(con, "Versículos", 200, "Ama a tu prójimo como a ti ____.", "mismo", "solo", "lejos", "mismo")

        # 300
        op(con, "Versículos", 300, "Completa: 'El justo por la ____ vivirá.'", "fe", "vista", "fuerza", "espada", "fe")
        comp(con, "Versículos", 300, "Lámpara es a mis pies tu ____.", "palabra", "oro", "fuerza", "palabra")
        vf(con, "Versículos", 300, "‘Dios resiste a los soberbios’ es una enseñanza bíblica.", "Verdadero")
        op(con, "Versículos", 300, "Completa: 'Yo soy la vid, vosotros los ____.'", "pámpanos", "ríos", "montes", "troncos", "pámpanos")

        # 400
        op(con, "Versículos", 400, "Completa: 'La paga del pecado es ____.'", "muerte", "oro", "honor", "fama", "muerte")
        comp(con, "Versículos", 400, "El principio de la sabiduría es el temor de ____.", "Dios", "hombre", "rey", "Dios")
        vf(con, "Versículos", 400, "‘Por gracia sois salvos’ es una enseñanza del NT.", "Verdadero")
        op(con, "Versículos", 400, "Completa: 'Bienaventurados los de limpio ____.'", "corazón", "brazo", "cuerpo", "rumor", "corazón")

        # 500
        op(con, "Versículos", 500, "Completa: 'El Verbo se hizo ____.'", "carne", "oro", "cielo", "mar", "carne")
        comp(con, "Versículos", 500, "Completa: 'Si Dios es por nosotros, ¿quién contra ____?'", "nosotros", "ellos", "nadie", "nosotros")
        vf(con, "Versículos", 500, "‘Todo tiene su tiempo’ es una idea de Eclesiastés.", "Verdadero")
        op(con, "Versículos", 500, "Completa: 'El que habita al abrigo del Altísimo... del ____.'", "Omnipotente", "faraón", "césar", "juez", "Omnipotente")

        con.commit()

def contar_preguntas():
    with connect() as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM preguntas")
        return cur.fetchone()[0]

def obtener_pregunta_random(categoria: str, dificultad: int):
    """Devuelve una pregunta random NO usada o None."""
    with connect() as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(
            """
            SELECT * FROM preguntas
            WHERE categoria=? AND dificultad=? AND usada=0
            ORDER BY RANDOM()
            LIMIT 1
            """,
            (categoria, int(dificultad))
        )
        row = cur.fetchone()
        return dict(row) if row else None

def obtener_preguntas_para_tablero(categorias, valores):
    """
    Devuelve un diccionario {(r,c): pregunta_dict} para un tablero 5x5
    escogiendo al azar una pregunta NO usada por cada (categoria, dificultad).
    """
    tablero = {}
    for r, val in enumerate(valores):
        for c, cat in enumerate(categorias):
            q = obtener_pregunta_random(cat, val)
            tablero[(r, c)] = q  # puede ser None si no hay
    return tablero

def marcar_pregunta_usada(pregunta_id: int):
    with connect() as con:
        con.execute("UPDATE preguntas SET usada=1 WHERE id=?", (int(pregunta_id),))
        con.commit()


def main():
    crear_db()

    # Si quieres reiniciar el banco desde cero, descomenta:
    borrar_todo()

    cargar_banco_200()
    cargar_extra_100()

    print(f"✅ Banco cargado en {DB_NAME}. Total preguntas: {contar_preguntas()}")


if __name__ == "__main__":
    main()
