import BancoDados
from LogErros import LogErros
from LeitorFeeds import LeitorFeeds
from LeitorTwitter import LeitorTwitter

bd = BancoDados.BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias')

def executa():

	log = LogErros(bd)
	log.inicia_processo()

	lf = LeitorFeeds(bd, log)
	lf.processa_feeds()

	lt = LeitorTwitter(bd, log)
	lt.processa_twitter()

	bd.fecha_conexao()

executa()
