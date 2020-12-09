from django.shortcuts import render
import json
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
from unicon.models import UsersDtl,CustomerDtl,SupplierTable,LaborsTechnision,MachinesSparepart,CustomerOrderDtl,CustomerAddProductDtl,CategoryDtl,SupplierTempDtl,SupplierProductionDtl,ProductDtl
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


class SaveCustomer(APIView):
    def post(self, request):
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
            user.user_type = request.data['user_type']
            user.category_type = request.data['category_type']
            user.password = raw_password
            user.email=email
            user.phone=phone
            session.add(user)
            if request.data['user_type']=='uniforms' and request.data['sub_type']=='customer':
                customer = CustomerDtl()
                customer.category_type=request.data['category_type']
                customer.user_id=user_id
                customer.customer_name=request.data['customer_name']
                customer.organization_name=request.data['organization_name']
                customer.designation=request.data['designation']
                customer.place=request.data['place']
                customer.state=request.data['state']
                customer.districtl=request.data['districtl']
                customer.pincode=request.data['pincode']
                customer.phone_number=request.data['phone_number']
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


class Authenticate(APIView):
    def post(self, request):
        try:
            session = dbsession.Session()
            user_id = request.data['user_id']
            password = request.data['password']

            user_data = get_user(user_id)
            if user_data == None:
                return Response({'response': 'Error','message':'Please provide a valid user name'})
            user = session.query(UsersDtl).filter(UsersDtl.user_id==user_id).one()
            if user.check_password(password):
                user.status='login'
                session.commit()
                if request.data['user_type']=='uniform' and request.data['sub_type']=='customer':
                    customer_dtls=session.query(CustomerDtl).filter(CustomerDtl.user_id==user_id).all()
                    if len(customer_dtls)==0:
                        return Response({'response': 'error','message':'user not found in the specified category'})
                    else:
                        customer_dtls_list = json.loads(json.dumps(customer_dtls, cls=AlchemyEncoder))
                        return Response({'response': 'success','data':customer_dtls_list,'type':'buyerandseller','category':'customer'})

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
            return Response({'response': 'Data saved success fully'})
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            session.close()
            return Response({'response': 'Error occured'})

