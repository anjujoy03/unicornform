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
from unicon.models import UsersDtl,CustomerDtl,SupplierTable,LaborsTechnision,MachinesSparepart,CustomerOrderDtl,CustomerAddProductDtl,CategoryDtl,SupplierTempDtl,SupplierProductionDtl,ProductDtl,AuthToken,QuotationTable,QutationDtl,BannerTable
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
import requests
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
import weasyprint
from io import BytesIO
import boto3
import logging
import time
from botocore.exceptions import ClientError
from uniconform.simpleSms import SnsWrapper





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
    subject, from_email, to = 'Hello from Uniconform', 'admin@uniconform.in', params['email']
    text_content = plaintext.render(ctx)
    html_content = htmly.render(ctx)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    res=msg.send(fail_silently=False)
    
    if(res==1):
        return True
    else:
        return False


def Sms(params):

    # SMS=SnsWrapper.publish_text_message('',"+91"+params['rece_mobile_no'],params['otp_val']+'is Your verification code for Uniconform')
    # print(SMS)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    session = boto3.Session(
    region_name="us-east-2"
    )
    sns_client = session.client('sns',
    aws_access_key_id = "AKIAWUJKMYVN32GPHB5V",
    aws_secret_access_key = "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",
    region_name = "us-east-2"
    )
    response = sns_client.publish(
        PhoneNumber="+91 7012433842",
        Message='Hi there! This is a test message sent with Amazon SNS',
        MessageAttributes={
            'AWS.SNS.SMS.SenderID': {
                'DataType': 'String',
                'StringValue': 'SENDERID'
            },
            'AWS.SNS.SMS.SMSType': {
                'DataType': 'String',
                'StringValue': 'Promotional'
            }
        }
    )
    logger.info(response)
    print(response)
    return 'OK'


    
    
#     SENDER_ID = "UNIFORM"
#     SMS_MOBILE = "+91"+params['rece_mobile_no']
#     SMS_MESSAGE = params['otp_val']+'is Your verification code for Uniconform'
#     client = boto3.client(
#         "sns",
#         aws_access_key_id=AWS_ACCESS_KEY_ID,
#         aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#         region_name=AWS_REGION_NAME
#         )
#     response = client.publish(
#     PhoneNumber=SMS_MOBILE,
#     Message=SMS_MESSAGE,
#     MessageAttributes={
#         'string': {
#             'DataType': 'String',
#             'StringValue': 'String',
#         },
#         'AWS.SNS.SMS.SenderID': {
#             'DataType': 'String',
#             'StringValue': SENDER_ID
#         }
#     }
# )

#     print(response)
#     print("MessageId:" + response["MessageId"])
#     print("HTTPStatusCode:" + str(response["ResponseMetadata"]["HTTPStatusCode"]))



    # some_list_of_contacts['91+701233842']
    
    # client = boto3.client(
    # "sns",
    # aws_access_key_id="YOUR ACCES KEY",
    # aws_secret_access_key="YOUR SECRET KEY",
    # region_name=us-east-1
    # )
    # topic = client.create_topic(Name="notifications")
    # topic_arn = topic['TopicArn']  # get its Amazon Resource Name
    # for number in some_list_of_contacts:
    #     client.subscribe(
    #     TopicArn=topic_arn,
    #     Protocol='sms',
    #     Endpoint=number  
    #    )
    # client.publish(Message="Good news everyone!", TopicArn=topic_arn)

