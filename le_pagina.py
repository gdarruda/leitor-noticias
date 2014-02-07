from readability.readability import Document
from HTMLParser import HTMLParser
import urllib
import feedparser
import re
import banco_dados

def noticia_importada(link):

	count_noticia = banco_dados.conta_noticias(link)

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

	banco_dados.adiciona_noticia(link, titulo, texto_limpo, id_feed)

def le_feed(id_feed, link):

	#Recupera os links atualizados
	posts = feedparser.parse(link)

	#Processa cada site
	for post in posts.entries:
		le_site(post.link, post.title, id_feed)

def processa_feeds():

	cursor_feeds = banco_dados.cursor_feeds()

	#Para cada feed Atom, processa os links retornados
	for (id_feed, link) in cursor_feeds:
		le_feed(id_feed, link)

	banco_dados.fecha_conexao()

processa_feeds()