class AddCustomerordes(APIView):
    def post(self, request):
        try:
            session = dbsession.Session()
            user_id = request.data['user_id']
            user_type=request.data['user_type']
            # myfile=request.FILES['file']
            if request.data['user_type']=='uniform' and request.data['sub_type']=='customer' and request.data['product_type']=='Customized Uniforms' and request.data['prod_sub_type']=='fabric':
                sql = text('SELECT MAX(CONVERT(REPLACE(order_id,"PF",""),UNSIGNED INTEGER)) as auto_order_id from customer_order_dtls')
                auto_order_id = session.execute(sql).fetchall()
                order_id = auto_order_id[0][0]
                if order_id == None or order_id == 0 :
                    order_id = 100000
                    order_id = 'PF' + str(int(order_id + 1))
                order=CustomerOrderDtl()
                # fs = FileSystemStorage()
                # filename = fs.save(myfile.name, myfile)
                # uploaded_file_url = fs.url(filename)
                # order.photo=uploaded_file_url
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
                session.commit()
                for x in request.data['product_list']:
                    addprod=CustomerAddProductDtl()
                    addprod.order_id=order.order_id
                    addprod.user_id=request.data['user_id']
                    addprod.name=x['item']
                    addprod.size=x['count']
                    session.add(addprod)
                session.commit()
                session.close()

            if request.data['user_type']=='uniform' and request.data['sub_type']=='customer' and request.data['product_type']=='Customized Uniforms' and request.data['prod_sub_type']=='stitching':
                sql = text('SELECT MAX(CONVERT(REPLACE(order_id,"PT",""),UNSIGNED INTEGER)) as auto_order_id from customer_order_dtls')
                auto_order_id = session.execute(sql).fetchall()
                order_id = auto_order_id[0][0]
                if order_id == None or order_id == 0 :
                    order_id = 100000
                    order_id = 'PT' + str(int(order_id + 1))
                order=CustomerOrderDtl()
                # fs = FileSystemStorage()
                # filename = fs.save(myfile.name, myfile)
                # uploaded_file_url = fs.url(filename)
                # order.photo=uploaded_file_url
                order.order_id=order_id
                order.user_id=request.data['user_id']
                order.product_type=request.data['product_type']
                order.prod_sub_type=request.data['prod_sub_type']
                order.category_type=request.data['model_type']
                order.photo=request.data['photo']
                order.delivery_date=request.data['delivery_date']
                order.message=request.data['message']
                order.is_invidulaystiched=request.data['stich_type']
                order.total_count=request.data['total_count']
                session.add(order)
                session.commit()
                return Response({'response': 'Data saved success fully'})
                for x in request.data['product_list']:
                    addprod=CustomerAddProductDtl()
                    addprod.order_id=order.order_id
                    addprod.user_id=request.data['user_id']
                    addprod.name=x['item']
                    addprod.size=x['count']
                    session.add(addprod)
                session.commit()
                session.close()
            if request.data['user_type']=='uniform' and request.data['sub_type']=='customer' and request.data['product_type']=='Customized Uniforms' and request.data['prod_sub_type']=='fabricandstitching':
                sql = text('SELECT MAX(CONVERT(REPLACE(order_id,"PS",""),UNSIGNED INTEGER)) as auto_order_id from customer_order_dtls')
                auto_order_id = session.execute(sql).fetchall()
                order_id = auto_order_id[0][0]
                if order_id == None or order_id == 0 :
                    order_id = 100000
                    order_id = 'PS' + str(int(order_id + 1))
                order=CustomerOrderDtl()
                # fs = FileSystemStorage()
                # filename = fs.save(myfile.name, myfile)
                # uploaded_file_url = fs.url(filename)
                # order.photo=uploaded_file_url
                order.order_id=order_id
                order.user_id=request.data['user_id']
                order.product_type=request.data['product_type']
                order.prod_sub_type=request.data['prod_sub_type']
                order.category_type=request.data['model_type']
                order.brand_name=request.data['brand_name']
                order.catalog_number=request.data['catalog_number']
                order.design_no=request.data['design_no']
                order.photo=request.data['photo']
                order.sahde_no=request.data['shade_no']
                order.delivery_date=request.data['delivery_date']
                order.message=request.data['message']
                order.is_invidulaystiched=request.data['stich_type']
                order.total_count=request.data['total_count']
                session.add(order)
                session.commit()
                for x in request.data['product_list']:
                    addprod=CustomerAddProductDtl()
                    addprod.order_id=order.order_id
                    addprod.user_id=request.data['user_id']
                    addprod.name=x['item']
                    addprod.size=x['count']
                    session.add(addprod)
                session.commit()
                session.close()
            if request.data['user_type']=='uniform' and request.data['sub_type']=='customer' and request.data['product_type']=='ReadyMade Uniforms' and request.data['prod_sub_type']=='OrderBasedForm':
                order=CustomerOrderDtl()
                sql = text('SELECT MAX(CONVERT(REPLACE(order_id,"PR",""),UNSIGNED INTEGER)) as auto_order_id from customer_order_dtls')
                auto_order_id = session.execute(sql).fetchall()
                order_id = auto_order_id[0][0]
                if order_id == None or order_id == 0 :
                    order_id = 100000
                    order_id = 'PR' + str(int(order_id + 1))
                # fs = FileSystemStorage()
                # filename = fs.save(myfile.name, myfile)
                # uploaded_file_url = fs.url(filename)
                # order.photo=uploaded_file_url
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
                for x in request.data['product_list']:
                    addprod=CustomerAddProductDtl()
                    addprod.order_id=order.order_id
                    addprod.user_id=request.data['user_id']
                    addprod.name=x['item']
                    addprod.size=x['count']
                    session.add(addprod)
                session.commit()
                session.close()
            if request.data['user_type']=='uniform' and request.data['sub_type']=='customer' and request.data['product_type']=='ReadyMade Uniforms' and request.data['prod_sub_type']=='StockBasedList':
                sql = text('SELECT MAX(CONVERT(REPLACE(order_id,"PR",""),UNSIGNED INTEGER)) as auto_order_id from customer_order_dtls')
                auto_order_id = session.execute(sql).fetchall()
                order_id = auto_order_id[0][0]
                if order_id == None or order_id == 0 :
                    order_id = 100000
                    order_id = 'PR' + str(int(order_id + 1)) 
                order=CustomerOrderDtl()
                # fs = FileSystemStorage()
                # filename = fs.save(myfile.name, myfile)
                # uploaded_file_url = fs.url(filename)
                # order.photo=uploaded_file_url
                order.order_id=order_id
                order.user_id=request.data['user_id']
                order.product_type=request.data['product_type']
                order.prod_sub_type=request.data['prod_sub_type']
                order.category_type=request.data['model_type']
                order.delivery_date=request.data['delivery_date']
                order.message=request.data['message']
                session.add(order)
                session.commit()
                for x in request.data['product_list']:
                    addprod=CustomerAddProductDtl()
                    addprod.order_id=order.order_id
                    addprod.user_id=request.data['user_id']
                    addprod.name=x['item']
                    addprod.size=x['count']
                    session.add(addprod)
                session.commit()
                session.close()
            if request.data['user_type']=='uniform' and request.data['sub_type']=='customer' and request.data['product_type']=='Uniform Accesories' and request.data['prod_sub_type']=='none':
                sql = text('SELECT MAX(CONVERT(REPLACE(order_id,"AC",""),UNSIGNED INTEGER)) as auto_order_id from customer_order_dtls')
                auto_order_id = session.execute(sql).fetchall()
                order_id = auto_order_id[0][0]
                print(order_id)
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
                session.commit()
                for x in request.data['product_list']:
                    addprod=CustomerAddProductDtl()
                    addprod.order_id=order.order_id
                    addprod.user_id=request.data['user_id']
                    addprod.name=x['item']
                    addprod.size=x['count']
                    session.add(addprod)
                session.commit()
                session.close()
            session.close()   
            return Response({'response': 'Data saved success fully'})
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            session.close()
            return Response({'response': 'Error occured'})

