import feedparser
import urllib
import URL

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

		#Para cada feed Atom, processa os links retornados
		for (id_feed, link, processador_html) in cursor_feeds:

			#Recupera o catalogo de links RSS
			posts = self.le_feed(link)

			#Para cada post, limpa HTML e adiciona no banco de dados
			for post in posts.entries:

				texto_limpo = URL.le_site(post.link, processador_html, self.bd)

				#Adiciona noticia no Banco de Dados
				self.bd.adiciona_noticia(link, post.title, texto_limpo, id_feed, None)