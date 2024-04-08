from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.db import connection
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import cx_Oracle
from django.conf import settings

class SQLQueryAPIView(View):
 
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)  
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            sql_query = data.get('sql_query')
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'})
 
        if not sql_query:
            return JsonResponse({'message': 'SQL query is required'})
 
        # db_user = "apps"
        # db_password = "testapps"
        # db_host = "secure.focusrtech.com:1581"
        # db_name = "TEST"
        # oracle_db_uri = f"{db_user}/{db_password}@{db_host}/{db_name}"
 
        try:
            oracle_db_config = settings.DATABASES['oracledb']
            with cx_Oracle.connect(
                    user=oracle_db_config['USER'],
                    password=oracle_db_config['PASSWORD'],
                    dsn=f"{oracle_db_config['HOST']}:{oracle_db_config['PORT']}/{oracle_db_config['NAME']}",
                    encoding='UTF-8'
                ) as connection:
                cursor = connection.cursor()
                cursor.execute(sql_query)
                columns = [col[0] for col in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
 
            return JsonResponse({'data': results})
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            return JsonResponse({'message': f'Error executing SQL query: {error.message}'})
