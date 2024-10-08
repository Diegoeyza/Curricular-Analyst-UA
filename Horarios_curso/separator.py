import pandas as pd
import re

def separator(file, out):
    # Load the CSV file with course data
    df = pd.read_csv(file, sep=';')

    # Define the replacement names directly in the code
    replacements = {
        "AEIC": "Álgebra e introducción al cálculo",
        "ANTROPOLOGIA FILOSOFICA": "Antropología Filosófica",
        "BIOLOGIA": "Biología de los Microorganismos",
        "CALCULO I": "Cálculo I",
        "CALCULO II": "Cálculo II",
        "ETICA": "Ética",
        "ECUACIONES": "Ecuaciones Diferenciales",
        "ELECTRO": "Electricidad y Magnetismo",
        "ESTATICA": "Estática",
        "FUNDAMENTOS DE ECONOMIA": "Fundamentos de Economía",
        "FUNDAMENTOS ECONOMIA": "Fundamentos de Economía",
        "QUIMICA": "Fundamentos de Química",
        "INTRO A LA MECANICA": "Introducción a la Mecánica",
        "MECANICA Y ONDAS": "Mecánica y Ondas",
        "PROBABILIDADES": "Probabilidades y Estadística",
        "PROGRAMACION": "Programación",
        "TPI": "Taller de Proyectos de Ingeniería",
        "TERMO": "Termodinámica",
        "ALGEBRA LINEAL": "Álgebra Lineal",
        "ANALISIS DE CIRCUITOS": "Análisis de Circuitos",
        "ANALISIS ESTRUCTURAL": "Análisis Estructural",
        "ARQUITECTURA DE COMPUTADORES": "Arquitectura de Computadores",
        "BASES DE DATOS": "Bases de Datos",
        "CONTABILIDAD": "Contabilidad y Estados Financieros",
        "ESTRUCTURAS DE DATOS Y ALGORITMOS": "Estructuras de Datos y Algoritmos",
        "FILOSOFIA DE LAS CIENCIAS": "Filosofía de las Ciencias",
        "FLUID MECHANICS": "Fluid Mechanics",
        "HIDRAULICA": "Hidráulica",
        "MATERIALES DE CONSTRUCCION": "Materiales de Construcción",
        "METODOS ESTAD PARA LA GEST": "Métodos Estadísticos para la Gestión",
        "MICROBIOLOGIA": "Microbiología Industrial y Ambiental",
        "MICROECONOMIA": "Microeconomía",
        "MODELOS ESTOCASTICOS": "Modelos Estocásticos",
        "OPTICAL SYSTEM": "Optical Systems",
        "OPTIMIZACION": "Optimización",
        "PARADIGMAS": "Paradigmas de Programación",
        "PBN": "Programación de Bajo Nivel",
        "PROCESAMIENTO DE SEÑALES": "Procesamiento de Señales",
        "PROGRAMACION MATEMATICA": "Programación Matemática",
        "SISTEMAS DE TRANSPORTE": "Sistemas de Transporte",
        "SISTEMAS DIGITALES AVANZADOS": "Sistemas Digitales Avanzados",
        "SISTEMAS ELECTRÓNICOS": "Sistemas Electrónicos",
        "SISTEMAS OPERATIVOS Y REDES": "Sistemas Operativos y Redes",
        "TEORIA DE TRAFICO VEHICULAR": "Teoría de Tráfico Vehicular",
        "TOPOGRAFIA APLICADA": "Topografía Aplicada",
        "TRANSFERENCIA DE CALOR": "Transferencia de Calor",
        "TRANSFERENCIA DE MASA": "Transferencia de Masa",
        "MEDIO AMBIENTE Y ENERGIA": "Medio Ambiente y Energía",
        "APLICACIONES MOVILES": "Aplicaciones Móviles",
        "ARTIFIAL INTELLIGENCE": "Artificial Intelligence",
        "ARTIFICIAL INTELLIGENCE": "Artificial Intelligence",
        "CINETICA Y DISEÑO DE REACTORES QUIMICOS": "Cinética y Diseño de Reactores Químicos",
        "COMUNICACIONES DIGITALES": "Comunicaciones Digitales",
        "CONTROL AUTOMATICO": "Control Automático",
        "DISEÑO Y EVALUACION DE PROYECTOS": "Diseño y Evaluación de Proyectos Industriales",
        "DISEÑO Y OPTIMIZACION DE PROCESOS IND": "Diseño y Optimización de Procesos Industriales",
        "ECONOMETRIA": "Econometría",
        "FINANZAS I": "Finanzas I",
        "HIDROLOGIA": "Hidrología",
        "INGENIERIA DE BIOPROCESOS": "Ingeniería de Bioprocesos Ambientales",
        "INTRO A LA ING DE SOFTWARE": "Introducción a la Ingeniería de Software",
        "MACROECONOMIA": "Macroeconomía",
        "METODOS COMPUTACIONALES EN IOC": "Métodos Computacionales en Obras Civiles",
        "METODOS Y TECNICAS DE CONST": "Métodos y Técnicas de Construcción",
        "PENSAMIENTO DE DISEÑO": "Pensamiento de Diseño Aplicado a Ingeniería",
        "POTENCIA ELECTRICA": "Potencia Eléctrica",
        "PROYECTO DE DESARROLLO DE SOFTWARE": "Proyecto de Desarrollo de Software",
        "WEB TECHNOLOGIES": "Web Technologies",
        "ADMINISTRACION Y CONTROL DE PROYECTOS": "Administración y Control de Proyectos",
        "ANALITICA TEXTUAL CON MACHINE LEARNING": "Analítica Textual con Machine Learning",
        "CONSULTORIA DE DATOS": "Consultoría de Datos",
        "CONT Y DES DE TEC DE REMED DE SUELO": "Gestión Residuos Sólidos y Remediación de Suelos",
        "CONTROL DE CONVERTIDORES": "Control de Convertidores",
        "DEEP LEARNING": "Deep Learning",
        "DISEÑO AVANZADO DE REACTORES QUIMICOS": "Diseño Avanzado de Reactores Químicos",
        "DISEÑO DE AEROGENERADORES": "Diseño de Aerogeneradores",
        "DISEÑO SISMORRESISTENTE": "Diseño Sismorresistente",
        "ECONOMIA AMBIENTAL Y DE LOS REC": "Economía Ambiental y de los Recursos Naturales",
        "GESTION DE PERSONAS": "Gestión de Personas y Desarrollo Organizacional",
        "GESTION DE PROYECTOS DE SOFTWARE": "Gestión de Proyectos de Software",
        "GESTION ESTRATEGICA": "Gestión Estratégica",
        "GESTION FINANCIERA": "Gestión Financiera",
        "HORMIGON ARMADO AVANZADO": "Hormigón Armado Avanzado",
        "INGENIERIA DEL FACTOR HUMANO": "Ingeniería del Factor Humano",
        "INGENIERIA VIAL": "Ingeniería Vial",
        "LAB DE CIBERSEGURIDAD OFENSIVA": "Ciberseguridad Ofensiva",
        "LOGISTICS": "Logistics",
        "MARKETING": "Marketing",
        "METODOLOGIA DE LA INVESTIGACIÓN": "Metodología de la Investigación",
        "MODELAMIENTO DEL TRANSPORTE": "Modelamiento de Transporte",
        "ORGANIZACIÓN INDUSTRIAL": "Organización Industrial",
        "PRINC. ESTETICOS DISEÑO INTERFACES": "Principios Estéticos del Diseño de Interfaces",
        "PROCESAMIENTO DIGITAL DE IMÁGENES": "Procesamiento Digital de Imágenes",
        "PROTECCIONES ELECTRICAS": "Protecciones Eléctricas",
        "PROY DE INFR HIDR": "Proyecto de Infraestructura Hidráulica",
        "PROYECTO DE TITULO 1": "Proyecto de Titulo 1",
        "PROYECTO DE TITULO 2": "Proyecto de Titulo 2",
        "REDES DE COMUNICACIÓN": "Redes de Comunicación",
        "SEMINARIO DE ETICA PROFESIONAL": "Seminario de Ética Profesional",
        "SEMINARIO DE TESIS 1": "Seminario de Tesis 1",
        "SEMINARIO DE TESIS I": "Seminario de Tesis I",
        "SOFTWARE ARCHITECTURE": "Software Architecture",
        "TECNOLOGIA DEL HORMIGON": "Tecnología del Hormigón",
        "TOPICOS AVANZADOS EN HA": "Tópicos Avanzados en HA",
        "VENTURE CAPITAL": "Venture Capital",
        "WASTEWATER TREATMENT": "Wastewater Treatment",
    }


    # Function to separate the course column into name, type, and section
    def separate_course(course):
        match = re.match(r'^(.*?) \((.*?)\) SEC (\d+)$', course)
        if match:
            return match.groups()  # Return the three groups as a tuple
        return course, None, None  # Return original course and None for others if it doesn't match

    # Apply the separation function to the course column
    df[['name', 'type', 'section']] = df['course'].apply(separate_course).apply(pd.Series)

    # Replace the names in the 'name' column using the replacements dictionary
    df['name'] = df['name'].replace(replacements).fillna(df['name'])

    # Drop the original course column
    df = df.drop(columns=['course'])

    # Save the modified DataFrame to a new CSV file
    df.to_csv(out, sep=';', index=False)

    print(f"Separation complete. The modified schedule is saved as {out}.")

#separator("merged_schedule.csv", "separated_schedule.csv")