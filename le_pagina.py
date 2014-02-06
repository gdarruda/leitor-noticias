from readability.readability import Document
from HTMLParser import HTMLParser
from datetime import datetime, date, timedelta
import urllib
import feedparser
import re
import mysql.connector
import time

conexao = mysql.connector.connect(user='garruda', password='garruda', host='127.0.0.1', database='noticias')

def noticia_importada(link):

	count_noticia = conexao.cursor()

	query_noticia = ('select count(*) from noticias where link =  %s')
	count_noticia.execute(query_noticia, (link,))

	return count_noticia.fetchone()[0] > 0

def le_site(link, titulo, id_feed):

	#Verifica se a noticia foi importada
	if noticia_importada(link):
		return

	#Abre uma URL e recupera o HTML
	url = urllib.urlopen(link)
	html = url.read()

	#Limpa o HTML com a API do Readability
	html_limpo = Document(html).summary()

	#Remove as quebras de linha do HTML
	html_limpo = html_limpo.replace('\n', '')
	paragrafos = html_limpo.split('<p>')

	texto_limpo = ''

	#Remove todas as TAGs
	for paragrafo in paragrafos:
		texto_limpo =  texto_limpo + re.sub('<.*?>', '', paragrafo)

	cursor_noticia = conexao.cursor()

	#Insere na tabela
	add_noticia = ('insert into noticias (link, titulo, corpo, data_importacao, id_feed) values (%s, %s, %s, %s, %s)')
	data_noticia = (link, titulo, texto_limpo, date(int(time.strftime('%y')), int(time.strftime('%m')), int(time.strftime('%d'))),id_feed)
	cursor_noticia.execute(add_noticia, data_noticia)

	#Fecha transacao
	conexao.commit()

def le_feed(id_feed, link):

	#Recupera os links atualizados
	posts = feedparser.parse(link)

	#Processa cada site
	for post in posts.entries:
		le_site(post.link, post.title, id_feed)

def processa_feeds():

	cursor_feeds = conexao.cursor()

	#Procura os feeds armazenados no banco de dados
	query_feeds = ('select * from feeds')
	cursor_feeds.execute(query_feeds)

	#Para cada feed Atom, processa os links retornados
	for (id_feed, link) in cursor_feeds:
		le_feed(id_feed, link)

	conexao.close()

processa_feeds()