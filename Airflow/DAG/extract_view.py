from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime 
import func as etf

email = Variable.get("EMAIL")
legal_month = Variable.get("PARTY_MONTH")
physical_month = Variable.get("PHYSICAL_MONTH")
legal_year = Variable.get("LEGAL_YEAR")
physical_year = Variable.get("PHYSICAL_YEAR")
v_schedule_temp = Variable.get("DAG_SCHEDULE")
v_schedule = ""

if (v_schedule_temp == "None"):
    v_schedule = None
else:
    v_schedule = v_schedule_temp

email_on_error_str = email 

if email_on_error_str and isinstance(email_on_error_str, str):
    email_on_error_list = [em.strip() for em in email_on_error_str.split(';') if em]
else:
    email_on_error_list = []

default_args = {
    'email_on_failure': True,
    'email': email_on_error_list
}
  

with DAG(dag_id="extract", start_date=datetime(2024, 8, 19), schedule=v_schedule,
         tags=["EXT"], catchup=False, max_active_runs=1, 
         params={"LEGAL_MONTH": legal_month,"LEGAL_YEAR": legal_year, "PHYSIC_MONTH": physical_month, "PHYSICAL_YEAR": physical_year}, default_args=default_args) as dag:
 

    
    replace_list = [
        ("&month_l", "{{params.LEGAL_MONTH}}"),
        ("&year_l", "{{params.LEGAL_YEAR}}"),
        ("&month_p", "{{params.PHYSIC_MONTH}}"),
        ("&year_p", "{{params.PHYSICAL_YEAR}}")
        ]

    start = EmptyOperator(task_id="start")
 
    
    View_To_Table = PythonOperator(     
        task_id=f"view_to_table",
        pool="test_pool",
        python_callable=etf.execute_sql_script,     
        op_kwargs={'sql_file': r'/path/to/view_to_table.sql',
                    'replace_list': replace_list}
    ) 
    
    end = EmptyOperator(task_id='end')
    
    start >> View_To_Table >> end
