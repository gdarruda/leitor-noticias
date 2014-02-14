 # coding=utf-8

import re
from readability.readability import Document

class ProcessadorHTML:
	'Classe para transformacao de paginas HTML em texto limpo'

	def __init__(self, html):
		self.html = html

	#Utiliza a API do readability para recuperar apenas a parte principal do texto
	def utiliza_readability(self):

		self.html = Document(self.html).summary()

	#Utiliza a API do readability para recuperar apenas a parte principal do texto
	def decodifica(self, codificacao):

		#Codifica o texto em UTF8 
		self.html = self.html.decode(codificacao).encode('utf-8')

	#Funcao basica para processar uma pagina HTML de noticia
	def processa_html(self):

		self.decodifica('utf-8')

		self.utiliza_readability()

		#Remove as quebras de linha do HTML
		self.html = self.html.replace('\n', '')

		#Separa o texto em paragrafos atraves da TAG "<p>"
		paragrafos = self.html.split('<p>')

		#Com o texto limpo
		texto_limpo = ''

		#Remove todas as TAGs
		for paragrafo in paragrafos:
			texto_limpo =  texto_limpo + re.sub('<.*?>', '', paragrafo)

		return texto_limpo

class ProcessadorEstadao(ProcessadorHTML):
	'Classe para transformacao de paginas do Estadao em texto limpo'

	def processa_html(self):

		self.decodifica('utf-8')

		self.utiliza_readability()

		#Apaga o caracter '&#13;'
		self.html = self.html.replace('&#13;', '')

		#Remove as quebras de linha do HTML
		self.html = self.html.replace('\n', '')

		#Separa o texto em paragrafos atraves da TAG "<p>"
		paragrafos = self.html.split('<p>')
		
		#Com o texto limpo
		texto_limpo = ''

		#Remove todas as TAGs
		for paragrafo in paragrafos:

			#Verifica se o paragrafo eh referente aos links relacionados presentes no meio da materia
			if paragrafo.find('Veja também:'.decode('utf-8')) > -1:
				continue

			texto_limpo =  texto_limpo + re.sub('<.*?>', '', paragrafo)

		return texto_limpo

class ProcessadorFolha(ProcessadorHTML):
	'Classe para transformacao de paginas da Folha em texto limpo'

	def processa_html(self):

		self.decodifica('cp1252')

		self.utiliza_readability()

		#Apaga o caracter '&#13;'
		self.html = self.html.replace('&#13;', '')

		#Remove as quebras de linha do HTML
		self.html = self.html.replace('\n', '')

		#Separa o texto em paragrafos atraves da TAG "<p>"
		paragrafos = self.html.split('<p>')
		
		#Com o texto limpo
		texto_limpo = ''

		#Remove todas as TAGs
		for paragrafo in paragrafos:

			texto_limpo =  texto_limpo + re.sub('<.*?>', '', paragrafo)

		return texto_limpo