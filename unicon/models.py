from django.db import models
from sqlalchemy import Column, DateTime, ForeignKey, Index, String,text
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
    def is_authenticated():
        return True


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
    alternative_number = Column(String(45))

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
    payment_status = Column(String(45), server_default=text("'open'"))
    prod_type = Column(String(45))
    prod_sub_type = Column(String(45))
    is_companydeler = Column(String(5))
    compnay_names = Column(String(600))
    is_wholesaler = Column(String(5))
    is_retailer = Column(String(5))
    company_undertaking = Column(String(600))
    no_labours = Column(String(10))
    male_number = Column(String(10))
    female_number = Column(String(10))
    readymade_providng_items = Column(String(650))
    Providing_accesoseries = Column(String(650))



class SupplierProductionDtl(Base):
    __tablename__ = 'supplier_production_dtls'

    poduction_id = Column(INTEGER(11), primary_key=True)
    item_name = Column(String(30), nullable=False)
    item_count = Column(String(10), nullable=False)
    sid = Column(String(10), nullable=False)

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
    work_type = Column(String(45), nullable=False)
    status = Column(String(45), nullable=False)
    email = Column(String(45))

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
    work_type = Column(String(45))
    status = Column(String(45))
    

class CustomerOrderDtl(Base):
    __tablename__ = 'customer_order_dtls'

    order_id = Column(String(45))
    user_id = Column(String(45))
    product_type = Column(String(45))
    prod_sub_type = Column(String(45))
    category_type = Column(String(45))
    brand_name = Column(String(45))
    catalog_number = Column(String(45))
    design_no = Column(String(45))
    sahde_no = Column(String(45))
    photo = Column(String(45))
    delivery_date = Column(String(45))
    message = Column(String(45))
    is_invidulaystiched = Column(String(45))
    total_count = Column(String(45))
    id = Column(INTEGER(11), primary_key=True)


class CustomerAddProductDtl(Base):
    __tablename__ = 'customer_add_product_dtls'

    prod_id = Column(INTEGER(11), primary_key=True)
    order_id = Column(String(45))
    name = Column(String(45))
    size = Column(String(45))
    user_id = Column(String(45))

class CategoryDtl(Base):
    __tablename__ = 'category_dtls'

    cat_id = Column(INTEGER(11), primary_key=True)
    cat_name = Column(String(100), nullable=False)
    cat_item = Column(String(120), nullable=False)

class SupplierTempDtl(Base):
    __tablename__ = 'supplier_temp_dtls'

    temp_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(45))
    comapny_name = Column(String(200))
    start_year = Column(DateTime)
    place = Column(String(45))
    state = Column(String(45))
    district = Column(String(45))
    pincode = Column(String(15))
    gst_number = Column(String(20))
    udayam_number = Column(String(20))
    phone_number = Column(String(20))
    alt_phone_number = Column(String(20))
    email = Column(String(100))
    password = Column(String(150))

class ProductDtl(Base):
    __tablename__ = 'product_dtls'

    prod_id = Column(INTEGER(11), primary_key=True)
    item_name = Column(String(45))
    item_code = Column(String(45))
    size = Column(String(45))
    shades = Column(String(45))
    image = Column(String(45))
    price = Column(String(45))
    quantity = Column(String(45))
    status = Column(String(45))
    user_id = Column(String(45))
    prod_type = Column(String(45))
    prod_desc = Column(String(600))
    condition = Column(String(45))



class AuthToken(Base):
    __tablename__ = 'auth_token'

    id = Column(INTEGER(11), primary_key=True)
    key = Column(String(600))
    created = Column(String(45))
    user_id = Column(String(45))
