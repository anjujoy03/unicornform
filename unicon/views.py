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
from unicon.models import UsersDtl,CustomerDtl,SupplierTable,LaborsTechnision,MachinesSparepart
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
	number = '{:04d}'.format(random.randrange (1,999))
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
		email_txt = email.split("@")[0]
		email_txt = email_txt[0:3]
		user_id = generateUserId(email_txt)
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
    subject, from_email, to = 'Hello from UnicornForm', 'anjujoy0310@gmail.com', params['email']
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
            phno_check = session.query(UsersDtl).filter(UsersDtl.phone==phone).all()
            if(len(phno_check) > 0):
                return Response({'status': 'phone num exists','message':'phone num already exists'})
            email_check = session.query(UsersDtl).filter(UsersDtl.email==email).all()
            if(len(email_check) > 0):
                return Response({'status': 'email  exists','message':'email already exists'})

            user_id = getUserId(email)
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
            if request.data['user_type']=='buyer' and request.data['category_type']=='customer':
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
                customer.prouduct_type=request.data['uniform_type']
                session.add(customer)
                session.commit()
            if request.data['user_type']=='buyer' and request.data['category_type']=='supplier':
                supplier=SupplierTable()
                supplier.user_id=user_id
                supplier.supplier_name=request.data['supplier_name']
                supplier.organization_name=request.data['organization_name']
                supplier.org_started_year=request.data['org_started_year']
                supplier.place=request.data['place']
                supplier.state=request.data['state']
                supplier.district=request.data['district']
                supplier.pincode=request.data['pincode']
                supplier.gst_number=request.data['gst_number']
                supplier.udayam_number=request.data['udayam_number']
                supplier.phone_number=request.data['phone_number']
                supplier.alternate_number=request.data['alternate_number']
                supplier.email=request.data['email']
                session.add(supplier)
                session.commit()
            if request.data['user_type']=='other' and request.data['category_type']=='Machines':
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
            if request.data['user_type']=='other' and request.data['category_type']=='Labours':
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
            user_type=request.data['user_type']
            category_type=request.data['category_type']

            user_data = get_user(user_id)
            if user_data == None:
                return Response({'response': 'Error','message':'Please provide a valid user name'})
            user = session.query(UsersDtl).filter(UsersDtl.user_id==user_id).one()
            print(user)
            if user.check_password(password):
                user.status='login'
                session.commit()
                if request.data['user_type']=='buyer' and request.data['category_type']=='customer':
                    customer_dtls=session.query(CustomerDtl).filter(CustomerDtl.user_id==user_id).all()
                    if len(customer_dtls)==0:
                        return Response({'response': 'error','message':'user not found in the specified category'})
                    else:
                        customer_dtls_list = json.loads(json.dumps(customer_dtls, cls=AlchemyEncoder))
                        return Response({'response': 'success','data':customer_dtls_list,'type':'buyerandseller','category':'customer'})

                if request.data['user_type']=='buyer' and request.data['category_type']=='supplier':
                    customer_dtls=session.query(SupplierTable).filter(SupplierTable.user_id==user_id).all()
                   
                    if len(customer_dtls)==0:
                        return Response({'response': 'error','message':'user not found in the specified category'})
                    else:
                        customer_dtls_list = json.loads(json.dumps(customer_dtls, cls=AlchemyEncoder))
                        return Response({'response': 'success','data':customer_dtls_list,'type':'buyerandseller','category':'supplier'})

                if request.data['user_type']=='other' and request.data['category_type']=='Machines':
                    customer_dtls=session.query(MachinesSparepart).filter(MachinesSparepart.user_id==user_id).all()
                    if len(customer_dtls)==0:
                        return Response({'response': 'error','message':'user not found in the specified category'})
                    else:
                        customer_dtls_list = json.loads(json.dumps(customer_dtls, cls=AlchemyEncoder))
                        return Response({'response': 'success','data':customer_dtls_list,'type':'Machinesandspareparts','category':'none'})
                   
                if request.data['user_type']=='other' and request.data['category_type']=='Labours':
                    customer_dtls=session.query(LaborsTechnision).filter(LaborsTechnision.user_id==user_id).all()
                    if len(customer_dtls)==0:
                        return Response({'response': 'error','message':'user not found in the specified category'})
                    else:
                        customer_dtls_list = json.loads(json.dumps(customer_dtls, cls=AlchemyEncoder))
                        return Response({'response': 'success','data':customer_dtls_list,'type':'Labours','category':'none'})
            
            else:
                return Response({'response': 'Error','message':'Please provide a valid credentails'})

            


            
            session.close()
            return Response({'response': 'Data saved success fully'})
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            session.close()
            return Response({'response': 'Error occured'})


