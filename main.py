import BancoDados
import ProcessadorHTML
from LeitorFeeds import LeitorFeeds
from LeitorTwitter import LeitorTwitter

bd = BancoDados.BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias')

def executa():
	# lf = LeitorFeeds(bd)
	# lf.processa_feeds()

	lt = LeitorTwitter(bd)
	lt.processa_twitter()

	bd.fecha_conexao()

executa()
