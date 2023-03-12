import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="gymbuddy_db",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS user;')
cur.execute('CREATE TABLE user (id serial PRIMARY KEY,'
                                 'name varchar (25) NOT NULL,'
                                 'username varchar (25) NOT NULL,'
                                 'email varchar (50) NOT NULL,'
                                 'password varchar (25) NOT NULL,'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
  )

# Insert data into the table

cur.execute('INSERT INTO user (name, username, email, password)'
            'VALUES (%s, %s, %s, %s)',
            ('Abby S',
             'Asanti0116',
             prican1011@gmail.com,
             'tiago420!')
            )


cur.execute('INSERT INTO user (name, username, email, password)'
            'VALUES (%s, %s, %s, %s)',
            ('John Doe',
             'fox40',
             madeup@gmail.com,
             'tiago420!')
            )

conn.commit()

cur.close()
conn.close()