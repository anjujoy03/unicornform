from django.shortcuts import render
import json,jwt
import os
from dateutil.relativedelta import relativedelta
import  datetime
from datetime import timedelta
from sqlalchemy import inspect, asc, desc, text, func, extract, and_
from sqlalchemy.orm import load_only
from sqlalchemy.exc import SQLAlchemyError
from rest_framework.response import Response
from rest_framework.views import APIView
from decimal import Decimal
import math, random 
import string,random
from rest_framework.decorators import api_view, permission_classes, renderer_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import Column,String
from django.core.mail import send_mail

from rest_framework import status
from django.template.loader import render_to_string
from unicon.models import UsersDtl,CustomerDtl,SupplierTable,LaborsTechnision,MachinesSparepart,CustomerOrderDtl,CustomerAddProductDtl,CategoryDtl,SupplierTempDtl,SupplierProductionDtl,ProductDtl,AuthToken,QuotationTable,QutationDtl
import pandas as pd
from uniconform.sqlalchamyencoder import AlchemyEncoder
from uniconform import dbsession
from django.template import loader 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.module_loading import import_string
from django.middleware.csrf import get_token
from uniconform.JSONDateSerializer import JSONDateEncoder
from uniconform.restframeworkTokenAuthentication import TokenAuthentication
from django.core.files.storage import FileSystemStorage




# @api_view(['GET','POST'])
# @permission_classes([AllowAny, ])
# def csrftokens(request):
# 	try:
	
# 		csrf = get_token(request) 
# 		return Response({'csrf_token':csrf})
# 	except KeyError:
# 		res = {'error': 'token not generated'}
# 		return Response(res)

def generateUserId(email_txt):
	number = '{:06d}'.format(random.randrange (1,999)) 
	customer_id = '{}{}'.format(email_txt, number)
	return customer_id

def checkUserIdisExist(id):
	try:
		session = dbsession.Session()
		uid_length = session.query(UsersDtl).filter(UsersDtl.user_id==id).all()
		if(len(uid_length) == 0):
			return id
		else:
			user_id = generateUserId(id)
			checkUserIdisExist(user_id)
		session.close()
	except SQLAlchemyError as e:
		session.rollback()
		session.close()
		return False

def getUserId(email):
	try:
		# email_txt = email.split("@")[0]
		# email_txt = email_txt[0:3]
		user_id = generateUserId(email)
		user_id = checkUserIdisExist(user_id)
		return user_id
	except SQLAlchemyError as e:
		return Response({'status':'ERROR'})


def SendEmail(params):
    
    ctx={
        'OTP':params['user_id']
    }
    plaintext = get_template('mail.txt')
    htmly     = get_template('mail.html')
    subject, from_email, to = 'Hello from Uniconform', 'anjujoy0310@gmail.com', params['email']
    text_content = plaintext.render(ctx)
    html_content = htmly.render(ctx)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    res=msg.send(fail_silently=False)
    
    if(res==1):
        return True
    else:
        return False

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def SaveCustomer(request):
    try:
        session = dbsession.Session()
        email=request.data['email']
        phone=request.data['phone_number']
            # phno_check = session.query(UsersDtl).filter(UsersDtl.phone==phone).all()
            # if(len(phno_check) > 0):
            #     return Response({'status': 'phone num exists','message':'phone num already exists'})
            # email_check = session.query(UsersDtl).filter(UsersDtl.email==email).all()
            # if(len(email_check) > 0):
            #     return Response({'status': 'email  exists','message':'email already exists'})

        user_id = getUserId(request.data['category_type'])
        otpParams ={
                "user_id":user_id,
                "email":email
                }
        emailResult=SendEmail(otpParams)
        print(emailResult)
           

        user = UsersDtl()

        raw_password = make_password(request.data['password'])
        user.user_id = user_id
        user.user_type = 'Buyer'
        user.category_type = request.data['category_type']
        user.password = raw_password
        user.email=email
        user.phone=phone
        user.status='login'
        session.add(user)
        customer = CustomerDtl()
        customer.category_type='Buyer'
        customer.user_id=user_id
        customer.customer_name=request.data['customer_name']
        customer.organization_name=request.data['organization_name']
        customer.designation=request.data['designation']
        customer.place=request.data['place']
        customer.state=request.data['state']
        customer.districtl=request.data['districtl']
        customer.pincode=request.data['pincode']
        customer.email=request.data['email']
        customer.phone_number=request.data['phone_number']
        customer.alternative_number=request.data['alternative_number']
        session.add(customer)
        session.commit()
            # if request.data['user_type']=='uniform' and request.data['category_type']=='supplier':
            #     supplier=SupplierTable()
            #     supplier.user_id=user_id
            #     supplier.supplier_name=request.data['supplier_name']
            #     supplier.organization_name=request.data['organization_name']
            #     supplier.org_started_year=request.data['org_started_year']
            #     supplier.place=request.data['place']
            #     supplier.state=request.data['state']
            #     supplier.district=request.data['district']
            #     supplier.pincode=request.data['pincode']
            #     supplier.gst_number=request.data['gst_number']
            #     supplier.udayam_number=request.data['udayam_number']
            #     supplier.phone_number=request.data['phone_number']
            #     supplier.alternate_number=request.data['alternate_number']
            #     supplier.email=request.data['email']
            #     session.add(supplier)
            #     session.commit()
            # if request.data['user_type']=='other' and request.data['category_type']=='Machines':
            #     machine=MachinesSparepart()
            #     machine.user_id=user_id
            #     machine.customer_name=request.data['customer_name']
            #     machine.designation=request.data['designation']
            #     machine.adress=request.data['adress']
            #     machine.place=request.data['place']
            #     machine.state=request.data['state']
            #     machine.districtl=request.data['districtl']
            #     machine.pincode=request.data['pincode']
            #     machine.email=request.data['email']
            #     machine.phone=request.data['phone_number']
            #     machine.alternate_number=request.data['alternate_number']
            #     machine.org_name=request.data['org_name']
            #     session.add(machine)
            #     session.commit()
            # if request.data['user_type']=='other' and request.data['category_type']=='Labours':
            #     labors=LaborsTechnision()
            #     labors.cutsomer_name=request.data['customer_name']
            #     labors.user_id=user_id
            #     labors.gender=request.data['gender']
            #     labors.place=request.data['place']
            #     labors.state=request.data['state']
            #     labors.district=request.data['district']
            #     labors.pincode=request.data['pincode']
            #     labors.phone=request.data['phone_number']
            #     labors.alternate_number=request.data['alternate_number']
            #     session.add(labors)
            #     session.commit()
        
        if(emailResult == True):
            session.commit()
            session.close()
            return Response({'response':'success'})
        else:
            session.rollback()
            session.close()
            return Response({'response':'Error occured'})



        session.close()
        return Response({'response': 'Data saved success fully'})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

