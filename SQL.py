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
choose=20

while(choose!='0'):
    choose=input("""
                    CONSULTAS: 

                    1-ID e nome das refeições onde houve consumo de acima de 10g de proteínas.
                    2-Nome de alimentos que possuem mais de 5g de gordura
                    3-Alimentos que não possuem Gordura
                    4-Alimentos que nao combinam
                    5-Nome de alimentos que possuem todos os nutrientes cadastrados no banco de dados
                    6-ID de receitas que possuem banana em sua composição
                    7-Alimentos consumidos no dia 26/01/2023
                    8-Registro de pesagem em order de data decrescente do usuário com nome de 'eduardoperetto'
                    9-Consulta id, peso alvo e o peso médio do usuário fernandosulzbach durante o período do ano de 2023
                    10-Retorna a lista de exercícios que foram realizados no dia 27/01/2023, juntamente com o tipo de exercício e o gasto calórico correspondente.

                    ESCOLHA UMA CONSULTA(insira '0' para sair): """)

    if choose=='1':
            
        cursor = conn.cursor() 
        # Fetch all rows from table
        cursor.execute("""select idRefeicao, Refeicao.nome from 
                            Refeicao natural join ComposicaoRefeicao 
                            join Alimento on(ComposicaoRefeicao.idAlimento=Alimento.idAlimento)
                            join ComposicaoAlimentar on(ComposicaoAlimentar.idAlimento=Alimento.idAlimento)
                            join Nutriente using(idNutriente)
                            group by idRefeicao
                            having sum(case when Nutriente.nome = 'Proteina' then quantidade end)>10;""")
        rows = cursor.fetchall()
        print("\n--idRefeicao--|--Refeicao--".center(20))
        # Print all rows
        for row in rows:
            print(" %s | %s ".center(20) %(str(row[0]), str(row[1])))

    elif choose=='2':

        cursor = conn.cursor() 
        # Fetch all rows from table
        cursor.execute("""select Alimento.nome 
                            from Alimento join ComposicaoAlimentar on(ComposicaoAlimentar.idAlimento=Alimento.idAlimento)
                            join Nutriente using(idNutriente)
                            group by Alimento.nome
                            having  sum(case when Nutriente.nome = 'Gordura' then quantidade end)>5;""")
        rows = cursor.fetchall()
        print("\n--Alimento--")
        # Print all rows
        for row in rows:
            print(" %s " %(str(row[0])))

    elif choose=='3':
            
        cursor = conn.cursor() 
        # Fetch all rows from table
        cursor.execute("""SELECT a.*
                        FROM Alimento a
                        WHERE NOT EXISTS (
                        SELECT *
                        FROM ComposicaoAlimentar c
                        JOIN Nutriente n ON c.idNutriente = n.idNutriente
                        WHERE c.idAlimento = a.idAlimento AND n.nome = 'Gordura');""")
        rows = cursor.fetchall()
        print("\n--idAlimento--|--Nome--".center(20))
        # Print all rows
        for row in rows:
            print(" %s | %s ".center(20) %(str(row[0]), str(row[1])))

    elif choose=='4':
            
        cursor = conn.cursor() 
        # Fetch all rows from table
        cursor.execute("""select nome
                            from Alimento ALI
                            where idAlimento <> 2 and
                            not exists (select nome
                            from ComposicaoRefeicao
                            where idAlimento = 2 and
                            idAlimento in
                            (select distinct idAlimento
                            from ComposicaoRefeicao
                            where idAlimento = ALI.idAlimento));""")
        rows = cursor.fetchall()
        print("\n--Nome--".center(20))
        # Print all rows
        for row in rows:
            print(" %s ".center(20) %(str(row[0])))

    elif choose=='5':
            
        cursor = conn.cursor() 
        # Fetch all rows from table
        cursor.execute("""SELECT nome
                            FROM Alimento A
                            WHERE NOT EXISTS (SELECT idNutriente
                            FROM Nutriente N
                            WHERE NOT EXISTS (SELECT idNutriente
                                            FROM ComposicaoAlimentar C
                                            WHERE C.idNutriente = N.idNutriente
                                            AND C.idAlimento = A.idAlimento));""")
        rows = cursor.fetchall()
        print("\n--Nome--".center(20))
        # Print all rows
        for row in rows:
            print(" %s ".center(20) %(str(row[0])))


    elif choose=='6':
            
        cursor = conn.cursor() 
        # Fetch all rows from table
        cursor.execute("""select idReceita 
                            from Receita natural join Ingrediente join Alimento a using(idAlimento)
                            where a.nome='Banana';""")
        rows = cursor.fetchall()
        print("\n--idReceita--".center(20))
        # Print all rows
        for row in rows:
            print(" %s ".center(20) %(str(row[0])))


    elif choose=='7':
            
        cursor = conn.cursor() 
        # Fetch all rows from table
        cursor.execute("""select Alimento.nome 
                            from Refeicao 
                            natural join CronogramaAlimentar 
                            natural join Diario 
                            join ComposicaoRefeicao using(idRefeicao) 
                            join Alimento using (idAlimento)
                            where data='2023-01-26';""")
        rows = cursor.fetchall()
        print("\n--Nome--".center(20))
        # Print all rows
        for row in rows:
            print(" %s ".center(20) %(str(row[0])))


    elif choose=='8':
            
        cursor = conn.cursor() 
        # Fetch all rows from table
        cursor.execute("""SELECT  UsuarioeObjetivo.nome,Peso.valor,(Peso.data)
                            FROM UsuarioeObjetivo
                            JOIN Pesagem ON UsuarioeObjetivo.id = Pesagem.idUsuario
                            JOIN Peso ON Pesagem.idPeso = Peso.idPeso
                            WHERE UsuarioeObjetivo.nome = 'eduardoperetto'
                            ORDER BY Peso.data DESC;""")
        rows = cursor.fetchall()
        print("\n--Nome--|--Peso--|--Data--".center(20))
        # Print all rows
        for row in rows:
            print(" %s | %s | %s ".center(20) %(str(row[0]), str(row[1]), str(row[2])))

    elif choose=='9':
            
        cursor = conn.cursor() 
        # Fetch all rows from table
        cursor.execute("""select id,avg(valor),pesoAlvo
                            from UsuarioeObjetivo u
                            join Pesagem on (u.id = Pesagem.idUsuario)
                            join Peso using (idpeso)
                            where data >'2023-01-01' and data <'2023-12-31'
                            and nome='eduardoperetto'
                            GROUP BY u.id,pesoAlvo;""")
        rows = cursor.fetchall()
        print("\n--id--|--Media--|--Alvo--".center(20))
        # Print all rows
        for row in rows:
            print(" %s | %s | %s ".center(20) %(str(row[0]), str(row[1]), str(row[2])))

    elif choose=='10':
            
        cursor = conn.cursor() 
        # Fetch all rows from table
        cursor.execute("""SELECT 
                            e.idExercicio,
                            e.duracao,
                            t.nome as tipo_exercicio,
                            t.gastoCalorico * e.duracao as gasto_calorico
                            FROM Exercicio e 
                            JOIN TipoExercicio t ON e.idTipoExercicio = t.idTipoExercicio 
                            JOIN Treino tr ON e.idExercicio = tr.idExercicio 
                            JOIN Diario d ON tr.idDiario = d.idDiario 
                            WHERE d.data = '2023-01-27';""")
        rows = cursor.fetchall()
        print("\n--id--|--Duracao--|--Nome--|--Calorias Queimadas--".center(20))
        # Print all rows
        for row in rows:
            print(" %s | %s | %s | %s ".center(20) %(str(row[0]), str(row[1]), str(row[2]), str(row[3])))
