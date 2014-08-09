import twitter
import URL
from Alchemy import Alchemy

class LeitorTwitter(object):
	'Processa os posts do Twitter'

	def __init__(self, bd):
		self.api = twitter.Api('ou1umOYzfOprMk5YPaZtqG6HG','SdUsK8IAKCITSRvdmVYz0y4uQpCPzAsLJ9rQAim6fek1RGoDDc','2356629355-I35FpdV7hoBmxcZUy4OCscmmwejDrlsX7JL1OPM','2mntySesSInFr6ApQjQOcn1bTfctYKFHVjMFq7kevNtgp')
		self.bd = bd

	def le_tweets(self, nome):

		tweets = self.api.GetUserTimeline(screen_name=nome)

		return tweets

	def processa_twitter(self):

		#Procura os perfis de Twitter ativos no banco de dados
		cursor_tweets = self.bd.procura_perfis()

		#Para cada perfil do Twitter, processa os tweets retornados
		for (id_perfil, nome) in cursor_tweets:

			#Abre os ultimos tweets importados
			lt = self.le_tweets(nome)

			#API do Alchemy
			api = Alchemy()

			#Processa todos os tweets
			for tweet in lt:

				#Extrai o link do tweet
				link = URL.extrai_link(tweet.text)

				#Se nao houver link, pula para o proximo tweet
				if link == None:
					continue

				#Chama o AlchemyAPI para limpar o texto
				texto_processado = api.processa_html(link)

				#Adiciona noticia no Banco de Dados
				self.bd.adiciona_noticia(link, tweet.text, texto_processado, None, id_perfil)
