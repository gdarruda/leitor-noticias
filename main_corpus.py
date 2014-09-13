import BancoDados
from GeraCorpusUAM import GeraCorpus

bd = BancoDados.BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias')

def gera_corpus():

  gc = GeraCorpus(bd)
  gc.gera_noticias()
  bd.fecha_conexao()

gera_corpus()
