import traceback
import feedparser
import URL
from GestorNoticias import GestorNoticias
from Alchemy import Alchemy

class LeitorFeeds(object):
	'Chama API para leitura de feeds Atom RSS'

	def __init__(self, bd, log):
		self.bd  = bd
		self.log = log

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

		#Classe para insercao de noticias
		gn = GestorNoticias(self.bd,api)

		#Para cada feed Atom, processa os links retornados
		for (id_feed, link) in cursor_feeds:

			try:
				#Recupera as ultimas noticias do feed
				posts = self.le_feed(link)

				#Para cada post, limpa HTML e adiciona no banco de dados
				for post in posts.entries:

					try:
						#Verifica se eh necessario importar a noticia
						if URL.url_importada(post.link, self.bd):
							continue

						#Chama o AlchemyAPI para limpar o texto
						texto_processado = api.processa_html(post.link)

						#Adiciona noticia ao banco de dados
						gn.adiciona_noticia(post.link, post.title, texto_processado, None, id_feed, None)

					except:
						self.log.registra_erro('Erro ao extrair informacoes do link' + post.link + ' do feed ' + str(id_feed) + ':' + traceback.format_exc())

			except:
				self.log.registra_erro('Erro ao processar feed' + str(id_feed) + ': ' + traceback.format_exc())
