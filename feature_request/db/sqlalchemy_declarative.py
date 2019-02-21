import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Table, MetaData, select, func, Sequence, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Feature(Base):
	__tablename__ = 'feature'
	id = Column(Integer, primary_key=True)
	title = Column(String(100), nullable=False) 
	description = Column(String(500))
	client_priority = Column(Integer, nullable=False)
	client_id = Column(Integer, ForeignKey('client.id'))
	product_area_id = Column(Integer, ForeignKey('product_area.id'))
	target_date = Column(Date)
	
	def __repr__(self):
		return "<Feature(id='%d', title='%s', description='%s', client_priority='%d', client_id='%d', product_area_id='%d', target_date='%s' )>" % (
						self.id, self.title, self.description, self.client_priority, self.client_id, self.product_area_id, self.target_date)

class Client(Base):
	__tablename__ = 'client'
	id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable=False)
	
	def __repr__(self):
		return "<Client(id='%d', name='%s')>" % (self.id, self.name)

class ProductArea(Base):
	__tablename__ = 'product_area'
	id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable=False)

	def __repr__(self):
		return "<ProductArea(id='%d', name='%s')>" % (self.id, self.name)


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqlalchemy_example.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
