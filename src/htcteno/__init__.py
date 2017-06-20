# 建立mysql连接，使用sqlalchemy
'''from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utils.static_keys import StaticKeys
from utils.parse_configure import parse_mysql_configure

mysql_conf = parse_mysql_configure()
user = mysql_conf[StaticKeys.MYSQL_USER]
password = mysql_conf[StaticKeys.MYSQL_PASSWORD]
host = mysql_conf[StaticKeys.MYSQL_HOST]
port = mysql_conf[StaticKeys.MYSQL_PORT]
database = mysql_conf[StaticKeys.MYSQL_DATABASE]

connector = "mysql+mysqlconnector://%s:%s@%s:%s/%s" %(user, password, host, port, database)
engine = create_engine(connector)
DBsession = sessionmaker(bind = engine)
session = DBsession()'''