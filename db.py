import sqlite3

# sqlite db
conn = sqlite3.connect('server.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS log
                 (datetime, command, device, response)''')
# Create table
c.execute('''CREATE TABLE IF NOT EXISTS status
                 (id integer PRIMARY KEY, running integer)''')
    
c.execute('''INSERT INTO status(id, running)
                 VALUES(0, 0)''')
# Save (commit) the changes
conn.commit()
    
conn.close()