import urllib
import re
from readability.readability import Document
import processa_estadao
from HTMLParser import HTMLParser

def abre_url(link):

	url = urllib.urlopen(link)
	html = url.read()

	return html

def limpa_html(html):

	html_limpo = Document(html).summary()
	return html_limpo

def html_texto(html):


	#Seleciona apenas o HTML referente ao texto
	html = limpa_html(html)

	#Transforma em Unicode
	html = html.encode('utf-8')

	#Remove as quebras de linha do HTML
	html = html.replace('\n', '')

	paragrafos = html.split('<p>')

	texto_limpo = ''

	#Remove todas as TAGs
	for paragrafo in paragrafos:
		texto_limpo =  texto_limpo + re.sub('<.*?>', '', paragrafo)

	return texto_limpo