def get_user(user_id):
    try:
        session = dbsession.Session()
        user_data = session.query(UsersDtl).filter(UsersDtl.user_id==user_id).one()      
    except NoResultFound:
        session.rollback()
        session.close()
        return None
    return user_data


@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def Authenticate(request):
    try:
        session = dbsession.Session()
        user_id = request.data['user_id']
        password = request.data['password']
            #user = authenticate(request, user_id=user_id, password=password)
        
        user_data = get_user(user_id)
        if user_data == None:
            return Response({'response': 'Error','message':'Please provide a valid user name'})
        user = session.query(UsersDtl).filter(UsersDtl.user_id==user_id,UsersDtl.status=='login').one()
        if user.check_password(password):
            # DateEncoder = JSONDateEncoder()
            # payload = {
            #     'user_id': user.user_id,
			# 	'expiry' : DateEncoder.default(datetime.date.today() + datetime.timedelta(days=1))
			# 	}
            # token = jwt.encode(payload, settings.SECRET_KEY)
            # print(token)
            # session.query(AuthToken).filter_by(user_id=user.user_id).delete()
            # auth_token = AuthToken()
            # auth_token.key = token
            # auth_token.created = datetime.datetime.now()
            # auth_token.user_id = user.user_id
            # session.add(auth_token)
            session.commit()
            user_details = {}
            # user_details['token'] = token
            customer_dtls=session.query(UsersDtl.user_type,UsersDtl.user_id).filter(UsersDtl.user_id==user_id).all()
            customer_dtls_list = json.loads(json.dumps(customer_dtls, cls=AlchemyEncoder))
            user_details['data'] = customer_dtls_list
        else:
            return Response({'response': 'Error','message':'Please provide a valid credentials'})


                # if request.data['user_type']=='uniform' and request.data['sub_type']=='customer':
                #     customer_dtls=session.query(CustomerDtl).filter(CustomerDtl.user_id==user_id).all()
                #     if len(customer_dtls)==0:
                #         return Response({'response': 'error','message':'user not found in the specified category'})
                #     else:
                #         customer_dtls_list = json.loads(json.dumps(customer_dtls, cls=AlchemyEncoder))
                #         return Response({'response': 'success','data':customer_dtls_list,'type':'buyerandseller','category':'customer'})

            #     if request.data['user_type']=='unifom' and request.data['sub_type']=='supplier':
            #         customer_dtls=session.query(SupplierTable).filter(SupplierTable.user_id==user_id).all()
                   
            #         if len(customer_dtls)==0:
            #             return Response({'response': 'error','message':'user not found in the specified category'})
            #         else:
            #             customer_dtls_list = json.loads(json.dumps(customer_dtls, cls=AlchemyEncoder))
            #             return Response({'response': 'success','data':customer_dtls_list,'type':'buyerandseller','category':'supplier'})

            #     if request.data['user_type']=='other' and request.data['category_type']=='Machines':
            #         customer_dtls=session.query(MachinesSparepart).filter(MachinesSparepart.user_id==user_id).all()
            #         if len(customer_dtls)==0:
            #             return Response({'response': 'error','message':'user not found in the specified category'})
            #         else:
            #             customer_dtls_list = json.loads(json.dumps(customer_dtls, cls=AlchemyEncoder))
            #             return Response({'response': 'success','data':customer_dtls_list,'type':'Machinesandspareparts','category':'none'})
                   
            #     if request.data['user_type']=='other' and request.data['category_type']=='Labours':
            #         customer_dtls=session.query(LaborsTechnision).filter(LaborsTechnision.user_id==user_id).all()
            #         if len(customer_dtls)==0:
            #             return Response({'response': 'error','message':'user not found in the specified category'})
            #         else:
            #             customer_dtls_list = json.loads(json.dumps(customer_dtls, cls=AlchemyEncoder))
            #             return Response({'response': 'success','data':customer_dtls_list,'type':'Labours','category':'none'})
            
            # else:
            #     return Response({'response': 'Error','message':'Please provide a valid credentails'})


            
        session.close()
        return Response({'response': 'success','data':user_details})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})
