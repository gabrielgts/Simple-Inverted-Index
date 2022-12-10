from database import Database
from invertedindex import InvertedIndex
from gui import Gui
from indexer import Indexer

def main():
    db = Database()
    index = InvertedIndex(db)
    Indexer('index.html', index)
    index.export_data_frame()
    Gui(index.get_data_frame().items())

main()