# Publish a message.

    # print("========233455")
    # client = boto3.client(
    #     "sns",
    #     aws_access_key_id="AKIAWUJKMYVN32GPHB5V",
    #     aws_secret_access_key="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",
    #     region_name="us-east-2"
    # )
    # status=client.publish(
    # PhoneNumber="+917012433842",
    # Message="This is Amazon SNS service talking"
    # )
    # print("+91"+params['rece_mobile_no'])
    # print(status)
    # return True

  

    # API_ENDPOINT = "http://sms.sangamamonline.in/httpapi/smsapi"
    # data={
    #     'uname':'uniconsms',
    #     'password':'sms10t44',
    #     'sender':'UNIFOM',
    #     'receiver':params['rece_mobile_no'],
    #     'route':'TA',
    #     'msgtype':'1',
    #     'sms':params['otp_val']+'is Your verification code for Uniconform'
    # }
    # status = requests.get(url = API_ENDPOINT, params=data)
    # print(status)
    # return True








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

        user_id = getUserId(request.data['model_type'])
        print(user_id)
        otpParams ={
                "user_id":user_id,
                "email":email
                }
        #emailResult=SendEmail(otpParams)
        otp_cre_time = datetime.datetime.now().replace(microsecond=0)
        otp_expire_time = otp_cre_time+datetime.timedelta(minutes = 5)
       

           

        user = UsersDtl()

        raw_password = make_password(request.data['password'])
        user.user_id = user_id
        user.user_type = 'Buyer'
        user.category_type = request.data['model_type']
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
        OTP = generateRandomOTP()
        params = {"otp_val": OTP , "otp_cre_time" : otp_cre_time, "otp_exp_time": otp_expire_time}
        otp_user = session.query(UsersDtl).filter(UsersDtl.user_id==user_id).update(params)
        session.commit()
        otpsParams = {
			"otp_val": OTP , 
			"rece_mobile_no":phone,
            
		}
        message=Sms(otpsParams)

        sql = text('SELECT user_id  from users_dtls where user_id="'+user_id+'"' )
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]

        session.close()
        return Response({'response': 'Data saved success fully',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})



