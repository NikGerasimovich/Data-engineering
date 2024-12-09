# Команды для работы с Apache Spark в PySpark

```python
# Основные команды для работы с RDD (Resilient Distributed Dataset)
sc.parallelize([elements])     # Создает RDD из списка данных.
sc.textFile("path")            # Загружает текстовый файл из указанного пути в RDD.
rdd.map(func)                  # Применяет функцию `func` к каждому элементу RDD.
rdd.flatMap(func)              # Применяет функцию `func` и разворачивает результат в одном уровне.
rdd.filter(func)               # Отбирает элементы, удовлетворяющие условию в функции `func`.
rdd.reduce(func)               # Аггрегирует элементы RDD с помощью функции `func`.
rdd.union(other_rdd)           # Объединяет два RDD в одно.
rdd.intersection(other_rdd)    # Возвращает пересечение двух RDD.
rdd.distinct()                 # Возвращает RDD с уникальными элементами.
rdd.cartesian(other_rdd)       # Возвращает декартово произведение двух RDD.

# Команды для работы с DataFrame
spark.read.csv("path")         # Читает CSV-файл в DataFrame.
spark.read.json("path")        # Читает JSON-файл в DataFrame.
df.select("column")            # Выбирает указанный столбец из DataFrame.
df.filter(df["column"] > 10)   # Фильтрует строки на основе условия.
df.groupBy("column").count()   # Группирует строки и подсчитывает их количество.
df.withColumn("new_column", expr)  # Добавляет новый столбец на основе выражения.
df.drop("column")              # Удаляет указанный столбец.
df.show()                      # Отображает первые строки DataFrame.
df.printSchema()               # Печатает схему DataFrame.

# Команды для работы с SQL
spark.sql("SELECT * FROM table")  # Выполняет SQL-запрос.
df.createOrReplaceTempView("table")  # Создает временное представление для DataFrame.
spark.catalog.listTables()       # Список доступных таблиц.

# Команды для работы с Spark Streaming
from pyspark.streaming import StreamingContext
ssc = StreamingContext(sc, batchDuration=1)  # Создает объект StreamingContext.
lines = ssc.socketTextStream("localhost", 9999)  # Создает DStream для входящих данных.
lines.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda x, y: x + y).pprint()
ssc.start()  # Запускает потоковую обработку.
ssc.awaitTermination()  # Ожидает завершения обработки.

# Команды для работы с MLlib
from pyspark.ml.classification import LogisticRegression
lr = LogisticRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)
model = lr.fit(training_data)  # Обучение модели на данных.

# Команды для работы с GraphX через PySpark (GraphFrames)
from graphframes import GraphFrame
vertices = spark.createDataFrame([(1, "A"), (2, "B")], ["id", "name"])
edges = spark.createDataFrame([(1, 2, "knows")], ["src", "dst", "relationship"])
g = GraphFrame(vertices, edges)
g.vertices.show()               # Показать вершины графа.
g.edges.show()                  # Показать ребра графа.
g.find("(a)-[e]->(b)").show()   # Поиск шаблонов в графе.
