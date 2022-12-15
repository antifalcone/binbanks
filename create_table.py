import psycopg2

try:
    connection = psycopg2.connect(
        host="127.0.0.1",
        user="root",
        password="roottoor",
        database="binbanks"
    )
    with connection.cursor() as cursor:
        cursor.execute(
        """
            CREATE TABLE binlist (
                    bank_bin integer NOT NULL,
                    bank_name text NOT NULL,
                    bank_country text NOT NULL
                    );
                """
        )
        connection.commit()
        cursor.execute(
        """
            CREATE TABLE top10 (
                    top integer ARRAY[10]
                    );
                """
        )
        connection.commit()
except Exception as ex:
	print(ex)
