from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

class EcomUser(Base):
  __tablename__ = "ecomusers"

  username = Column(String,primary_key=True,nullable = False)
  email = Column(String,nullable = False)
  password = Column(String,nullable=False)
  created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Roles(Base):
  __tablename__ = "roles"
  id = Column(Integer,primary_key=True,nullable = False,index=True)
  role = Column(String,nullable = False)

class UserRoles(Base):
   __tablename__="userroles"
   id = Column(Integer,primary_key=True,nullable = False,index=True)
   username = Column(String,ForeignKey("ecomusers.username",ondelete="CASCADE"),nullable = False)
   role_id = Column(Integer, ForeignKey("roles.id",ondelete="CASCADE"), nullable=False)



class Products(Base):
  __tablename__="ecomproducts"
  id = Column(Integer,primary_key=True,nullable = False,index=True, autoincrement=True)
  name = Column(String,nullable = False)
  price = Column(Float,nullable = False)
  quantity_available=Column(Integer,nullable = False)
  


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("ecomusers.username", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("ecomproducts.id", ondelete="CASCADE"))
    quantity = Column(Integer, nullable=False, default=1)
    total_price=Column(Integer,nullable=False)

    user = relationship("EcomUser", backref="cart_items")
    product = relationship("Products")

class Order(Base):
   __tablename__="orders"
   id=Column(Integer,primary_key=True,index=True)
   user_id = Column(String, ForeignKey("ecomusers.username", ondelete="CASCADE"))
   total_bill=Column(Integer,nullable=False)
   items = Column(JSON, nullable=False)
   placed_at= Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

   user = relationship("EcomUser", backref="orders")



