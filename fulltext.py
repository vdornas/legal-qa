from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
from whoosh.filedb.filestore import FileStorage

schema = Schema(teorArtigo=TEXT(analyzer=StemmingAnalyzer()),
                numArtigo=TEXT(analyzer=StemmingAnalyzer()),
                pergunta =TEXT(analyzer=StemmingAnalyzer()),
                idResposta=ID(stored=True))

storage = FileStorage("index")
ix = storage.create_index(schema)

ix = storage.open_index()
writer = ix.writer()





