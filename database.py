import sqlite3

connection=sqlite3.connect("database.db")
cursor=connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS simulation_log (
               id_simulation INTEGER PRIMARY KEY AUTOINCREMENT,
               game_mode TEXT,
               seconds INTEGER,
               total_born INTEGER,
               total_deaths INTEGER 
               )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS species_performance (
               id_register INTEGER PRIMARY KEY AUTOINCREMENT,
               id_simulation INTEGER,
               main_gene INTEGER,

               initial_population INTEGER,
               final_population INTEGER,
               population_peak INTEGER,
               max_generation INTEGER,

               FOREIGN KEY (id_simulation) REFERENCES simulation_log(id_simulation)
               )""")

def save_simulation_log(game_mode, seconds, total_born, total_deaths):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""INSERT INTO simulation_log (
                   game_mode,
                   seconds,
                   total_born,
                   total_deaths
                   ) VALUES (?, ?, ?, ?)""", (game_mode, seconds, total_born, total_deaths))
    created_id=cursor.lastrowid
    connection.commit()
    connection.close()

    return created_id

def save_species_performance(species_data):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.executemany("""INSERT INTO species_performance (
                       id_simulation, main_gene, initial_population, final_population, population_peak, max_generation)
                       VALUES (?, ?, ?, ?, ?, ?)""", species_data)
    
    connection.commit()
    connection.close()

connection.commit()
connection.close()