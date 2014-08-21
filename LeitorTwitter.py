import traceback
import twitter
import URL
from Alchemy import Alchemy
from GestorNoticias import GestorNoticias

class LeitorTwitter(object):
	'Processa os posts do Twitter'

	def __init__(self, bd, log):
		self.api = twitter.Api('ou1umOYzfOprMk5YPaZtqG6HG','SdUsK8IAKCITSRvdmVYz0y4uQpCPzAsLJ9rQAim6fek1RGoDDc','2356629355-I35FpdV7hoBmxcZUy4OCscmmwejDrlsX7JL1OPM','2mntySesSInFr6ApQjQOcn1bTfctYKFHVjMFq7kevNtgp')
		self.log = log
		self.bd  = bd

	def le_tweets(self, nome):

		tweets = self.api.GetUserTimeline(screen_name=nome)

		return tweets

	def processa_twitter(self):

		#Procura os perfis de Twitter ativos no banco de dados
		cursor_tweets = self.bd.procura_perfis()

		#Para cada perfil do Twitter, processa os tweets retornados
		for (id_perfil, nome) in cursor_tweets:

			try:
				#Abre os ultimos tweets importados
				lt = self.le_tweets(nome)

				#API do Alchemy
				api = Alchemy()

				#Classe para insercao de noticias
				gn = GestorNoticias(self.bd, api)

				#Processa todos os tweets
				for tweet in lt:

					try:
						#Extrai o link do tweet
						link = URL.extrai_link(tweet.text)

						#Se nao houver link, pula para o proximo tweet
						if link == None:
							continue

						#Chama o AlchemyAPI para limpar o texto
						texto_processado = api.processa_html(link)
						titulo = api.obtem_titulo(link)

						#Adiciona noticia no Banco de Dados
						gn.adiciona_noticia(link, titulo, texto_processado, tweet.text, None, id_perfil)

					except:
						self.log.registra_erro('Erro ao extrair informacoes do link' + link + ' do tweet ' + tweet.text + ':' + traceback.format_exc())

			except:
				self.log.registra_erro('Erro ao processar perfil' + str(id_perfil) + ': ' + traceback.format_exc())
