# coding=utf-8
import urllib
import ProcessadorHTML

def abre_url(link):

	#Abre URL e carrega o HTML em uma String
	url = urllib.urlopen(link)
	html = url.read()

	return html

def extrai_link(tweet):

	#Encontra a URL do Tweet
	posic_url_ini = tweet.find('http://')

	#Se nao encontrou nenhuma posicao, retorna nulo
	if posic_url_ini == -1:
		return None

	#Encontra o primeiro espaco depois do inicio do link
	posic_url_fim = tweet.find(' ', posic_url_ini) + 1

	#Retorna o inicio da URL ate o primeiro espaco ou fim
	if posic_url_fim == 0:
		return tweet[posic_url_ini:]
	else:
		return tweet[posic_url_ini:posic_url_fim]
	

def url_importada(link, bd):

	#Verifica se a URL já está presente no Banco de Dados
	count_noticia = bd.conta_noticias(link)

	#Retorna o contador
	return count_noticia.fetchone()[0] > 0

def le_site(link, processador_html, bd):

	#Verifica se a noticia foi importada
	if url_importada(link, bd):
		return

	#Recupera o HTML da URL
	html = abre_url(link)

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
	return ph.processa_html()