@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def AddCustomerordes(request):
    try:
        session = dbsession.Session()
        user_id = request.data['user_id']
        
        product_type=request.data['product_type']
        if request.data['product_type']=="Customized Uniforms" and request.data['prod_sub_type']=="Fabrics":
            print("================02200")
            sql = text('SELECT MAX(CONVERT(REPLACE(order_id,"PF",""),UNSIGNED INTEGER)) as auto_order_id from customer_order_dtls')
            auto_order_id = session.execute(sql).fetchall()
            order_id = auto_order_id[0][0]
            if order_id == None or order_id == 0 :
                order_id = 100000
            order_id = 'PF'+ str(int(order_id + 1))
            myfile=request.FILES['file']
            print(order_id)
            order=CustomerOrderDtl()
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            order.photo=uploaded_file_url
            order.order_id=order_id
            order.user_id=request.data['user_id']
            order.product_type=request.data['product_type']
            order.prod_sub_type=request.data['prod_sub_type']
            order.category_type=request.data['model_type']
            order.brand_name=request.data['brand_name']
            order.catalog_number=request.data['catalog_number']
            order.design_no=request.data['design_no']

                
            order.sahde_no=request.data['shade_no']
            order.delivery_date=request.data['delivery_date']
            order.message=request.data['message']
            session.add(order)
            for x in json.loads(request.data['order_lines']):
                print(x)
                addprod=CustomerAddProductDtl()
                addprod.order_id=order.order_id
                addprod.user_id=request.data['user_id']
                addprod.name=x['item']
                addprod.size=x['count']
                session.add(addprod)

            session.commit()
            session.close()

        if request.data['product_type']=='Customized Uniforms' and request.data['prod_sub_type']=='Stitching':
            print("==========")
            sql = text('SELECT MAX(CONVERT(REPLACE(order_id,"PT",""),UNSIGNED INTEGER)) as auto_order_id from customer_order_dtls')
            auto_order_id = session.execute(sql).fetchall()
            order_id = auto_order_id[0][0]
            if order_id == None or order_id == 0 :
                order_id = 100000
            order_id = 'PT' + str(int(order_id + 1))
                
            myfile=request.FILES['file']
            order=CustomerOrderDtl()
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            order.photo=uploaded_file_url
            order.order_id=order_id
            order.user_id=request.data['user_id']
            order.product_type=request.data['product_type']
            order.prod_sub_type=request.data['prod_sub_type']
            order.category_type=request.data['model_type']
            order.delivery_date=request.data['delivery_date']
            order.message=request.data['message']
            order.is_invidulaystiched=request.data['stich_type']
            order.total_count=request.data['total_count']
            session.add(order)
            for x in json.loads(request.data['order_lines']):
                addprod=CustomerAddProductDtl()
                addprod.order_id=order.order_id
                addprod.user_id=request.data['user_id']
                addprod.name=x['item']
                addprod.size=x['count']
                session.add(addprod)
            session.commit()
            session.close()
        if request.data['product_type']=='Customized Uniforms' and request.data['prod_sub_type']=='Fabric and Stitching':
            sql = text('SELECT MAX(CONVERT(REPLACE(order_id,"PS",""),UNSIGNED INTEGER)) as auto_order_id from customer_order_dtls')
            auto_order_id = session.execute(sql).fetchall()
            order_id = auto_order_id[0][0]
            if order_id == None or order_id == 0 :
                order_id = 100000
            order_id = 'PS' + str(int(order_id + 1))
            myfile=request.FILES['file']
            order=CustomerOrderDtl()
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            order.photo=uploaded_file_url
            order.order_id=order_id
            order.user_id=request.data['user_id']
            order.product_type=request.data['product_type']
            order.prod_sub_type=request.data['prod_sub_type']
            order.category_type=request.data['model_type']
            # order.brand_name=request.data['brand_name']
            # order.catalog_number=request.data['catalog_number']
            # order.design_no=request.data['design_no']
            order.photo=request.data['photo']
            # order.sahde_no=request.data['shade_no']
            order.delivery_date=request.data['delivery_date']
            order.message=request.data['message']
            order.is_invidulaystiched=request.data['stich_type']
            order.total_count=request.data['total_count']
            session.add(order)

            for x in json.loads(request.data['order_lines']):
                addprod=CustomerAddProductDtl()
                addprod.order_id=order.order_id
                addprod.user_id=request.data['user_id']
                addprod.name=x['item']
                addprod.size=x['count']
                session.add(addprod)
            session.commit()
            session.close()
        if request.data['product_type']=='ReadyMade Uniforms' and request.data['prod_sub_type']=='OrderBasedForm':
            print(request.data)
            order=CustomerOrderDtl()
            sql = text('SELECT MAX(CONVERT(REPLACE(order_id,"PR",""),UNSIGNED INTEGER)) as auto_order_id from customer_order_dtls')
            auto_order_id = session.execute(sql).fetchall()
            order_id = auto_order_id[0][0]
            if order_id == None or order_id == 0 :
                order_id = 100000
            order_id = 'PR' + str(int(order_id + 1))
            myfile=request.FILES['file']
            order=CustomerOrderDtl()
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            order.photo=uploaded_file_url
            order.order_id=order_id
            order.user_id=request.data['user_id']
            order.product_type=request.data['product_type']
            order.prod_sub_type=request.data['prod_sub_type']
            order.category_type=request.data['model_type']
            order.photo=request.data['photo']
            order.delivery_date=request.data['delivery_date']
            order.message=request.data['message']
            session.add(order)
            session.commit()
            for x in json.loads(request.data['order_lines']):
                addprod=CustomerAddProductDtl()
                addprod.order_id=order.order_id
                addprod.user_id=request.data['user_id']
                addprod.name=x['item']
                addprod.size=x['count']
                session.add(addprod)
            session.commit()
            session.close()
        if request.data['product_type']=='ReadyMade Uniforms' and request.data['prod_sub_type']=='StockBasedList':
            sql = text('SELECT MAX(CONVERT(REPLACE(order_id,"PR",""),UNSIGNED INTEGER)) as auto_order_id from customer_order_dtls')
            auto_order_id = session.execute(sql).fetchall()
            order_id = auto_order_id[0][0]
            if order_id == None or order_id == 0 :
                order_id = 100000
            order_id = 'PR' + str(int(order_id + 1))
            myfile=request.FILES['file'] 
            order=CustomerOrderDtl()
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            order.photo=uploaded_file_url
            order.order_id=order_id
            order.user_id=request.data['user_id']
            order.product_type=request.data['product_type']
            order.prod_sub_type=request.data['prod_sub_type']
            order.category_type=request.data['model_type']
            order.delivery_date=request.data['delivery_date']
            order.message=request.data['message']
            session.add(order)
            for x in json.loads(request.data['order_lines']):
                addprod=CustomerAddProductDtl()
                addprod.order_id=order.order_id
                addprod.user_id=request.data['user_id']
                addprod.name=x['item']
                addprod.size=x['count']
                session.add(addprod)
            session.commit()
            session.close()
            print(request.data['product_type']=='Uniform Accesoriess' and request.data['prod_sub_type']=='none')
        if request.data['product_type']=='Uniform Accesoriess' and request.data['prod_sub_type']=='none':
            print("=====ew=e=wewerwerre")
            sql = text('SELECT MAX(CONVERT(REPLACE(order_id,"AC",""),UNSIGNED INTEGER)) as auto_order_id from customer_order_dtls')
            auto_order_id = session.execute(sql).fetchall()
            order_id = auto_order_id[0][0]
            if order_id == None or order_id == 0 :
                order_id = 100000
            order_id = 'AC' + str(int(order_id + 1))
            order=CustomerOrderDtl()
            order.order_id=order_id
            order.user_id=request.data['user_id']
            order.product_type=request.data['product_type']
            order.prod_sub_type=request.data['prod_sub_type']
            order.delivery_date=request.data['delivery_date']
            session.add(order)
            for x in json.loads(request.data['order_lines']):
                addprod=CustomerAddProductDtl()
                addprod.order_id=order.order_id
                addprod.user_id=request.data['user_id']
                addprod.name=x['item']
                addprod.size=x['count']
                session.add(addprod)
            session.commit()
            session.close()
        return Response({'response': 'Data saved success fully'})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def SaveLabours(request):
    try:
        session = dbsession.Session()
        email=request.data['email']
        phone=request.data['phone_number']
            # phno_check = session.query(UsersDtl).filter(UsersDtl.phone==phone).all()
            # if(len(phno_check) > 0):
            #     return Response({'status': 'phone num exists','message':'phone num already exists'})
            # email_check = session.query(UsersDtl).filter(UsersDtl.email==email).all()
            # if(len(email_check) > 0):
            #     return Response({'status': 'email  exists','message':'email already exists'})

        user_id = getUserId('LA')
        otpParams ={
                "user_id":user_id,
                "email":email
            }
        emailResult=SendEmail(otpParams)
        print(emailResult)
           

        user = UsersDtl()

        raw_password = make_password(request.data['password'])
        user.user_id = user_id
        user.user_type = 'Labrous and Technicians'
        user.category_type = 'LA'
        user.password = raw_password
        user.email=email
        user.phone=phone
        session.add(user)
        labors=LaborsTechnision()
        labors.cutsomer_name=request.data['customer_name']
        labors.user_id=user_id
        labors.gender=request.data['gender']
        labors.place=request.data['place']
        labors.state=request.data['state']
        labors.district=request.data['district']
        labors.pincode=request.data['pincode']
        labors.phone=request.data['phone_number']
        labors.alternate_number=request.data['alternate_number']
        labors.work_type=request.data['work_type']
        labors.email=request.data['email']
        labors.status="active"
        session.add(labors)
        session.commit()
        if(emailResult == True):
            session.commit()
            session.close()
            return Response({'response':'success'})
        else:
            session.rollback()
            session.close()
            return Response({'response':'Error occured'})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def SaveMachiners(request):
    try:
        session = dbsession.Session()
        email=request.data['email']
        phone=request.data['phone_number']
            # phno_check = session.query(UsersDtl).filter(UsersDtl.phone==phone).all()
            # if(len(phno_check) > 0):
            #     return Response({'status': 'phone num exists','message':'phone num already exists'})
            # email_check = session.query(UsersDtl).filter(UsersDtl.email==email).all()
            # if(len(email_check) > 0):
            #     return Response({'status': 'email  exists','message':'email already exists'})

        user_id = getUserId('MA')
        otpParams ={
            "user_id":user_id,
            "email":email
            }
        emailResult=SendEmail(otpParams)
        print(emailResult)
        user = UsersDtl()
        raw_password = make_password(request.data['password'])
        user.user_id = user_id
        user.user_type = 'supplier'
        user.category_type = 'MA'
        user.password = raw_password
        user.email=email
        user.phone=phone
        session.add(user)
        machine=MachinesSparepart()
        machine.user_id=user_id
        machine.customer_name=request.data['customer_name']
        machine.designation=request.data['designation']
        machine.adress=request.data['adress']
        machine.place=request.data['place']
        machine.state=request.data['state']
        machine.districtl=request.data['district']
        machine.pincode=request.data['pincode']
        machine.email=request.data['email']
        machine.phone=request.data['phone_number']
        machine.alternate_number=request.data['alternate_number']
        machine.org_name=request.data['org_name']
        session.add(machine)
        session.commit()
        if(emailResult == True):
            session.commit()
            session.close()
            return Response({'response':'success'})
        else:
            session.rollback()
            session.close()
            return Response({'response':'Error occured'})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