def generateRandomOTP():
	digits = "0123456789"
	OTP = ""
	for i in range(6) : 
		OTP += digits[math.floor(random.random() * 10)] 
	return OTP





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
def verifyOTP(request):
    session = dbsession.Session()
    try:
        user_id = request.data['user_id'] if request.data['user_id'] else None
        otp_val = request.data['otp_val'] if request.data['otp_val'] else None
        user=session.query(UsersDtl).filter(UsersDtl.otp_val == otp_val,UsersDtl.user_id==user_id).one()
        db_otp=user.otp_val
        if otp_val!=db_otp:
            print("============")
            return Response({'response':'failed','message':'otp not matched'})
        if otp_val==db_otp:
            print("============1")
            return Response({'response':'success','message':'otp verfiled succesfull'})
    except SQLAlchemyError as e:
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

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
        print("============addcustoomerorders")
        
        product_type=request.data['product_type']
        if request.data['product_type']=="Customized Uniforms" and request.data['prod_sub_type']=="Fabrics":
            sql = text('SELECT MAX(CONVERT(REPLACE(order_id,"PF",""),UNSIGNED INTEGER)) as auto_order_id from customer_order_dtls')
            auto_order_id = session.execute(sql).fetchall()
            order_id = auto_order_id[0][0]
            if order_id == None or order_id == 0 :
                order_id = 100000
            order_id = 'PF'+ str(int(order_id + 1))

            order=CustomerOrderDtl()
            if request.data.getlist('file')[0]!='undefined':
                for f in request.data.getlist('file'):
                    fs=FileSystemStorage()
                    filename=fs.save(f.name,f)
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
                addprod.brand_name=x['brand_name']
                addprod.design_number=x['design_no']
                addprod.shade_number=x['shade_no']
                addprod.catalogue_number=x['catalog_number']
                addprod.size=x['count']
                session.add(addprod)

            session.commit()
            session.close()

        if request.data['product_type']=='Customized Uniforms' and request.data['prod_sub_type']=='Stitching':
            sql = text('SELECT MAX(CONVERT(REPLACE(order_id,"PT",""),UNSIGNED INTEGER)) as auto_order_id from customer_order_dtls')
            auto_order_id = session.execute(sql).fetchall()
            order_id = auto_order_id[0][0]
            if order_id == None or order_id == 0 :
                order_id = 100000
            order_id = 'PT' + str(int(order_id + 1))
            order=CustomerOrderDtl()
            if request.data.getlist('file')[0]!='undefined':
                for f in request.data.getlist('file'):
                    fs=FileSystemStorage()
                    filename=fs.save(f.name,f)
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
            order=CustomerOrderDtl()
            if request.data.getlist('file')[0]!='undefined':
                for f in request.data.getlist('file'):
                    fs=FileSystemStorage()
                    filename=fs.save(f.name,f)
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
        if request.data['product_type']=='Ready Made Uniforms' and request.data['prod_sub_type']=='Order Based Form':
            print("readymade")
            sql = text('SELECT MAX(CONVERT(REPLACE(order_id,"PR",""),UNSIGNED INTEGER)) as auto_order_id from customer_order_dtls')
            auto_order_id = session.execute(sql).fetchall()
            order_id = auto_order_id[0][0]
            if order_id == None or order_id == 0 :
                order_id = 100000
            order_id = 'PR' + str(int(order_id + 1))
            order=CustomerOrderDtl()
            if request.data.getlist('file')[0]!='undefined':
                for f in request.data.getlist('file'):
                    fs=FileSystemStorage()
                    filename=fs.save(f.name,f)
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
                addprod.avail_size=x['size']
                session.add(addprod)
            session.commit()
            session.close()
        if request.data['product_type']=='Uniform Accesoriess' and request.data['prod_sub_type']=='none':
            print("====================xssdsdsdsdsds")
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
        #getUserId('LA')
        user_id = getUserId('LA')
        otpParams ={
                "user_id":user_id,
                "email":email
            }
        #emailResult=SendEmail(otpParams)
        #print(emailResult)
           

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
        labors.status=request.data['status']
        session.add(labors)
        session.commit()
        return Response({'response': 'success'})

        # if(emailResult == True):
        #     session.commit()
        #     session.close()
        #     return Response({'response':'success'})
        # else:
        #     session.rollback()
        #     session.close()
        #     return Response({'response':'Error occured'})
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
        otp_cre_time = datetime.datetime.now().replace(microsecond=0)
        otp_expire_time = otp_cre_time+datetime.timedelta(minutes = 5)
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
        # emailResult=SendEmail(otpParams)
        # print(emailResult)
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
        OTP = generateRandomOTP()
        params = {"otp_val": OTP , "otp_cre_time" : otp_cre_time, "otp_exp_time": otp_expire_time}
        otp_user = session.query(UsersDtl).filter(UsersDtl.user_id==user_id).update(params)
        session.commit()
        otpsParams = {
        "otp_val": OTP , 
        "rece_mobile_no":phone,
        }
        message=Sms(otpsParams)

        sql = text('SELECT user_id  from users_dtls where user_id="'+user_id+'"' )
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        return Response({'response': 'Data saved success fully',"product_dtls_list":product_dtls_list})
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
        otp_cre_time = datetime.datetime.now().replace(microsecond=0)
        otp_expire_time = otp_cre_time+datetime.timedelta(minutes = 5)
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
            # emailResult=SendEmail(otpParams)
            # print(emailResult)
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
            OTP = generateRandomOTP()
            params = {"otp_val": OTP , "otp_cre_time" : otp_cre_time, "otp_exp_time": otp_expire_time}
            otp_user = session.query(UsersDtl).filter(UsersDtl.user_id==user_id).update(params)
            session.commit()
            otpsParams = {
                "otp_val": OTP , 
                "rece_mobile_no":data[9],
                }
            message=Sms(otpsParams)

            sql = text('SELECT user_id  from users_dtls where user_id="'+user_id+'"' )
            prod_list = session.execute(sql).fetchall()
            product_dtls_list = [dict(row) for row in prod_list]
            return Response({'response': 'Data saved success fully',"product_dtls_list":product_dtls_list})

        if request.data['prod_type']=='Customized Uniforms' and request.data['sub_type']=='stitching':


            order_lines=json.dumps(request.data['order_lines'])
            user_id = getUserId('TS')
            otpParams ={
                "user_id":user_id,
                "email":data[11]
                }
            #emailResult=SendEmail(otpParams)
            # print(emailResult)
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
            OTP = generateRandomOTP()
            params = {"otp_val": OTP , "otp_cre_time" : otp_cre_time, "otp_exp_time": otp_expire_time}
            otp_user = session.query(UsersDtl).filter(UsersDtl.user_id==user_id).update(params)
            session.commit()
            otpsParams = {
                "otp_val": OTP , 
                "rece_mobile_no":data[9],
                }
            message=Sms(otpsParams)

            sql = text('SELECT user_id  from users_dtls where user_id="'+user_id+'"' )
            prod_list = session.execute(sql).fetchall()
            product_dtls_list = [dict(row) for row in prod_list]
            return Response({'response': 'Data saved success fully',"product_dtls_list":product_dtls_list})
        if request.data['prod_type']=='Customized Uniforms' and request.data['sub_type']=='fabricandstitching':
            user_id = getUserId('FT')
            otpParams ={
                "user_id":user_id,
                "email":data[11]
                }
            #emailResult=SendEmail(otpParams)
            #print(emailResult)
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
            OTP = generateRandomOTP()
            params = {"otp_val": OTP , "otp_cre_time" : otp_cre_time, "otp_exp_time": otp_expire_time}
            otp_user = session.query(UsersDtl).filter(UsersDtl.user_id==user_id).update(params)
            session.commit()
            otpsParams = {
                "otp_val": OTP , 
                "rece_mobile_no":data[9],
                }
            message=Sms(otpsParams)

            sql = text('SELECT user_id  from users_dtls where user_id="'+user_id+'"' )
            prod_list = session.execute(sql).fetchall()
            product_dtls_list = [dict(row) for row in prod_list]
            return Response({'response': 'Data saved success fully',"product_dtls_list":product_dtls_list})
        if request.data['prod_type']=='Ready Made Uniforms':
            print("REady")
            user_id = getUserId('RM')
            otpParams ={
                "user_id":user_id,
                "email":data[11]
                }
            #emailResult=SendEmail(otpParams)
            #print(emailResult)
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
            supplier.prod_sub_type='orderbasedform'
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
            OTP = generateRandomOTP()
            params = {"otp_val": OTP , "otp_cre_time" : otp_cre_time, "otp_exp_time": otp_expire_time}
            otp_user = session.query(UsersDtl).filter(UsersDtl.user_id==user_id).update(params)
            session.commit()
            otpsParams = {
                "otp_val": OTP , 
                "rece_mobile_no":data[9],
                }
            message=Sms(otpsParams)

            sql = text('SELECT user_id  from users_dtls where user_id="'+user_id+'"' )
            prod_list = session.execute(sql).fetchall()
            product_dtls_list = [dict(row) for row in prod_list]
            return Response({'response': 'Data saved success fully',"product_dtls_list":product_dtls_list})
        if request.data['prod_type']=='Uniform Accessories':
            user_id = getUserId('AS')
            otpParams ={
            "user_id":user_id,
            "email":data[11]
            }
            # emailResult=SendEmail(otpParams)
            # print(emailResult)
            
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
            OTP = generateRandomOTP()
            params = {"otp_val": OTP , "otp_cre_time" : otp_cre_time, "otp_exp_time": otp_expire_time}
            otp_user = session.query(UsersDtl).filter(UsersDtl.user_id==user_id).update(params)
            session.commit()
            otpsParams = {
                "otp_val": OTP , 
                "rece_mobile_no":data[9],
                }
            message=Sms(otpsParams)

            sql = text('SELECT user_id  from users_dtls where user_id="'+user_id+'"' )
            prod_list = session.execute(sql).fetchall()
            product_dtls_list = [dict(row) for row in prod_list]
            return Response({'response': 'Data saved success fully',"product_dtls_list":product_dtls_list})


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
        product.careted_time=datetime.datetime.now()
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
        sql = text('SELECT email,phone_number,prod_type,prod_sub_type,organization_name,place,state,district from supplier_table where user_id="'+user_id+'"')
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
        sql = text('SELECT * from customer_add_product_dtls where order_id="'+order_id+'"' )
        prod_list = session.execute(sql).fetchall()
        product__list = [dict(row) for row in prod_list]
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list,"product__list":product__list})
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
        columns =['organization_name','place','state','district','phone_number','item_name','image','price','status','prod_type','prod_id','item_code','shades','size','condition']
        cart_list = session.query(SupplierTable.organization_name, SupplierTable.place,SupplierTable.state,SupplierTable.district,SupplierTable.phone_number,ProductDtl.item_name,ProductDtl.image,ProductDtl.price,ProductDtl.status,ProductDtl.prod_type,ProductDtl.prod_id,ProductDtl.item_code,ProductDtl.shades,ProductDtl.size,ProductDtl.condition).join(ProductDtl, SupplierTable.user_id == ProductDtl.user_id).all()
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
        sql = text("select customer_dtls.user_id,customer_dtls.pincode,customer_order_dtls.order_id,customer_order_dtls.product_type, customer_order_dtls.category_type,customer_order_dtls.prod_sub_type,customer_order_dtls.photo,customer_order_dtls.delivery_date from  customer_order_dtls join customer_dtls on customer_order_dtls.user_id=customer_dtls.user_id")
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
        sql = text("select users_dtls.user_id,users_dtls.user_id,users_dtls.otp_cre_time,supplier_table.supplier_name,supplier_table.place,supplier_table.district,supplier_table.state,supplier_table.phone_number,supplier_table.email,supplier_table.prod_type,supplier_table.prod_sub_type from  users_dtls join supplier_table on supplier_table.user_id=users_dtls.user_id where status IS  NULL and user_type='supplier' order by usid desc")
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
    subject, from_email, to = 'Hello from Uniconform', 'admin@uniconform.in', params['email']
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
    subject, from_email, to = 'Hello from Uniconform', 'admin@uniconform.in', params['email']
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
        subject, from_email, to = request.data['subject'], 'admin@uniconform.in', request.data['email']
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
        order.expiry_date=request.data['delivery_date']
        session.add(order)
        session.flush()
        for x in json.loads(request.data['order_lines']):
            addprod=QutationDtl()
            addprod.qutation_id=order.quotatit_id
            addprod.qutation_form_id=order.quatation_form_id
            addprod.item_name=x['item']
            addprod.count=x['count']
            addprod.rate_per_item=x['rate_per_meter']
            addprod.total__amt=x['total_amount']
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
        sql = text('select DISTINCT(quotation_table.quotatit_id),quotation_table.quotatit_id, quotation_table.order_form_id,quotation_table.user_id,quotation_table.supplier_id,quotation_table.grand_total,quotation_table.quatation_form_id,quotation_table.is_order_accepted,quotation_table.prod_type,quotation_table.prod_sub_type from quotation_table join qutation_dtls on quotation_table.quotatit_id=qutation_dtls.qutation_id where qutation_dtls.user_id="'+user_id+'" and expiry_date> CURDATE()')
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        sql = text('select DISTINCT(quotation_table.quotatit_id),quotation_table.quotatit_id, quotation_table.order_form_id,quotation_table.user_id,quotation_table.supplier_id,quotation_table.grand_total,quotation_table.quatation_form_id,quotation_table.is_order_accepted,quotation_table.prod_type,quotation_table.prod_sub_type from quotation_table join qutation_dtls on quotation_table.quotatit_id=qutation_dtls.qutation_id where qutation_dtls.user_id="'+user_id+'" and expiry_date< CURDATE()' )
        exp_prod_list = session.execute(sql).fetchall()
        exp_product_dtls_list = [dict(row) for row in exp_prod_list]
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list,"exp_product_dtls_list":exp_product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def getQuotationlist(request):
    try:
        user_id = request.data['user_id']
        quatation_form_id=request.data['qutation_form_id']
        session = dbsession.Session()
        sql = text('select quotation_table.quotatit_id, quotation_table.order_form_id,quotation_table.user_id,quotation_table.supplier_id,quotation_table.grand_total,quotation_table.quatation_form_id,quotation_table.is_order_accepted,quotation_table.prod_type,quotation_table.prod_sub_type,qutation_dtls.item_name,qutation_dtls.count,qutation_dtls.rate_per_item,qutation_dtls.total__amt from quotation_table join qutation_dtls on quotation_table.quotatit_id=qutation_dtls.qutation_id where supplier_id="'+user_id+'" and quotation_table.quatation_form_id="'+quatation_form_id+'"')
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
def quotelist_for_all(request):
    try:
        quote_id = request.data['quote_id']
        session = dbsession.Session()
        sql = text('SELECT * FROM quotation_table where quatation_form_id="'+quote_id+'"')
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
        expiry_date=request.data['expiry_date']
        session = dbsession.Session()
        session.query(QuotationTable).filter(QuotationTable.quatation_form_id==quote_id,QuotationTable.user_id==user_id).update({'is_order_accepted':order_status})
        session.query(QuotationTable).filter(QuotationTable.quatation_form_id==quote_id,QuotationTable.user_id==user_id).update({'expiry_date':expiry_date})
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
        sql = text('SELECT * FROM customer_dtls order by customer_id desc')
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
        sql = text('SELECT * FROM supplier_table order by sid desc')
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
        sql = text('SELECT * FROM customer_order_dtls order by id desc')
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
        
        sql = text("select * from quotation_table where supplier_id='"+user_id+"' order by quotatit_id desc")
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
        user_id=request.data['user_id']
        sql = text('select pincode from supplier_table where user_id="'+user_id+'"')
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
def supplierdetails_by_id(request):
    try:
        session = dbsession.Session()
        user_id=request.data['user_id']
        sql = text('select *  from supplier_table where user_id="'+user_id+'"')
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
def customerdetails_by_id(request):
    try:
        session = dbsession.Session()
        user_id=request.data['user_id']
        sql = text('select *  from customer_dtls where user_id="'+user_id+'"')
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
def banneraddd(request):
    try:
        session = dbsession.Session()
        for f in request.data.getlist('myfile'):
            print("=========")
            banner = BannerTable()
            fs=FileSystemStorage()
            filename=fs.save(f.name,f)
            uploaded_file_url = fs.url(filename)
            banner.banner_path=uploaded_file_url
            banner.banner_type=request.data['banner_type']
            banner.banner_name=request.data['banner_name']
            session.add(banner)
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
def addbannerList(request):
    try:
        session = dbsession.Session()
        sql = text('select *  from banner_table')
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
def ImageDetails(request):
    try:
        session = dbsession.Session()
        banner_id = request.data['id']
        sql = text("select *  from banner_table where banner_id='"+banner_id+"'")
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
def EditBannerImage(request):
    try:
        session = dbsession.Session()
        banner_id = request.data['id']
        for f in request.data.getlist('myfile'):
            banner = BannerTable()
            fs=FileSystemStorage()
            filename=fs.save(f.name,f)
            uploaded_file_url = fs.url(filename)
            session.query(BannerTable).filter(BannerTable.banner_id==banner_id).update({'banner_path':uploaded_file_url})
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
def deletebanner(request):
    try:
        session = dbsession.Session()
        banner_id = request.data['id']
        session.query(BannerTable).filter(BannerTable.banner_id==banner_id).delete()
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
def getOrderdetials(request):
    try:
     
        order_id = request.data['order_id']
        session = dbsession.Session()
        sql = text('select *  from customer_order_dtls where order_id="'+order_id+'"')
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        sql = text('select *  from customer_add_product_dtls where order_id="'+order_id+'"')
        add_product_dtls = session.execute(sql).fetchall()
        add_product_dtls_dtls = [dict(row) for row in add_product_dtls]
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list,"add_product_dtls_dtls":add_product_dtls_dtls})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def production_details(request):
    try:
     
        sid = request.data['sid']
        types = request.data['type']
        session = dbsession.Session()
        sql = text('select *  from supplier_table where sid="'+sid+'"  and prod_sub_type="'+types+'"')
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        sql = text('select *  from supplier_production_dtls where sid="'+sid+'"')
        add_product_dtls = session.execute(sql).fetchall()
        add_product_dtls_dtls = [dict(row) for row in add_product_dtls]
        session.close()
        return Response({'response': 'success',"product_dtls_list":product_dtls_list,"add_product_dtls_dtls":add_product_dtls_dtls})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def getbannerimages(request):
    try:
     
        types = request.data['type']
        session = dbsession.Session()
        sql = text('select *  from banner_table where banner_type ="'+types+'"')
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})

