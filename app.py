import fitness_database

db = fitness_database.QueryHandler()
db.getExerciseDataByDate('2023-02-01')
db.getWeightHistoryByUser('eduardoperetto')
db.getWeightGoalAndAverageWeightInYearByUser('eduardoperetto')