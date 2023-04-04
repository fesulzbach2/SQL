import psycopg2

#configurações
host = 'localhost'
dbname = 'FITNESS'
user = 'postgres'
password = 'admin'
sslmode = 'allow'

#string de conexão
conn_string = 'host={0} user={1} dbname={2} password={3} sslmode={4}'.format(host,user,dbname,password,sslmode)
print(conn_string)

conn = psycopg2.connect(conn_string)

print('conectado')

cursor = conn.cursor()


# Fetch all rows from table

cursor.execute("SELECT * FROM Alimento;")
rows = cursor.fetchall()

# Print all rows

for row in rows:
    print("Data row = (%s, %s)" %(str(row[0]), str(row[1])))