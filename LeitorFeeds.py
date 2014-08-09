import feedparser
import URL
from Alchemy import Alchemy

class LeitorFeeds(object):
	'Chama API para leitura de feeds Atom RSS'

	def __init__(self, bd):
		self.bd = bd

	def le_feed(self, link):

		#Recupera os links atualizados
		posts = feedparser.parse(link)

		#Retorna a colecao de posts
		return posts

	def processa_feeds(self):

		#Procura os feeds ativos no banco de dados
		cursor_feeds = self.bd.procura_feeds()

		#API do Alchemy
		api = Alchemy()

		#Para cada feed Atom, processa os links retornados
		for (id_feed, link) in cursor_feeds:

			#Recupera o catalogo de links RSS
			posts = self.le_feed(link)

			#Para cada post, limpa HTML e adiciona no banco de dados
			for post in posts.entries:

				#Verifica se eh necessario importar a noticia
				if URL.url_importada(post.link, self.bd):
					continue

				#Chama o AlchemyAPI para limpar o texto
				texto_processado = api.processa_html(post.link)

				#Adiciona noticia no Banco de Dados
				self.bd.adiciona_noticia(link, post.title, texto_processado, id_feed, None)
