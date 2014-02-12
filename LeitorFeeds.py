import feedparser
import urllib

class LeitorFeeds(object):
	'Chama API para leitura de feeds Atom RSS'

	def __init__(self, link):
		
		self.link = link
	
	@staticmethod
	def abre_url(link):

		#Abre URL e carrega o HTML em uma String
		url = urllib.urlopen(link)
		html = url.read()

		return html

	def le_feed(self):

		#Recupera os links atualizados
		posts = feedparser.parse(self.link)

		#Retorna a colecao de posts
		return posts