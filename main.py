import BancoDados
from LogErros import LogErros
from LeitorFeeds import LeitorFeeds
from LeitorTwitter import LeitorTwitter
from GeraCorpusMetaAnn import GeraCorpus
from IdentificadorEntidades import IdentificadorEntidades

bd = BancoDados.BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias')


def executa_crawler():

    log = LogErros(bd)
    log.inicia_processo()

    lf = LeitorFeeds(bd, log)
    lf.processa_feeds()

    lt = LeitorTwitter(bd, log)
    lt.processa_twitter()


def gera_corpus():

    gc = GeraCorpus(bd)
    gc.gera_noticias()
    bd.fecha_conexao()

def identifica_entidades():

    ie = IdentificadorEntidades(bd)
    # ie.atualiza_entidades()
    ie.identifica_entidades_tweets()

gera_corpus()
