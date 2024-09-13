from mysql.connector import connect, Error
import logging
myhost="172.26.0.2"
logging.basicConfig(filename='/var/log/secsaas/mysql.log',
                    filemode='a',
                    format="%(asctime)s %(levelname)s pid:%(process)d "\
                           "%(funcName)s (%(filename)s:%(lineno)d) "\
                           "%(message)s",
                    level=logging.DEBUG)

def execute_insert_sql(sql_command,val):
  try:
    with connect(
      host=myhost,
      database="secsaas",
      user="root",
      password="root",
      port="3306",
      connection_timeout=60
    ) as connection:
      cursor=connection.cursor()
      cursor.execute(sql_command, val)
      connection.commit()
  except Error as e:
    logging.error(e)
    raise

def execute_select_sql(sql_command,val):
  try:
    with connect(
      host=myhost,
      database="secsaas",
      user="root",
      password="root",
      port="3306",
      connection_timeout=60
    ) as connection:
      logging.info("Sql qqq %s %s",sql_command, val)
      cursor=connection.cursor()
      cursor.execute(sql_command, val)
      row=cursor.fetchone()
  except Error as e:
    logging.error(e)
    raise

  return row