class saveCategories(APIView):
    def post(self, request):
        try:
            session = dbsession.Session()
            category_type = request.data['category_type']
            for x in request.data['category_list']:
                category = CategoryDtl()
                category.cat_name=category_type
                category.cat_item=x['item']
                session.add(category)
            session.commit()
            session.close()
            return Response({'response': 'Success'})
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            session.close()
            return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def getCategories(request):
    try:
        session = dbsession.Session()
        category_type = request.data['category_type']
        sql = text("SELECT * from category_dtls where cat_name='"+category_type+"'")
        category_dtls = session.execute(sql).fetchall()
        category_dtls_list = [dict(row) for row in category_dtls]
        session.close()
        return Response({'response': 'Success','category_dtls_list':category_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

class getStockBasedList(APIView):
    def post(self, request):
        try:
            session = dbsession.Session()
            category_type = request.data['category_type']
            category_dtls=session.query(CategoryDtl.cat_item).filter(CategoryDtl.cat_name==category_type).all()
            category_dtls_list = json.loads(json.dumps(category_dtls, cls=AlchemyEncoder))

            session.close()
            return Response({'response': 'Success','category_dtls_list':category_dtls_list})
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            session.close()
            return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def SaveSupplier(request):
    try:
        session = dbsession.Session()
        # email=request.data['email']
        # phone=request.data['phone_number']
        print(request.data)
        delete_id=request.data['temp_id']
        data=session.query(SupplierTempDtl.name,SupplierTempDtl.start_year,SupplierTempDtl.comapny_name,SupplierTempDtl.place,SupplierTempDtl.state,SupplierTempDtl.district,SupplierTempDtl.pincode,SupplierTempDtl.gst_number,SupplierTempDtl.udayam_number,SupplierTempDtl.phone_number,SupplierTempDtl.alt_phone_number,SupplierTempDtl.email,SupplierTempDtl.password).filter(SupplierTempDtl.temp_id==delete_id).one()
        print(data[0])
        #session.query(SupplierTempDtl).filter(SupplierTempDtl.temp_id==delete_id).delete()

            # phno_check = session.query(UsersDtl).filter(UsersDtl.phone==phone).all()
            # if(len(phno_check) > 0):
            #     return Response({'status': 'phone num exists','message':'phone num already exists'})
            # email_check = session.query(UsersDtl).filter(UsersDtl.email==email).all()
            # if(len(email_check) > 0):
            #     return Response({'status': 'email  exists','message':'email already exists'})
        


        if request.data['prod_type']=='Customized Uniforms' and request.data['sub_type']=='fabric':
            user_id = getUserId('FS')
            otpParams ={
                "user_id":user_id,
                "email":data[11]
                }
            print(data[11])
            emailResult=SendEmail(otpParams)
            print(emailResult)
            user = UsersDtl()

            raw_password = make_password(data[12])
            user.user_id = user_id
            user.user_type = 'supplier'
            user.category_type = request.data['prod_type']
            user.password = raw_password
            user.email=data[11]
            user.phone=data[9]
            session.add(user)
            supplier=SupplierTable()
            supplier.user_id=user_id
            supplier.supplier_name=data[0]
            supplier.organization_name=data[2]
            supplier.org_started_year=data[1]
            supplier.prod_type=request.data['prod_type']
            supplier.prod_sub_type=request.data['sub_type']
            supplier.place=data[3]
            supplier.state=data[4]
            supplier.district=data[5]
            supplier.pincode=data[6]
            supplier.gst_number=data[7]
            supplier.udayam_number=data[8]
            supplier.phone_number=data[9]
            supplier.alternate_number=data[10]
            if request.data['is_companydeler']=='Yes':
                supplier.compnay_names=request.data['compnay_names']
                supplier.is_companydeler='Yes'
            else:
                supplier.is_companydeler='No'
            supplier.is_wholesaler=request.data['is_wholesaler']
            supplier.is_retailer=request.data['is_retailer']
            supplier.email=data[11]
            session.add(supplier)
            session.commit()
        if request.data['prod_type']=='Customized Uniforms' and request.data['sub_type']=='stitching':


            order_lines=json.dumps(request.data['order_lines'])
            user_id = getUserId('TS')
            otpParams ={
                "user_id":user_id,
                "email":data[11]
                }
            emailResult=SendEmail(otpParams)
            print(emailResult)
            user = UsersDtl()

            raw_password = make_password(data[12])
            user.user_id = user_id
            user.user_type = 'supplier'
            user.category_type = request.data['prod_type']
            user.password = raw_password
            user.email=data[11]
            user.phone=data[9]
            session.add(user)
            supplier=SupplierTable()
            supplier.user_id=user_id
            supplier.supplier_name=data[0]
            supplier.organization_name=data[2]
            supplier.org_started_year=data[1]
            supplier.prod_type=request.data['prod_type']
            supplier.prod_sub_type=request.data['sub_type']
            supplier.place=data[3]
            supplier.state=data[4]
            supplier.district=data[5]
            supplier.pincode=data[6]
            supplier.gst_number=data[7]
            supplier.udayam_number=data[8]
            supplier.phone_number=data[9]
            supplier.alternate_number=data[10]
            supplier.email=data[11]
            supplier.company_undertaking=request.data['company_undertaking']
            supplier.no_labours=request.data['no_labours']
            supplier.male_number=request.data['male_number']
            supplier.female_number=request.data['female_number']
            session.add(supplier)
            session.commit()
            #session.flush()
            for x in json.loads(order_lines):
                production_dtls=SupplierProductionDtl()
                production_dtls.item_name=x['item']
                production_dtls.item_count=x['count']
                production_dtls.sid=supplier.sid
                session.add(production_dtls)
                session.commit()
        if request.data['prod_type']=='Customized Uniforms' and request.data['sub_type']=='fabricandstitching':
            user_id = getUserId('FT')
            otpParams ={
                "user_id":user_id,
                "email":data[11]
                }
            emailResult=SendEmail(otpParams)
            print(emailResult)
            order_lines=json.dumps(request.data['order_lines'])
            user = UsersDtl()

            raw_password = make_password(data[12])
            user.user_id = user_id
            user.user_type = 'supplier'
            user.category_type = request.data['prod_type']
            user.password = raw_password
            user.email=data[11]
            user.phone=data[9]
            session.add(user)
            supplier=SupplierTable()
            supplier.user_id=user_id
            supplier.supplier_name=data[0]
            supplier.organization_name=data[2]
            supplier.org_started_year=data[1]
            supplier.prod_type=request.data['prod_type']
            supplier.prod_sub_type=request.data['sub_type']
            supplier.place=data[3]
            supplier.state=data[4]
            supplier.district=data[5]
            supplier.pincode=data[6]
            supplier.gst_number=data[7]
            supplier.udayam_number=data[8]
            supplier.phone_number=data[9]
            supplier.alternate_number=data[10]
            supplier.email=data[11]
            if request.data['is_companydeler']=='Yes':
                supplier.compnay_names=request.data['compnay_names']
                supplier.is_companydeler='Yes'
            else:
                supplier.is_companydeler='No'


            supplier.company_undertaking=request.data['company_undertaking']
            supplier.no_labours=request.data['no_labours']
            supplier.male_number=request.data['male_number']
            supplier.female_number=request.data['female_number']
            session.add(supplier)
            session.flush()
            for x in json.loads(order_lines):
                production_dtls=SupplierProductionDtl()
                production_dtls.item_name=x['item']
                production_dtls.item_count=x['count']
                production_dtls.sid=supplier.sid
                session.add(production_dtls)
                session.commit()
            session.commit()
        if request.data['prod_type']=='Ready Made Uniforms':
            print("REady")
            user_id = getUserId('RM')
            otpParams ={
                "user_id":user_id,
                "email":data[11]
                }
            emailResult=SendEmail(otpParams)
            print(emailResult)
            user = UsersDtl()

            raw_password = make_password(data[12])
            user.user_id = user_id
            user.user_type = 'supplier'
            user.category_type = request.data['prod_type']
            user.password = raw_password
            user.email=data[11]
            user.phone=data[9]
            session.add(user)
            supplier=SupplierTable()
            supplier.user_id=user_id
            supplier.supplier_name=data[0]
            supplier.organization_name=data[2]
            supplier.org_started_year=data[1]
            supplier.prod_type=request.data['prod_type']
            supplier.prod_sub_type=request.data['sub_type']
            supplier.place=data[3]
            supplier.state=data[4]
            supplier.district=data[5]
            supplier.pincode=data[6]
            supplier.gst_number=data[7]
            supplier.udayam_number=data[8]
            supplier.phone_number=data[9]
            supplier.alternate_number=data[10]
            supplier.email=data[11]
            supplier.readymade_providng_items=request.data['readymade_providng_items'] 
            session.add(supplier)
            session.commit()
        if request.data['prod_type']=='Uniform Accessories':
            user_id = getUserId('AS')
            otpParams ={
            "user_id":user_id,
            "email":data[11]
            }
            emailResult=SendEmail(otpParams)
            print(emailResult)
            
            user = UsersDtl()

            raw_password = make_password(data[12])
            user.user_id = user_id
            user.user_type = 'supplier'
            user.category_type = request.data['prod_type']
            user.password = raw_password
            user.email=data[11]
            user.phone=data[9]
            session.add(user)
            supplier=SupplierTable()
            supplier.user_id=user_id
            supplier.supplier_name=data[0]
            supplier.organization_name=data[2]
            supplier.org_started_year=data[1]
            supplier.prod_type=request.data['prod_type']
            supplier.prod_sub_type=request.data['sub_type']
            supplier.place=data[3]
            supplier.state=data[4]
            supplier.district=data[5]
            supplier.pincode=data[6]
            supplier.gst_number=data[7]
            supplier.udayam_number=data[8]
            supplier.phone_number=data[9]
            supplier.alternate_number=data[10]
            supplier.email=data[11]
            supplier.Providing_accesoseries=request.data['providing_accesoseries']
            session.add(supplier)
            session.commit()
                
            if(emailResult == True):
                session.commit()
                session.close()

        session.close()
        return Response({'response': 'Data saved success fully'})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def SaveSuppliertempdetails(request):
    try:
        session = dbsession.Session()
        supplier=SupplierTempDtl()
        supplier.name=request.data['supplier_name']
        supplier.comapny_name=request.data['organization_name']
        supplier.start_year=request.data['org_started_year']
        supplier.place=request.data['place']
        supplier.state=request.data['state']
        supplier.district=request.data['districtl']
        supplier.pincode=request.data['pincode']
        supplier.gst_number	=request.data['gst_number']
        supplier.udayam_number=request.data['udayam_number']
        supplier.phone_number=request.data['phone_number']
        supplier.alt_phone_number=request.data['alternate_number']
        supplier.email=request.data['email']
        supplier.password=request.data['password']
        session.add(supplier)
        session.commit()
        tempID=session.query(SupplierTempDtl.temp_id).filter(SupplierTempDtl.temp_id==supplier.temp_id).one()
        tempID_dtls_list = json.loads(json.dumps(tempID, cls=AlchemyEncoder))
        session.close()
        return Response({'response': 'success','delete_id':tempID_dtls_list[0]})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})