@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def generatebill(request):
    session = dbsession.Session()

    try:
        order_id=request.data['order_id']
        sub_type=request.data['type']
        quote_id=request.data['quote_id']
        email=request.data['emailto']
        grand_total=request.data['grand_total']
       
        sql = text('SELECT * from customer_order_dtls where order_id="'+order_id+'" and prod_sub_type="'+sub_type+'"' )
        prod_list = session.execute(sql).fetchall()
        product_dtls_list1 = [dict(row) for row in prod_list]
        sql = text('SELECT * from customer_add_product_dtls where order_id="'+order_id+'"' )
        prod_list = session.execute(sql).fetchall()
        product__list2 = [dict(row) for row in prod_list]

        quote_id = request.data['quote_id']
        sql = text('SELECT * FROM quotation_table where quatation_form_id="'+quote_id+'"')
        prod_list = session.execute(sql).fetchall()
        product_dtls_list3 = [dict(row) for row in prod_list]
        sql = text('SELECT * FROM qutation_dtls where qutation_form_id="'+quote_id+'"')
        quote_list = session.execute(sql).fetchall()
        quote_dtls_list = [dict(row) for row in quote_list]
 
        buyer_id=request.data['buyer_id']
        sql = text('select *  from customer_dtls where user_id="'+buyer_id+'"')
        buyers_list = session.execute(sql).fetchall()
        buyers_list_dtls = [dict(row) for row in buyers_list]

        supplier_id=request.data['supplier_id']
        sql = text('select *  from supplier_table where user_id="'+supplier_id+'"')
        supplier_table = session.execute(sql).fetchall()
        supplier_table_dtls = [dict(row) for row in supplier_table]


        subject = 'Uniconform, -Quotation no.{}'.format(quote_id)
        message='Please, find the attached Quotation  for your recent orders'
        emails=[email]
        mail = EmailMessage(subject, message, "anjujoy0310@gmail.com",emails)
        html=render_to_string('agrrement.html',{'order':product_dtls_list3,'order_dtls':quote_dtls_list,'buyer_dtls':buyers_list_dtls,'supplier_dtls':supplier_table_dtls,'grand_total':grand_total})
        out = BytesIO()
        weasyprint.HTML(string=html,base_url="http://www.jonathantneal.com/examples/invoice/logo.png").write_pdf(out)
        mail.attach('order_{}.pdf'.format(quote_id),out.getvalue(),'application/pdf')
        mail.send()
        return Response({'response': 'success'})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})


@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def getAccessories(request):
    try:
     
    
        session = dbsession.Session()
        sql = text("select *  from product_dtls where prod_type ='Accesories' or prod_type='Ready mades'")
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})


@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def getMachines(request):
    try:

        session = dbsession.Session()
        sql = text("select *  from product_dtls where prod_type ='machines'")
        prod_list = session.execute(sql).fetchall()
        product_dtls_list = [dict(row) for row in prod_list]
        return Response({'response': 'success',"product_dtls_list":product_dtls_list})
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        session.close()
        return Response({'response': 'Error occured'})








        

        



        















