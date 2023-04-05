import psycopg2

def setupDBConnection():
    #configurações
    host = 'localhost'
    dbname = 'FITNESS'
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

    def getOver10gProtein(self):
        print("\n(idRefeicao, Refeicao)".center(20))
        self.cursor.execute("""select idRefeicao, Refeicao.nome from 
                            Refeicao natural join ComposicaoRefeicao 
                            join Alimento on(ComposicaoRefeicao.idAlimento=Alimento.idAlimento)
                            join ComposicaoAlimentar on(ComposicaoAlimentar.idAlimento=Alimento.idAlimento)
                            join Nutriente using(idNutriente)
                            group by idRefeicao
                            having sum(case when Nutriente.nome = 'Proteina' then quantidade end)>10;""")
        printQueryRows(self.cursor.fetchall())

    
    def getOver5gFat(self):
        print("\n(Nome)".center(20))
        self.cursor.execute("""select Alimento.nome 
                            from Alimento join ComposicaoAlimentar on(ComposicaoAlimentar.idAlimento=Alimento.idAlimento)
                            join Nutriente using(idNutriente)
                            group by Alimento.nome
                            having  sum(case when Nutriente.nome = 'Gordura' then quantidade end)>5;""")
        printQueryRows(self.cursor.fetchall())

    def getNoFat(self):
        print("\n(idAlimento, Nome)".center(20))
        self.cursor.execute("""SELECT a.*
                            FROM Alimento a
                            WHERE NOT EXISTS (
                            SELECT *
                            FROM ComposicaoAlimentar c
                            JOIN Nutriente n ON c.idNutriente = n.idNutriente
                            WHERE c.idAlimento = a.idAlimento AND n.nome = 'Gordura');""")
        printQueryRows(self.cursor.fetchall())

    def getNoMatching(self):
        print("\n(Nome)".center(20))
        self.cursor.execute("""select nome
                            from Alimento ALI
                            where idAlimento <> 2 and
                            not exists (select nome
                            from ComposicaoRefeicao
                            where idAlimento = 2 and
                            idAlimento in
                            (select distinct idAlimento
                            from ComposicaoRefeicao
                            where idAlimento = ALI.idAlimento));""")
        printQueryRows(self.cursor.fetchall())

    def getWithAllNutrients(self):
        print("\n(Nome)".center(20))
        self.cursor.execute("""SELECT nome
                            FROM Alimento A
                            WHERE NOT EXISTS (SELECT idNutriente
                            FROM Nutriente N
                            WHERE NOT EXISTS (SELECT idNutriente
                                            FROM ComposicaoAlimentar C
                                            WHERE C.idNutriente = N.idNutriente
                                            AND C.idAlimento = A.idAlimento));""")
        printQueryRows(self.cursor.fetchall())

    def getBananaInComposition(self):
        print("\n(idReceita)".center(20))
        self.cursor.execute("""select idReceita 
                            from Receita natural join Ingrediente join Alimento a using(idAlimento)
                            where a.nome='Banana';""")
        printQueryRows(self.cursor.fetchall())

    def getEatenIn26(self):
        print("\n(Nome)".center(20))
        self.cursor.execute("""select Alimento.nome 
                            from Refeicao 
                            natural join CronogramaAlimentar 
                            natural join Diario 
                            join ComposicaoRefeicao using(idRefeicao) 
                            join Alimento using (idAlimento)
                            where data='2023-01-26';""")
        printQueryRows(self.cursor.fetchall())

    def getWeightHistoryByUser(self, user):
        print(" - Histórico de pesagens para o usuário", user)
        self.cursor.execute("""
            SELECT  Peso.valor, Peso.data
            FROM 
                Usuario u
                JOIN Pesagem ON Pesagem.idUsuario = u.id
                JOIN Peso ON Pesagem.idPeso = Peso.idPeso
            WHERE u.nome = %s
            ORDER BY Peso.data DESC;
        """, (user, ))
        print("(valor, data)")
        printQueryRows(self.cursor.fetchall())

    def getExerciseDataByDate(self, date):
        print(" - Dados de exercícios para o dia", date)
        self.cursor.execute("""
            SELECT e.idExercicio, e.duracao, t.nome as tipo_exercicio, t.gastoCalorico * e.duracao / 60 as gasto_calorico
            FROM 
                Exercicio e 
                JOIN TipoExercicio t ON e.idTipoExercicio = t.idTipoExercicio 
                JOIN Treino tr ON e.idExercicio = tr.idExercicio 
                JOIN Diario d ON tr.idDiario = d.idDiario 
            WHERE d.data = %s;
        """, (date, ))
        print("(idExercicio, duracao, tipo_exercicio, gasto_calorico)")
        printQueryRows(self.cursor.fetchall())

    def getWeightGoalAndAverageWeightInYearByUser(self, user):
        print(" - Peso alvo e peso médio para o usuário", user, "durante o ano atual")
        self.cursor.execute("""
            SELECT Usuario.id, Objetivo.pesoAlvo, AVG(Peso.valor) as pesoMedio
            FROM 
                Usuario
                JOIN Objetivo ON Usuario.idObjetivo = Objetivo.idObjetivo
                JOIN Pesagem ON Usuario.id = Pesagem.idUsuario
                JOIN Peso ON Pesagem.idPeso = Peso.idPeso
            WHERE Usuario.nome = %s 
            AND date_part('year', Peso.data) = date_part('year', CURRENT_DATE)
            GROUP BY Usuario.id, Objetivo.pesoAlvo;
        """, (user, ))
        print("(idUsuario, pesoAlvo, pesoMedio)")
        printQueryRows(self.cursor.fetchall())