@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def prod_dtls_save(request):
    try:

        print(request.data)
        session = dbsession.Session()
        prod_id=request.data['prod_id']
        print(request.data.getlist('file')[0]=='undefined')
        print(request.data.getlist('file')[0])
        # if request.FILES['file']!='undefined':
        #     myfile=request.FILES['file']
        
        if prod_id:
            print(":=========")
            product=session.query(ProductDtl).filter(ProductDtl.prod_id==prod_id).one()
        else:
            product=ProductDtl()

        product.item_name=request.data['item_name']
        product.item_code=request.data['item_code']
        product.size=request.data['size']
        if request.data.getlist('file')[0]!='undefined':
            for f in request.data.getlist('file'):
                fs=FileSystemStorage()
                filename=fs.save(f.name,f)
                uploaded_file_url = fs.url(filename)
                product.image=uploaded_file_url
        product.price=request.data['price']
        product.quantity=request.data['quantity']
        product.status=request.data['status']
        product.user_id=request.data['user_id']
        product.prod_type=request.data['prod_type']
        product.prod_desc=request.data['prod_desc']
        product.condition=request.data['condition']
        product.shades=request.data['brand_name']
        session.add(product)
        session.commit()
        session.close()
        return Response({'response': 'success'})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})
@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def delete_prod_dtls(request):
    try:
        session = dbsession.Session()
        prod_id=request.data['prod_id']
        if prod_id:
            product=session.query(ProductDtl).filter(ProductDtl.prod_id==prod_id).delete()
            session.commit()
            session.close()
            return Response({'response': 'success'})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

