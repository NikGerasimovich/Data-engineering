from airflow.providers.exasol.hooks.exasol import ExasolHook
from airflow.providers.exasol.operators.exasol import ExasolOperator
from airflow.models import Variable
import sqlparse
import openpyxl
from pyexasol import ExaQueryError


def execute_sql_script(exasol_conn_id='exasol7', **kwargs):
    sql_file = kwargs['sql_file']

    if 'replace_list' in kwargs:
        replace_list = kwargs['replace_list']
    else:
        replace_list = []

    if isinstance(sql_file, str):
        sql_file = [sql_file]

    sql = []

    for f_name in sql_file:
        with open(f_name, encoding='utf-8') as f:
            raw = f.read()
            for rp in replace_list:
                if rp[0] != rp[1]:
                    raw = raw.replace(rp[0], rp[1])

            statements = sqlparse.split(raw)

        for query in statements:
            query_new = sqlparse.format(query, strip_comments=True)
            if query_new:
                sql.append(query_new)

# формируем имя подключения
default_conn_name = exasol_conn_id
exasol_conn_id = kwargs.get("conn_name", default_conn_name)
#
exh = ExasolHook(exasol_conn_id)
with exh.get_conn() as exc:
    exc.set_autocommit(False)
    
    for query in sql:
        print(query)
        exc.execute(query)
    
    exc.commit()