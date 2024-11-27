from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
import psycopg2
from airflow.models import Variable

# Функция для извлечения дат из базы данных
def extract_dates_from_db(**kwargs):
    # Получение параметров подключения из Airflow Variables
    db_name = Variable.get("db_name")
    db_host = Variable.get("db_host")
    db_port = Variable.get("db_port")
    db_user = Variable.get("db_user")  # Имя пользователя может быть зашито в конфигурации Airflow
    db_password = Variable.get("db_password")  # Пароль также можно хранить в Airflow
    
    # Подключение к базе данных
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    cursor = conn.cursor()

    # SQL запрос для извлечения двух последних дат
    cursor.execute("""
        SELECT DISTINCT DATE FROM TABLE_123 ORDER BY DATE DESC LIMIT 2;
    """)
    result = cursor.fetchall()

    # Проверяем, что данные найдены
    if len(result) < 2:
        raise ValueError("Недостаточно данных для извлечения двух последних дат.")

    # Извлечение дат
    last_date = result[0][0]
    second_last_date = result[1][0]

    # Передача дат в XCom
    kwargs['ti'].xcom_push(key='last_date', value=last_date)
    kwargs['ti'].xcom_push(key='second_last_date', value=second_last_date)

    cursor.close()
    conn.close()

# Параметры DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Путь к SQL-скрипту
SQL_SCRIPT_PATH = "/path/to/Date_compile.sql"

# Создание DAG
with DAG(
    'unified_dag_with_variables',
    default_args=default_args,
    description='DAG',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:

    # Задача 1: Извлечение дат из базы данных
    extract_dates_task = PythonOperator(
        task_id='extract_dates_from_db',
        python_callable=extract_dates_from_db,
        provide_context=True
    )

    # Задача 2: Выполнение SQL-скрипта с использованием извлечённых дат
    execute_sql_task = PostgresOperator(
        task_id='execute_sql_with_dates',
        postgres_conn_id='your_postgres_conn_id',  
        sql=SQL_SCRIPT_PATH,
        parameters={
            '@start_date': "{{ task_instance.xcom_pull(task_ids='extract_dates_from_db', key='second_last_date') }}",
            '@end_date': "{{ task_instance.xcom_pull(task_ids='extract_dates_from_db', key='last_date') }}"
        },
        autocommit=True
    )

    # Устанавливаем порядок выполнения
    extract_dates_task >> execute_sql_task
