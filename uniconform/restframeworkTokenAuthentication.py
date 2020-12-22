import jwt
import json
import datetime
from django.conf import settings
from unicon.models import AuthToken,UsersDtl
from django.http import HttpResponse
from uniconform import dbsession
from sqlalchemy.exc import SQLAlchemyError
from rest_framework import status, exceptions
from rest_framework.authentication import get_authorization_header, BaseAuthentication


class TokenAuthentication(BaseAuthentication):

    model = None

    def get_model(self):
        return UsersDtl



    def authenticate(self, request):
        session = dbsession.Session()
        print("AUTH TESTING ==== ")
        print(request.__dict__)
        
        auth = get_authorization_header(request).split()
        print(auth)

        print(auth[0].lower())
        if not auth or auth[0].lower() != b'bearer':
            return None
        # print(len(auth))
        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)

        try:
            print("======")
            token = auth[1]
            # print(token)
            if token=="null":
                msg = 'Null token not allowed'
                raise exceptions.AuthenticationFailed(msg)

        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)
        session.close()
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        # model = self.get_model()
        session = dbsession.Session()
        print("============authenticate_credentials===========")
        #print(token)
        #print(settings.SECRET_KEY)
        try:
            print("Try inside")
            payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.DecodeError:
            session.rollback()
            print("Error------")
            msg = {'Error': "Token mismatch"}
            raise exceptions.AuthenticationFailed(msg)
            # raise exceptions.AuthenticationFailed(msg)
        print(payload)
        if payload:
            user_id = payload['user_id']
            expiry = payload['expiry']
        msg = {'Error': "Token mismatch",'status' :"401"}
        try:
            try:
                user = session.query(AuthToken).filter(AuthToken.user_id==user_id,AuthToken.key==token).one()
            except SQLAlchemyError as e:
                print("Token Not Exit" ,e)
                session.rollback()
                session.close()

            try:
                print("Before Create sqlalchemy")
                user = session.query(UsersDtl).filter_by(user_id=user_id).one()
                print(user)
                print("user data")
            except SQLAlchemyError as e:
                print("User not Exit",e)
                raise exceptions.AuthenticationFailed({'Error':'Token is invalid'})
                session.rollback()
                session.close()
                user = None
            if not user.status == 'login':
                print("came inside")
                raise exceptions.AuthenticationFailed({'Error':'User Not Logedin'})
            try:
                auth_token = session.query(AuthToken).filter_by(user_id=user_id).one()
                print("auth_token")
                print(auth_token)
            except SQLAlchemyError as e:
                print(e)
                session.rollback()
                auth_token = None
            stored_token = b'' + (auth_token.key).encode("utf-8")
            print(stored_token)
            print(token)
            print(stored_token == token)
            if not stored_token == token:
                raise exceptions.AuthenticationFailed(msg)

            if datetime.datetime.strptime(expiry, "%Y-%m-%d").date() < datetime.date.today():
                raise exceptions.AuthenticationFailed({'Error':'Token Expired.'})
               
        except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:
            return HttpResponse({'Error': "Token is invalid"}, status="403")
        except SQLAlchemyError as e:
            return HttpResponse({'Error': "Internal server error"}, status="500")
        session.close()
        return (user, token)

    def authenticate_header(self, request):
        return 'Bearer'