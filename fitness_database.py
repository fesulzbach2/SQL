import psycopg2

def setupDBConnection():
        #configurações
        host = 'localhost'
        dbname = 'postgres'
        user = 'postgres'
        password = 'admin'
        sslmode = 'allow'

        #string de conexão
        conn_string = 'host={0} user={1} dbname={2} password={3} sslmode={4}'.format(host,user,dbname,password,sslmode)
        conn = psycopg2.connect(conn_string)
        print('Database succesfully connected')
        return conn.cursor()

def printQueryRows(rows):
        for row in rows:
            rowDescription = "("
            for attribute in row:
                if attribute != None:
                    rowDescription += str(attribute) + ", "
            rowDescription += ")"
            print(rowDescription)

class QueryHandler:
    def __init__(self):
        self.cursor = setupDBConnection()

    def getExerciseDataByDate(self, date):
        self.cursor.execute("""
            SELECT 
            e.idExercicio,
            e.duracao,
            t.nome as tipo_exercicio,
            t.gastoCalorico * e.duracao / 60 as gasto_calorico
            FROM 
            Exercicio e 
            JOIN TipoExercicio t ON e.idTipoExercicio = t.idTipoExercicio 
            JOIN Treino tr ON e.idExercicio = tr.idExercicio 
            JOIN Diario d ON tr.idDiario = d.idDiario 
            WHERE 
            d.data = %s;
        """, (date, ))
        printQueryRows(self.cursor.fetchall())

    def getWeightHistoryByUser(self, user):
        self.cursor.execute("""
            SELECT  Peso.valor, Peso.data
            FROM 
                Usuario u
                JOIN Pesagem ON Pesagem.idUsuario = u.id
                JOIN Peso ON Pesagem.idPeso = Peso.idPeso
            WHERE u.nome = %s
            ORDER BY Peso.data DESC;
        """, (user, ))
        printQueryRows(self.cursor.fetchall())