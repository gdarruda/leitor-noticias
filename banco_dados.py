import mysql.connector
import time
from datetime import datetime, date, timedelta

#Conexao com banco de dados local
conexao = mysql.connector.connect(user='garruda', password='garruda', host='127.0.0.1', database='noticias')

def conta_noticias(link):
	
	count_noticia = conexao.cursor()

	query_noticia = ('select count(*) from noticias where link =  %s')
	count_noticia.execute(query_noticia, (link,))

	return count_noticia

def adiciona_noticia(link, titulo, texto_limpo, id_feed):

	cursor_noticia = conexao.cursor()

	add_noticia = ('insert into noticias (link, titulo, corpo, data_importacao, id_feed) values (%s, %s, %s, %s, %s)')
	data_noticia = (link, titulo, texto_limpo, date(int(time.strftime('%y')), int(time.strftime('%m')), int(time.strftime('%d'))),id_feed)
	cursor_noticia.execute(add_noticia, data_noticia)

	conexao.commit()

def cursor_feeds():

	cursor_feeds = conexao.cursor()

	#Procura os feeds armazenados no banco de dados
	query_feeds = ('select * from feeds')
	cursor_feeds.execute(query_feeds)

	return cursor_feeds

def fecha_conexao():

	conexao.close()