# class getlabours_technisions_list(APIView):
#     def post(self, request):
#         try:
#             session = dbsession.Session()
#             sql = text('SELECT * from labors_technisions')
#             prod_list = session.execute(sql).fetchall()
#             product_dtls_list = [dict(row) for row in prod_list]
#             session.commit()
#             session.close()
#             return Response({'response': 'success',"product_dtls_list":product_dtls_list})
#         except SQLAlchemyError as e:
#             print(e)
#             session.rollback()
#             session.close()
#             return Response({'response': 'Error occured'})
@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def getlabours_technisions_list(request):
    try:
        session = dbsession.Session()
        sql = text('SELECT * from labors_technisions')
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        session.commit()
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def getmachneries_spareparts_list(request):
    try:
        session = dbsession.Session()
        sql = text('SELECT * from machines_spareparts')
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})










# class getmachneries_spareparts_list(APIView):
#     permission_classes = (IsAuthenticated, )
#     authentication_classes = (TokenAuthentication, )
#     def post(self, request):
#         try:
#             session = dbsession.Session()
#             sql = text('SELECT * from machines_spareparts')
#             prod_list = session.execute(sql).fetchall()
#             product_dtls_list = [dict(row) for row in prod_list]
#             session.close()
#             return Response({'response': 'success',"product_dtls_list":product_dtls_list})
#         except SQLAlchemyError as e:
#             print(e)
#             session.rollback()
#             session.close()
#             return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def get_prod_list(request):
    try:
        print(request)
        prod_type=request.data['prod_type']
        user_id=request.data['user_id']
        session = dbsession.Session()
        sql = text('SELECT * from product_dtls where user_id="'+user_id+'" and prod_type="'+prod_type+'"')
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def prod_list_byid(request):
    try:
        print(request)
        prod_id=request.data['prod_id']
        user_id=request.data['user_id']
        session = dbsession.Session()
        if user_id:
            sql = text('SELECT * from product_dtls where user_id="'+user_id+'" and prod_id="'+prod_id+'"')
            prod_list = session.execute(sql).fetchall()
            product_dtls_list = [dict(row) for row in prod_list]
            session.close()
        else:
            sql = text('SELECT * from product_dtls where prod_id="'+prod_id+'"')
            prod_list = session.execute(sql).fetchall()
            product_dtls_list = [dict(row) for row in prod_list]
            session.close()

        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})



