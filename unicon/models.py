from django.db import models
from sqlalchemy import Column, DateTime, ForeignKey, Index, String
from sqlalchemy.dialects.mysql import DATETIME, INTEGER, LONGTEXT, SMALLINT, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from django.contrib.auth.hashers import make_password, check_password

Base = declarative_base()
metadata = Base.metadata

# Create your models here.
class UsersDtl(Base):
    __tablename__ = 'users_dtls'

    usid = Column(INTEGER(11), primary_key=True)
    user_id = Column(String(45))
    password = Column(String(220))
    user_type = Column(String(45), comment='customer or supplier')
    category_type = Column(String(45), comment='buyers/sellers,machineresandspareparts,')
    status = Column(String(45))
    email = Column(String(120))
    phone = Column(String(45))
    def check_password(self, raw_password):
         return check_password(raw_password, self.password)

class CustomerDtl(Base):
    __tablename__ = 'customer_dtls'

    customer_id = Column(INTEGER(11), primary_key=True)
    user_id = Column(String(120))
    category_type = Column(String(200), comment='type of the item which the use is going to buy')
    customer_name = Column(String(45))
    organization_name = Column(String(100), comment='name of the schhol,collage,house etc ')
    designation = Column(String(45), comment='designation')
    place = Column(String(45))
    state = Column(String(45))
    districtl = Column(String(45))
    pincode = Column(String(45))
    phone_number = Column(String(45))
    prouduct_type = Column(String(45), comment='cousomized/readymade/accessories')

class SupplierTable(Base):
    __tablename__ = 'supplier_table'

    sid = Column(INTEGER(11), primary_key=True)
    user_id = Column(String(45))
    supplier_name = Column(String(45))
    organization_name = Column(String(120))
    org_started_year = Column(DateTime)
    place = Column(String(45))
    state = Column(String(45))
    district = Column(String(45))
    pincode = Column(String(45))
    gst_number = Column(String(45))
    udayam_number = Column(String(45))
    phone_number = Column(String(45))
    alternate_number = Column(String(45))
    email = Column(String(45))

class LaborsTechnision(Base):
    __tablename__ = 'labors_technisions'

    lid = Column(INTEGER(11), primary_key=True)
    cutsomer_name = Column(String(45))
    user_id = Column(String(45))
    gender = Column(String(45))
    place = Column(String(45))
    state = Column(String(45))
    district = Column(String(45))
    pincode = Column(String(45))
    phone = Column(String(45))
    alternate_number = Column(String(45))

class MachinesSparepart(Base):
    __tablename__ = 'machines_spareparts'

    mid = Column(INTEGER(11), primary_key=True)
    user_id = Column(String(45))
    customer_name = Column(String(45))
    designation = Column(String(45))
    adress = Column(String(120))
    place = Column(String(45))
    state = Column(String(45))
    districtl = Column(String(45))
    pincode = Column(String(45))
    email = Column(String(45))
    phone = Column(String(45))
    alternate_number = Column(String(45))
    org_name = Column(String(120))