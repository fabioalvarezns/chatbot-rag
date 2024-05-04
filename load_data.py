from tools.data_load_vd import books_load
from tools.qdrant_manager import qdrant_manager
from tools.parameters import Config
from tools.data_load_vd import books_load

# #new_book = books_load('KB/fuentes/mundodesofia.pdf',200,50,'El mundo de Sofia','Jostein Gaarder')
sofia_database = qdrant_manager(Config.SOFIA_DEV_URL,Config.SOFIA_DEV_KEY)

load = books_load('KB/fuentes/mundodesofia.pdf',300,50,'El mundo de Sofia', 'Jostein Gaarder', Config.OPENAI_KEY)

data = load.prepare_data('El mundo de Sofia')['data']

load_data = load.load_data(100,data,'books')

print(data[0])


# sofia_database.create_collection('books',768)

#sofia_database.delete_collection('books')