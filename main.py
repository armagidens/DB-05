import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Sale, Book, Stock, Shop
import json

DSN = ''
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()



with open('tests_data.json', 'r') as db:
    data = json.load(db)

for line in data:
    method = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[line['model']]
    session.add(method(id=line['pk'], **line.get('fields')))
session.commit()


publusher_input = input('Укажите id или имя издателя: ')


if publusher_input.isnumeric():
    for c in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher.book).join(Book.stock_book).join(Stock.shop).join(Stock.sale).filter(Publisher.id == int(publusher_input)).all():   
        print(c)
else:
    for c in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher.book).join(Book.stock_book).join(Stock.shop).join(Stock.sale).filter(Publisher.name.like(f'%{publusher_input}%')).all():   
        print(c)

session.close()




