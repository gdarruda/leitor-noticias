import LeitorFeeds
import BancoDados
import ProcessadorHTML
from LeitorFeeds import LeitorFeeds

bd = BancoDados.BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias')

def noticia_importada(link):

	count_noticia = bd.conta_noticias(link)

	return count_noticia.fetchone()[0] > 0

def le_site(link, titulo, id_feed, processador_html):

	#Verifica se a noticia foi importada
	if noticia_importada(link):
		return

	#Recupera o HTML da URL
	html = LeitorFeeds.abre_url(link)

	#Caso nao esteja paramerizado nenhum tipo, utiliza o valor padrao
	if processador_html is None:
		processador_html = 'ProcessadorHTML'

	#Instancia dinamicamente o processador de HTML
	try:
		ph = getattr(ProcessadorHTML, processador_html)(html)
	except AttributeError:
		print 'Classe nao carregada: ' +  processador_html
		return

	#Limpa o texto em html
	texto_limpo = ph.processa_html()

	#Adiciona noticia no banco de dados
	bd.adiciona_noticia(link, titulo, texto_limpo, id_feed)

def processa_feeds():
	
	#Procura os feeds ativos no banco de dados
	cursor_feeds = bd.procura_feeds()

	#Para cada feed Atom, processa os links retornados
	for (id_feed, link, processador_html) in cursor_feeds:

		#Recupera o catalogo de links RSS
		lf = LeitorFeeds(link)
		posts = lf.le_feed()

		#Para cada post, limpa HTML e adiciona no banco de dados
		for post in posts.entries:
			le_site(post.link, post.title, id_feed, processador_html)

	bd.fecha_conexao()

processa_feeds()