# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Index, String
from sqlalchemy.dialects.mysql import DATETIME, INTEGER, LONGTEXT, SMALLINT, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AuthGroup(Base):
    __tablename__ = 'auth_group'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(150), nullable=False, unique=True)


class AuthUser(Base):
    __tablename__ = 'auth_user'

    id = Column(INTEGER(11), primary_key=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DATETIME(fsp=6))
    is_superuser = Column(TINYINT(1), nullable=False)
    username = Column(String(150), nullable=False, unique=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(TINYINT(1), nullable=False)
    is_active = Column(TINYINT(1), nullable=False)
    date_joined = Column(DATETIME(fsp=6), nullable=False)


class CustomerAddProductDtl(Base):
    __tablename__ = 'customer_add_product_dtls'

    prod_id = Column(INTEGER(11), primary_key=True)
    order_id = Column(String(45))
    name = Column(String(45))
    size = Column(String(45))
    user_id = Column(String(45))


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


class CustomerOrderDtl(Base):
    __tablename__ = 'customer_order_dtls'

    order_id = Column(INTEGER(11), primary_key=True)
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


class DjangoContentType(Base):
    __tablename__ = 'django_content_type'
    __table_args__ = (
        Index('django_content_type_app_label_model_76bd3d3b_uniq', 'app_label', 'model', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    app_label = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)


class DjangoMigration(Base):
    __tablename__ = 'django_migrations'

    id = Column(INTEGER(11), primary_key=True)
    app = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    applied = Column(DATETIME(fsp=6), nullable=False)


class DjangoSession(Base):
    __tablename__ = 'django_session'

    session_key = Column(String(40), primary_key=True)
    session_data = Column(LONGTEXT, nullable=False)
    expire_date = Column(DATETIME(fsp=6), nullable=False, index=True)


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


class SupplierAddProd(Base):
    __tablename__ = 'supplier_add_prods'

    sid = Column(INTEGER(11), primary_key=True)
    order_id = Column(String(45))
    type = Column(String(45), comment="type 'comapany' companuy name \\ntype'product , product_count")
    names = Column(String(45))
    item_name = Column(String(45))
    count = Column(String(45))


class SupplierOrderDtl(Base):
    __tablename__ = 'supplier_order_dtls'

    supplier_order_id = Column(INTEGER(11), primary_key=True)
    user_id = Column(String(45))
    product_type = Column(String(45), comment='customized_uniformss,readymades,unifromaccrs')
    product_subtype = Column(String(45), comment='fabric,stiching,fabricandstichng')
    is_company_dealer = Column(String(45))
    compnaies_that_leads = Column(String(45))
    is_whole_saler = Column(String(45))
    is_retailer = Column(String(45))
    company_name = Column(String(45))
    labours_number = Column(String(45))
    male_numbers = Column(String(45))
    categoriesl = Column(String(45))
    provided_items = Column(String(45))


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


class AuthPermission(Base):
    __tablename__ = 'auth_permission'
    __table_args__ = (
        Index('auth_permission_content_type_id_codename_01ab375a_uniq', 'content_type_id', 'codename', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)
    content_type_id = Column(ForeignKey('django_content_type.id'), nullable=False)
    codename = Column(String(100), nullable=False)

    content_type = relationship('DjangoContentType')


class AuthUserGroup(Base):
    __tablename__ = 'auth_user_groups'
    __table_args__ = (
        Index('auth_user_groups_user_id_group_id_94350c0c_uniq', 'user_id', 'group_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False)
    group_id = Column(ForeignKey('auth_group.id'), nullable=False, index=True)

    group = relationship('AuthGroup')
    user = relationship('AuthUser')


class AuthtokenToken(Base):
    __tablename__ = 'authtoken_token'

    key = Column(String(40), primary_key=True)
    created = Column(DATETIME(fsp=6), nullable=False)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False, unique=True)

    user = relationship('AuthUser')


class DjangoAdminLog(Base):
    __tablename__ = 'django_admin_log'

    id = Column(INTEGER(11), primary_key=True)
    action_time = Column(DATETIME(fsp=6), nullable=False)
    object_id = Column(LONGTEXT)
    object_repr = Column(String(200), nullable=False)
    action_flag = Column(SMALLINT(5), nullable=False)
    change_message = Column(LONGTEXT, nullable=False)
    content_type_id = Column(ForeignKey('django_content_type.id'), index=True)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False, index=True)

    content_type = relationship('DjangoContentType')
    user = relationship('AuthUser')


class AuthGroupPermission(Base):
    __tablename__ = 'auth_group_permissions'
    __table_args__ = (
        Index('auth_group_permissions_group_id_permission_id_0cd325b0_uniq', 'group_id', 'permission_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    group_id = Column(ForeignKey('auth_group.id'), nullable=False)
    permission_id = Column(ForeignKey('auth_permission.id'), nullable=False, index=True)

    group = relationship('AuthGroup')
    permission = relationship('AuthPermission')


class AuthUserUserPermission(Base):
    __tablename__ = 'auth_user_user_permissions'
    __table_args__ = (
        Index('auth_user_user_permissions_user_id_permission_id_14a6b632_uniq', 'user_id', 'permission_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False)
    permission_id = Column(ForeignKey('auth_permission.id'), nullable=False, index=True)

    permission = relationship('AuthPermission')
    user = relationship('AuthUser')
