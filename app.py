import fitness_database

choose=11

while(choose!='0'):
    choose=input("""\nCONSULTAS: 
1-ID e nome das refeições onde houve consumo de acima de 10g de proteínas.
2-Nome de alimentos que possuem mais de 5g de gordura
3-Alimentos que não possuem Gordura
4-Alimentos que nao combinam
5-Nome de alimentos que possuem todos os nutrientes cadastrados no banco de dados
6-ID de receitas que possuem banana em sua composição
7-Alimentos consumidos no dia 26/01/2023
8-Registro de pesagem em order de data decrescente do usuário ESCOLHIDO
9-Consulta id, peso alvo e o peso médio do usuário ESCOLHIDO durante o período do ano de 2023
10-Retorna a lista de exercícios que foram realizados no dia ESCOLHIDO, juntamente com o tipo de exercício e o gasto calórico correspondente.

ESCOLHA UMA CONSULTA(insira '0' para sair): """)

    db = fitness_database.QueryHandler()

    if choose=='1':
        db.getOver10gProtein()
    elif choose=='2':
        db.getOver5gFat()
    elif choose=='3':
        db.getNoFat()
    elif choose=='4':
        db.getNoMatching()
    elif choose=='5':
        db.getWithAllNutrients()
    elif choose=='6':
        db.getBananaInComposition()
    elif choose=='7':
        db.getEatenIn26()
    elif choose=='8':
        date=input("Entre com a data desejada (YYY-MM-DD)'2023-02-01': ")
        db.getExerciseDataByDate(date)
    elif choose=='9':
        user=input("Entre com o usuario desejado: ")
        db.getWeightHistoryByUser(user)
    elif choose=='10':
        user=input("Entre com o usuario desejado: ")
        db.getWeightGoalAndAverageWeightInYearByUser(user)