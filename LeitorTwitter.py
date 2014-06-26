import twitter
import URL

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
		for (id_perfil, nome, processador_html) in cursor_tweets:

			#Abre os ultimos tweets importados
			lt = self.le_tweets(nome)

			#Processa todos os tweets
			for tweet in lt:

				#Extrai o link do tweet
				link = URL.extrai_link(tweet.text)

				#Se nao houver link, pula para o proximo tweet
				if link == None:
					continue

				#Recupera o texto limpo
				texto_limpo = URL.le_site(link, processador_html, self.bd)

				#Adiciona noticia no Banco de Dados
				self.bd.adiciona_noticia(link, tweet.text, texto_limpo, None, id_perfil)