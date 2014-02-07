import feedparser

def le_feed(id_feed, link):

	#Recupera os links atualizados
	posts = feedparser.parse(link)

	return posts