@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def supplier_list(request):
    try:
        session = dbsession.Session()
        user_id = request.data['user_id']
        sql = text('SELECT email,phone_number,prod_type,prod_sub_type from supplier_table where user_id="'+user_id+'"')
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})
@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def productSupplideerlst(request):
    try:
        session = dbsession.Session()
        order_id=request.data['order_id']
        sub_type=request.data['type']
       
        sql = text('SELECT * from customer_order_dtls where order_id="'+order_id+'" and prod_sub_type="'+sub_type+'"' )
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def customer_requirements(request):
    try:
        session = dbsession.Session()
        order_id=request.data['order_id']
       
        sql = text('SELECT * from customer_add_product_dtls where order_id="'+order_id+'"')
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})


@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def prod_list_cat(request):
    session = dbsession.Session()
    user_id = request.GET.get('user_id') 
    try:
        session = dbsession.Session()
        # sql = text('SELECT * from product_dtls')
        # prod_list = session.execute(sql).fetchall()
        # product_dtls_list = [dict(row) for row in prod_list]

        # sql = text('SELECT * from supplier_table')
        # supplier_list = session.execute(sql).fetchall()
        # supplier_details_list = [dict(row) for row in supplier_list]
        # session.close()


        # session.close()
        # return Response({'response': 'success',"product_dtls_list":product_dtls_list,"supplier_details_list":supplier_details_list})
        columns =['organization_name','place','state','district','phone_number','item_name','image','price','status','prod_type','prod_id']
        cart_list = session.query(SupplierTable.organization_name, SupplierTable.place,SupplierTable.state,SupplierTable.district,SupplierTable.phone_number,ProductDtl.item_name,ProductDtl.image,ProductDtl.price,ProductDtl.status,ProductDtl.prod_type,ProductDtl.prod_id).join(ProductDtl, SupplierTable.user_id == ProductDtl.user_id).all()
        print(cart_list)
        cart_list = json.dumps(cart_list, cls=AlchemyEncoder)
        cart_list = pd.read_json(cart_list)
        if columns:
            cart_list.columns = columns
            cart_list = cart_list.to_json(orient='records')
        
        session.close()
        return Response({'response': 'Success', 'cart_list': json.loads(cart_list)})
    except SQLAlchemyError as e:
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})





@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def orders_enquiries(request):
    try:
        # product_type=request.data['product_type']
        # prod_sub_type=request.data['prod_sub_type']
        session = dbsession.Session()
        sql = text("select customer_dtls.user_id,customer_dtls.pincode,customer_order_dtls.order_id,customer_order_dtls.product_type, customer_order_dtls.category_type,customer_order_dtls.prod_sub_type,customer_order_dtls.photo,customer_order_dtls.delivery_date from  customer_order_dtls join customer_dtls on customer_order_dtls.user_id=customer_dtls.user_id  where product_type NOT IN('ReadyMade Uniforms')")
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        sql = text("SELECT * from customer_dtls")
        cust_list = session.execute(sql).fetchall()
        cust_dtls_list = [dict(row) for row in cust_list]
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list,"cust_dtls_list":cust_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def users_list(request):
    try:
        # product_type=request.data['product_type']
        # prod_sub_type=request.data['prod_sub_type']
        session = dbsession.Session()
        sql = text("SELECT * from users_dtls where status IS  NULL and user_type='supplier'")
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def supplier_details(request):
    try:
        # product_type=request.data['product_type']
        # prod_sub_type=request.data['prod_sub_type']
        user_id = request.data['user_id']
        session = dbsession.Session()
        sql = text('SELECT * from supplier_table where user_id="'+user_id+'"')
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

def SendConform(params):
    
    ctx={
        'OTP':params['user_id']
    }
    plaintext = get_template('mail.txt')
    htmly     = get_template('conform.html')
    subject, from_email, to = 'Hello from Uniconform', 'anjujoy0310@gmail.com', params['email']
    text_content = plaintext.render(ctx)
    html_content = htmly.render(ctx)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    res=msg.send(fail_silently=False)
    
    if(res==1):
        return True
    else:
        return False
