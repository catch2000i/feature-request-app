from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, scoped_session
 
from sqlalchemy_declarative import Base, Feature, Client, ProductArea, Date

engine = create_engine('sqlite:///sqlalchemy_example.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
 

# Insert new clients in the client table
new_client = Client(name='Client A')
session.add(new_client)
session.commit()
new_client = Client(name='Client B')
session.add(new_client)
session.commit()
new_client = Client(name='Client C')
session.add(new_client)
session.commit()

# Insert product areas in the product_area table
new_product_area = ProductArea(name='Policies')
session.add(new_product_area)
session.commit()
new_product_area = ProductArea(name='Billing')
session.add(new_product_area)
session.commit()
new_product_area = ProductArea(name='Claims')
session.add(new_product_area)
session.commit()
new_product_area = ProductArea(name='Reports')
session.add(new_product_area)
session.commit()


# Insert Features in the features table
new_feature = Feature(title='feature #1', description="This is full description for the feature #1...", client_priority=3, client_id=1, product_area_id=1, target_date=func.now())
session.add(new_feature)
session.commit()

new_feature = Feature(title='Lorem ipsum dolor sit amet, et cum habemus omnesque, utinam liberavisse ne his.', 
	description="Lorem ipsum is a pseudo-Latin text used in web design, typography, layout, and printing in place of English to emphasise design elements over content. It's also called placeholder (or filler) text. It's a convenient tool for mock-ups. It helps to outline the visual elements of a document or presentation, eg typography, font, or layout. Lorem ipsum is mostly a part of a Latin text by the classical author and philosopher Cicero.", 
	client_priority=1, client_id=2, product_area_id=2, target_date=func.now())
session.add(new_feature)
session.commit()

new_feature = Feature(title="It would be a stark turnaround in the story of Tesla, considering the company spent most of 2018", 
	description="This question was repeated a number of times during a call with industry analysts on January 30th where Tesla discussed its full financial results for 2018. Tesla still hasn’t started production of the $35,000 version of the Model 3 originally promised in 2016, and some on Wall Street are worried that the company has tapped out demand for the higher-priced versions of the car in the United States — especially as other automakers are warning of a rough 2019 as car sales cool worldwide.", 
	client_priority=1, client_id=1, product_area_id=3, target_date=func.now())
session.add(new_feature)
session.commit()

