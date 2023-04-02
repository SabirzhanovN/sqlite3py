import sqlite3


def create_tables(connection) -> str:
    cursor = connection.cursor()

    cursor.execute('''
                    CREATE TABLE countries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL
                    );
                    ''')

    cursor.execute("""
                CREATE TABLE cities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    area REAL DEFAULT 0,
                    country_id INTEGER,
                    FOREIGN KEY (country_id) REFERENCES countries (id)
                );
                """)

    cursor.execute("""
                CREATE TABLE employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    city_id INTEGER,
                    FOREIGN KEY (city_id) REFERENCES cities (id)
                );
                """)

    connection.commit()
    print("Done!")

def insert_data(connection) -> None:
    cursor = connection.cursor()

    cursor.execute("""
                    INSERT INTO countries (title) 
                    VALUES ('Kyrgyzstan'), 
                        ('Kazakstan'), 
                        ('Uzbekstan');
                    """)

    cursor.execute("""
                    INSERT INTO cities (title, area, country_id)
                    VALUES ("Osh", 42001, 1),
                        ("Naryn", 43002, 1),
                        ("Jalal-Abad", 44003, 1),
                        ("Batken", 45004, 1),
                        ("Talas", 46005, 1),
                        ("Issyk-Kol", 47006, 1),
                        ("Chuy", 48007, 1),

                        ("NURSULTAN", 999999, 2),
                        ("Almaty", 12000, 2),
                        ("Astana", 34555, 2),
                        ("Shymkent", 22000, 2),
                        ("Atyrau", 92000, 2),

                        ("Pekin", 92000, 3),
                        ("Urumchi", 34, 3),
                        ("NEZNAU_CHTO_DALSHE", 4233, 3);
                    """)

    cursor.execute("""
                    INSERT INTO employees (first_name, last_name, city_id)
                    VALUES  ("NURSULTAN", "SABIRZHANOV", 7),
                            ("Atynay", "Toktorova", 7),
                            ("John", "Doe", 1),
                            ("Jane", "Smith", 2),
                            ("Bob", "Johnson", 1),
                            ("Alice", "Brown", 2),
                            ("Tom", "Wilson", 13),
                            ("Sara", "Garcia", 2),
                            ("Mike", "Martinez", 3),
                            ("Emily", "Davis", 3),
                            ("David", "Lee", 8),
                            ("Karen", "Taylor", 8),
                            ("Brian", "Miller", 12),
                            ("Lisa", "Anderson", 9),
                            ("Paul", "Clark", 7),
                            ("Amy", "Scott", 7),
                            ("Mark", "Robinson", 5);
                    """)

    connection.commit()
    print("Done!")


def program(connection) -> None:
    while True:
        print("""
        Вы можете отобразить список сотрудников по выбранному id города из перечня городов ниже, 
        для выхода из программы введите 0
        _________________________________
        """)

        cursor = connection.cursor()

        cursor.execute("""SELECT id, title FROM cities;""")
        for id, city in cursor.fetchall():
            print(f"{city} - {id}")

        id = int(input("\nEnter id: "))

        if id == 0:
            print("Goodbye!")
            break
        else:
            cursor.execute("""
                SELECT e.first_name, e.last_name, ci.title, co.title
                FROM employees e 
                INNER JOIN cities ci
                ON e.city_id = ci.id and e.city_id == {id}
                INNER JOIN countries co
                ON ci.country_id = co.id;
            """.format(id=id))
            employees = cursor.fetchall()
            if employees:
                print()
                for name, surname, city, country in employees:
                    print(f"Fullname: {surname} {name}\nCity: {city}\nCountry: {country}\n")

                question = input("Are you want to continue?(y/n)")
                if question == "y":
                    continue
                else:
                    print("GoodBye!")
                    break
            else:
                print("There are not employees from this city!")
                question = input("Are you want to continue?(y/n)")
                if question == "y":
                    continue
                else:
                    print("GoodBye!")
                    break



def main():
    connect = sqlite3.connect("altynay_db.db")

    # call this methods ones! Then comment them!

    #create_tables(connection=connect)
    #insert_data(connection=connect)

    program(connection=connect)

if __name__ == "__main__":
    main()