class SaveLabours(APIView):
    def post(self, request):
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
            user.user_type = request.data['user_type']
            user.category_type = request.data['category_type']
            user.password = raw_password
            user.email=email
            user.phone=phone
            session.add(user)
            if request.data['user_type']=='other' and request.data['sub_type']=='Labours':
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
                labors.status=request.data['status']
                session.add(labors)
                session.commit()

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

class SaveMachiners(APIView):
    def post(self, request):
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
            user.user_type = request.data['user_type']
            user.category_type = request.data['category_type']
            user.password = raw_password
            user.email=email
            user.phone=phone
            session.add(user)
            if request.data['user_type']=='other' and request.data['sub_type']=='Machines':
                machine=MachinesSparepart()
                machine.user_id=user_id
                machine.customer_name=request.data['customer_name']
                machine.designation=request.data['designation']
                machine.adress=request.data['adress']
                machine.place=request.data['place']
                machine.state=request.data['state']
                machine.districtl=request.data['districtl']
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

class getCategories(APIView):
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

class SaveSupplier(APIView):
    def post(self, request):
        try:
            session = dbsession.Session()
            email=request.data['email']
            phone=request.data['phone_number']
            delete_id=request.data['delete_id']
            session.query(SupplierTempDtl).filter(SupplierTempDtl.temp_id==delete_id).delete()

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
                "email":email
                }
                emailResult=SendEmail(otpParams)
                print(emailResult)
                user = UsersDtl()

                raw_password = make_password(request.data['password'])
                user.user_id = user_id
                user.user_type = 'supplier'
                user.category_type = request.data['prod_type']
                user.password = raw_password
                user.email=email
                user.phone=phone
                session.add(user)
                supplier=SupplierTable()
                supplier.user_id=user_id
                supplier.supplier_name=request.data['supplier_name']
                supplier.organization_name=request.data['organization_name']
                supplier.org_started_year=request.data['org_started_year']
                supplier.prod_type=request.data['prod_type']
                supplier.prod_sub_type=request.data['sub_type']
                supplier.place=request.data['place']
                supplier.state=request.data['state']
                supplier.district=request.data['district']
                supplier.pincode=request.data['pincode']
                supplier.gst_number=request.data['gst_number']
                supplier.udayam_number=request.data['udayam_number']
                supplier.phone_number=request.data['phone_number']
                supplier.alternate_number=request.data['alternate_number']
                if request.data['is_companydeler']=='Yes':
                    supplier.compnay_names=request.data['compnay_names']
                    request.is_companydeler='Yes'
                else:
                    request.is_companydeler='No'
                supplier.is_wholesaler=request.data['is_wholesaler']
                supplier.is_retailer=request.data['is_retailer']
                supplier.email=request.data['email']
                session.add(supplier)
                session.commit()
            if request.data['prod_type']=='Customized Uniforms' and request.data['sub_type']=='stitching':
                user_id = getUserId('TS')
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
                user.category_type = request.data['prod_type']
                user.password = raw_password
                user.email=email
                user.phone=phone
                session.add(user)
                supplier=SupplierTable()
                supplier.user_id=user_id
                supplier.supplier_name=request.data['supplier_name']
                supplier.organization_name=request.data['organization_name']
                supplier.org_started_year=request.data['org_started_year']
                supplier.prod_type=request.data['prod_type']
                supplier.prod_sub_type=request.data['sub_type']
                supplier.place=request.data['place']
                supplier.state=request.data['state']
                supplier.district=request.data['district']
                supplier.pincode=request.data['pincode']
                supplier.gst_number=request.data['gst_number']
                supplier.udayam_number=request.data['udayam_number']
                supplier.phone_number=request.data['phone_number']
                supplier.alternate_number=request.data['alternate_number']
                supplier.email=request.data['email']
                supplier.company_undertaking=request.data['company_undertaking']
                supplier.no_labours=request.data['no_labours']
                supplier.male_number=request.data['male_number']
                supplier.female_number=request.data['female_number']
                session.add(supplier)
                session.commit()
                session.flush()
                for x in request.data['product_list']:
                    production_dtls=SupplierProductionDtl()
                    production_dtls.item_name=x['item_name']
                    production_dtls.item_count=x['item_count']
                    production_dtls.sid=supplier.sid
                    session.add(production_dtls)
                session.commit()
            if request.data['prod_type']=='Customized Uniforms' and request.data['sub_type']=='fabricandstitching':
                user_id = getUserId('FT')
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
                user.category_type = request.data['prod_type']
                user.password = raw_password
                user.email=email
                user.phone=phone
                session.add(user)
                supplier=SupplierTable()
                supplier.user_id=user_id
                supplier.supplier_name=request.data['supplier_name']
                supplier.organization_name=request.data['organization_name']
                supplier.org_started_year=request.data['org_started_year']
                supplier.prod_type=request.data['prod_type']
                supplier.prod_sub_type=request.data['sub_type']
                supplier.place=request.data['place']
                supplier.state=request.data['state']
                supplier.district=request.data['district']
                supplier.pincode=request.data['pincode']
                supplier.gst_number=request.data['gst_number']
                supplier.udayam_number=request.data['udayam_number']
                supplier.phone_number=request.data['phone_number']
                supplier.alternate_number=request.data['alternate_number']
                supplier.email=request.data['email']
                if request.data['is_companydeler']=='yes':
                    supplier.compnay_names=request.data['compnay_names']
                supplier.is_wholesaler=request.data['is_wholesaler']
                supplier.is_retailer=request.data['is_retailer']
                supplier.company_undertaking=request.data['company_undertaking']
                supplier.no_labours=request.data['no_labours']
                supplier.male_number=request.data['male_number']
                supplier.female_number=request.data['female_number']
                session.add(supplier)
                session.flush()
                for x in request.data['product_list']:
                    production_dtls=SupplierProductionDtl()
                    production_dtls.item_name=x['item_name']
                    production_dtls.item_count=x['item_count']
                    production_dtls.sid=supplier.sid
                    session.add(production_dtls)
                session.commit()
            if request.data['prod_type']=='Ready Made Uniforms':
                user_id = getUserId('RM')
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
                user.category_type = request.data['prod_type']
                user.password = raw_password
                user.email=email
                user.phone=phone
                session.add(user)
                supplier=SupplierTable()
                supplier.user_id=user_id
                supplier.supplier_name=request.data['supplier_name']
                supplier.organization_name=request.data['organization_name']
                supplier.org_started_year=request.data['org_started_year']
                supplier.prod_type=request.data['prod_type']
                supplier.place=request.data['place']
                supplier.state=request.data['state']
                supplier.district=request.data['district']
                supplier.pincode=request.data['pincode']
                supplier.gst_number=request.data['gst_number']
                supplier.udayam_number=request.data['udayam_number']
                supplier.phone_number=request.data['phone_number']
                supplier.alternate_number=request.data['alternate_number']
                supplier.email=request.data['email']
                supplier.readymade_providng_items=request.data['readymade_providng_items']
                
                session.add(supplier)
                session.commit()
            if request.data['prod_type']=='Uniform Accessories':
                user_id = getUserId('AS')
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
                user.category_type = request.data['prod_type']
                user.password = raw_password
                user.email=email
                user.phone=phone
                session.add(user)
                supplier=SupplierTable()
                supplier.user_id=user_id
                supplier.supplier_name=request.data['supplier_name']
                supplier.organization_name=request.data['organization_name']
                supplier.org_started_year=request.data['org_started_year']
                supplier.prod_type=request.data['prod_type']
                supplier.place=request.data['place']
                supplier.state=request.data['state']
                supplier.district=request.data['district']
                supplier.pincode=request.data['pincode']
                supplier.gst_number=request.data['gst_number']
                supplier.udayam_number=request.data['udayam_number']
                supplier.phone_number=request.data['phone_number']
                supplier.alternate_number=request.data['alternate_number']
                supplier.email=request.data['email']
                supplier.Providing_accesoseries=request.data['Providing_accesoseries']
                session.add(supplier)
                session.commit()

                
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

