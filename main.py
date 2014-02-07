import leitor_feeds
import banco_dados
import processa_html

def noticia_importada(link):

	count_noticia = banco_dados.conta_noticias(link)

	return count_noticia.fetchone()[0] > 0

def le_site(link, titulo, id_feed):

	#Verifica se a noticia foi importada
	if noticia_importada(link):
		return

	#Recupera o HTML da URL
	html = processa_html.abre_url(link)

	#Limpa o texto em html
	texto_limpo = processa_html.html_texto(html)

	#Adiciona noticia no banco de dados
	banco_dados.adiciona_noticia(link, titulo, texto_limpo, id_feed)

def processa_feeds():

	cursor_feeds = banco_dados.cursor_feeds()

	#Para cada feed Atom, processa os links retornados
	for (id_feed, link) in cursor_feeds:
		
		posts = leitor_feeds.le_feed(id_feed, link)

		#Para cada post, limpa HTML e adiciona no banco de dados
		for post in posts.entries:
			le_site(post.link, post.title, id_feed)

	banco_dados.fecha_conexao()

processa_feeds()