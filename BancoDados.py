import mysql.connector
import time
from datetime import datetime, date, timedelta

class BancoDados:
	'Classe abstrata para manipulacao de banco de dados'

#Conta noticias importadas
def contaNoticias(self, link):
	raise NotImplementedError

#Adiciona uma noticia ao banco de dados
def adiciona_noticia(self, link, titulo, texto_limpo, id_feed):
	raise NotImplementedError

#Procura os feeds ativos 
def procura_feeds(self):
	raise NotImplementedError

#Procura os perfis de Twitter ativos
def procura_perfis(self):
	raise NotImplementedError

#Fecha a conexaoo com o banco
def fecha_conexao(self):
	raise NotImplementedError


class BancoMySQL(BancoDados):
	'Classe para manipulacao de banco de dados em MySQL'

	def __init__(self, usuario, senha, host, banco):
		self.conexao =  mysql.connector.connect(user=usuario, password=senha, host=host, database=banco, buffered=True)

	def conta_noticias(self, link):
		
		contador_noticia = self.conexao.cursor()

		query_noticia = ('select count(*) from noticias where link =  %s')
		contador_noticia.execute(query_noticia, (link,))

		return contador_noticia

	def adiciona_noticia(self, link, titulo, texto_limpo, id_feed, id_perfil):

		cursor_noticia = self.conexao.cursor()

		insert_noticia = ('insert into noticias (link, titulo, corpo, data_importacao, id_feed, id_perfil) values (%s, %s, %s, %s, %s, %s)')
		dados_noticia = (link, titulo, texto_limpo, date(int(time.strftime('%y')), int(time.strftime('%m')), int(time.strftime('%d'))),id_feed, id_perfil)
	
		cursor_noticia.execute(insert_noticia, dados_noticia)

		self.conexao.commit()

	def procura_feeds(self):
		
		cursor_feeds = self.conexao.cursor()

		query_feeds = ('select id_feed, link , processador_html from feeds where ind_ativo = \'S\'')
		cursor_feeds.execute(query_feeds)

		return cursor_feeds

	def procura_perfis(self):
		
		cursor_tweets = self.conexao.cursor()

		query_tweets = ('select id_perfil, nome , processador_html from perfis_twitter where ind_ativo = \'S\'')
		cursor_tweets.execute(query_tweets)

		return cursor_tweets

	def fecha_conexao(self):

		self.conexao.close()