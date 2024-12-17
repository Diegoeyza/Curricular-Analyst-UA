import psycopg2

# Connect to the external PostgreSQL database (replace with actual credentials)
external_db_conn = psycopg2.connect(
    host="localhost",
    database="links_ra",  # External DB
    user="postgres",
    password="bduandes"
)

# Connect to the first local PostgreSQL database (replace with actual credentials)
local_db_1_conn = psycopg2.connect(
    host="localhost",
    database="management",  # First local DB name
    user="postgres",
    password="bduandes"
)

def import_data():
    id_counter = 1
    
    # Delete all data in the destination tables before loading new data
    with local_db_1_conn.cursor() as cursor_1:
        cursor_1.execute("TRUNCATE TABLE course_management_course RESTART IDENTITY CASCADE;")
        cursor_1.execute("TRUNCATE TABLE course_management_objective RESTART IDENTITY CASCADE;")
        cursor_1.execute("TRUNCATE TABLE course_management_requirement RESTART IDENTITY CASCADE;")
        cursor_1.execute("TRUNCATE TABLE course_management_ralink RESTART IDENTITY CASCADE;")
    local_db_1_conn.commit()
    
    # Fetch data from the 'courses' table from the external database
    with external_db_conn.cursor() as cursor:
        cursor.execute("SELECT id, nombre FROM courses")
        courses = cursor.fetchall()

    # Insert courses into the local PostgreSQL database
    for course in courses:
        course_id, course_name = course
        
        with local_db_1_conn.cursor() as cursor_1:
            cursor_1.execute("""
                INSERT INTO course_management_course (id, id_curso, nombre)
                VALUES (%s, %s, %s)
            """, (id_counter, course_id, course_name))
        id_counter += 1

    # Fetch data from the 'objectives' table from the external database
    with external_db_conn.cursor() as cursor:
        cursor.execute("""
            SELECT id, id_objetivo, nombre, objetivo FROM objectives
        """)
        objectives = cursor.fetchall()

    # Insert objectives into the local PostgreSQL database
    for obj in objectives:
        course_id, objective_id, objective_name, objective_text = obj
        
        with local_db_1_conn.cursor() as cursor_1:
            cursor_1.execute("""
                INSERT INTO course_management_objective (id, id_objetivo, id_curso, nombre, objetivo)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_counter, objective_id, course_id, objective_name, objective_text))
        id_counter += 1

    # Fetch data from the 'requirements' table from the external database
    with external_db_conn.cursor() as cursor:
        cursor.execute("""
            SELECT id, id_requisito FROM requirements
        """)
        requirements = cursor.fetchall()

    # Insert requirements into the local PostgreSQL database
    for req in requirements:
        requirement_id, prerequisite_id = req
        
        with local_db_1_conn.cursor() as cursor_1:
            cursor_1.execute("""
                INSERT INTO course_management_requirement (id, id_curso, id_requisito)
                VALUES (%s, %s, %s)
            """, (id_counter, requirement_id, prerequisite_id))
        id_counter += 1

    # Fetch data from the 'ra_links' table from the external database
    with external_db_conn.cursor() as cursor:
        cursor.execute("""
            SELECT id, id_objetivo, id_prerequisito, id_objetivo_prerequisito, importancia FROM ra_links
        """)
        ra_links = cursor.fetchall()

    # Insert RA links into the local PostgreSQL database
    for link in ra_links:
        link_id, objective_id, prerequisite_id, objective_prerequisite_id, importance = link
        
        with local_db_1_conn.cursor() as cursor_1:
            cursor_1.execute("""
                INSERT INTO course_management_ralink (id, id_curso, id_objetivo, id_prerequisito, id_objetivo_prerequisito, importancia)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (id_counter, link_id, objective_id, prerequisite_id, objective_prerequisite_id, importance))
        id_counter += 1
        
    # Commit changes to the local database
    local_db_1_conn.commit()

    # Close the database connections
    external_db_conn.close()
    local_db_1_conn.close()

# Run the import function
import_data()