class SaveSuppliertempdetails(APIView):
    def post(self, request):
        try:
            session = dbsession.Session()
            supplier=SupplierTempDtl()
            supplier.name=request.data['supplier_name']
            supplier.comapny_name=request.data['organization_name']
            supplier.start_year=request.data['org_started_year']
            supplier.place=request.data['place']
            supplier.state=request.data['state']
            supplier.district=request.data['district']
            supplier.pincode=request.data['pincode']
            supplier.gst_number	=request.data['gst_number']
            supplier.udayam_number=request.data['udayam_number']
            supplier.phone_number=request.data['phone_number']
            supplier.alt_phone_number=request.data['alternate_number']
            supplier.email=request.data['email']
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


class prod_dtls_save(APIView):
    def post(self, request):
        try:
            session = dbsession.Session()
            prod_id=request.data['prod_id']
            if prod_id:
                product=session.query(ProductDtl).filter(ProductDtl.prod_id==prod_id).one()
            else:
                product=ProductDtl()

            product.item_name=request.data['item_name']
            product.item_code=request.data['item_code']
            product.size=request.data['size']
            product.image=request.data['image']
            product.shades=request.data['shades']
            product.price=request.data['price']
            product.quantity=request.data['quantity']
            product.status=request.data['status']
            product.user_id=request.data['user_id']
            product.prod_type=request.data['prod_type']
            session.add(product)
            session.commit()
            session.close()
            return Response({'response': 'success'})
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            session.close()
            return Response({'response': 'Error occured'})

class delete_prod_dtls(APIView):
    def post(self, request):
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

class getlabours_technisions_list(APIView):
    def post(self, request):
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

class getmachneries_spareparts_list(APIView):
    def post(self, request):
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