@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def accept_supplier(request):
    try:
        # product_type=request.data['product_type']
        # prod_sub_type=request.data['prod_sub_type']
        user_id = request.data['user_id']
        print(user_id)
        session = dbsession.Session()
        email=session.query(UsersDtl.email,UsersDtl.user_id).filter(UsersDtl.user_id==user_id).one()
        print(email[0])
        params={
            "email":email[0],
            "user_id":user_id
        }
        emailresult=SendConform(params)
        session.query(UsersDtl).filter(UsersDtl.user_id==user_id).update({'status':'login'})
        session.commit()
        session.close()
        return Response({'response': 'success'})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def getProfile(request):
    try:
        # product_type=request.data['product_type']
        # prod_sub_type=request.data['prod_sub_type']
        user_id = request.data['user_id']
        print(user_id)
        session = dbsession.Session()
        email=session.query(UsersDtl.user_id,UsersDtl.phone).filter(UsersDtl.user_id==user_id).one()
        print(email)
        session.commit()
        session.close()
        return Response({'response': 'success','phone_no':email[1],'user_id':email[0]})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})


def SendEmail(params):
    
    ctx={
        'OTP':params['user_id']
    }
    plaintext = get_template('mail.txt')
    htmly     = get_template('mail.html')
    subject, from_email, to = 'Hello from Uniconform', 'anjujoy0310@gmail.com', params['email']
    text_content = plaintext.render(ctx)
    html_content = htmly.render(ctx)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    res=msg.send(fail_silently=False)
    
    if(res==1):
        return True
    else:
        return False


@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def Email(request):
    try:
        ctx={
        'PhoneNumber':request.data['phone_numer'],
        'Message':request.data['message'],
        'CompanyName':request.data['org_name'],
        'Name':request.data['name']
        }
        plaintext = get_template('mail.txt')
        htmly     = get_template('contact.html')
        subject, from_email, to = request.data['subject'], 'anjujoy0310@gmail.com', request.data['email']
        text_content = plaintext.render(ctx)
        html_content = htmly.render(ctx)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        res=msg.send(fail_silently=False)
        if(res==1):
            return True
        else:
            return False
   
        session.commit()
        session.close()
        return Response({'response': 'success','phone_no':email[1],'user_id':email[0]})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def Edit_profile(request):
    try:
        user_id = request.data['user_id']
        session = dbsession.Session()
        sql = text('SELECT * from users_dtls where user_id="'+user_id+'"')
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def save_profile(request):
    try:
        session = dbsession.Session()
        user_id = request.data['user_id']
        if usid:
            user=session.query(UsersDtl).filter(UsersDtl.usid==UsersDtl).one()
        else:
            user = UsersDtl()
        
        user.user_id=request.data['user_id']
        user.email=request.data['email']
        user.phone=request.data['phone']
        session.add()
        session.commit()
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})


@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def quotaton_form(request):
    try:
        session = dbsession.Session()
        user_id = request.data['user_id']

        order=QuotationTable()
        order.order_form_id=request.data['order_id']
        order.user_id=request.data['user_id']
        order.supplier_id=request.data['customer_id']
        order.total_amount=request.data['total_amount']
        order.grand_total=request.data['grand_total']
        order.quatation_form_id=getUserId(request.data['type'])
        order.category_type=request.data['model_type']
        order.prod_sub_type=request.data['prod_sub_type']
        order.prod_type=request.data['product_type']
        session.add(order)
        session.flush()
        for x in json.loads(request.data['order_lines']):
            addprod=QutationDtl()
            addprod.qutation_id=order.quotatit_id
            addprod.qutation_form_id=order.quatation_form_id
            addprod.item_name=x['item']
            addprod.count=x['count']
            addprod.rate_per_item=x['rate_per_meter']
            session.add(addprod)

        session.commit()
        session.close()
        return Response({'response': 'success'})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def quote_list(request):
    try:
        user_id = request.data['user_id']
        session = dbsession.Session()
        sql = text('select quotation_table.quotatit_id, quotation_table.order_form_id,quotation_table.user_id,quotation_table.supplier_id,quotation_table.grand_total,quotation_table.quatation_form_id,quotation_table.is_order_accepted,quotation_table.prod_type,quotation_table.prod_sub_type from quotation_table join qutation_dtls on quotation_table.quotatit_id=qutation_dtls.qutation_id where user_id="'+user_id+'"')
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def get_qouteditem(request):
    try:
        user_id = request.data['user_id']
        quote_id = request.data['quote_id']
        session = dbsession.Session()
        sql = text('SELECT * FROM quotation_table where quatation_form_id="'+quote_id+'" and user_id="'+user_id+'" ')
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        sql = text('SELECT * FROM qutation_dtls where qutation_form_id="'+quote_id+'"')
        quote_list = session.execute(sql).fetchall()
        quote_dtls_list = [dict(row) for row in quote_list]
        print(quote_dtls_list)
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list,"quote_dtls_list":quote_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def update_quotes(request):
    try:
        user_id = request.data['user_id']
        quote_id = request.data['quote_id']
        order_status=request.data['order_status']
        session = dbsession.Session()
        session.query(QuotationTable).filter(QuotationTable.quatation_form_id==quote_id,QuotationTable.user_id==user_id).update({'is_order_accepted':order_status})
        session.commit()
        session.close()
        return Response({'response': 'success'})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def buyers_list(request):
    try:
        
        session = dbsession.Session()
        sql = text('SELECT * FROM customer_dtls')
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def customer_details(request):
    try:
        user_id=request.data['user_id']
        session = dbsession.Session()
        sql = text('SELECT * FROM customer_dtls where user_id="'+user_id+'"')
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})


        

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def all_supplier_list(request):
    try:
        session = dbsession.Session()
        sql = text('SELECT * FROM supplier_table')
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def order_details(request):
    try:
        session = dbsession.Session()
        sql = text('SELECT * FROM customer_order_dtls')
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def all_quote_list(request):
    try:
        session = dbsession.Session()
        sql = text("select * from quotation_table where is_order_accepted='Accepted by supplier'")
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def quote_list_by_id(request):
    try:
        user_id = request.data['user_id']
        session = dbsession.Session()
        sql = text("select * from quotation_table where  is_order_accepted='Accepted Proposal' and supplier_id='"+user_id+"'")
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def pincode(request):
    try:
        session = dbsession.Session()
        sql = text(' select pincode from supplier_table')
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})


        



        















