
             

            #         customer_dtls=session.query(CustomerDtl).filter(CustomerDtl.user_id==user_id).all()
            #         if len(customer_dtls)==0:
            #             return Response({'response': 'error','message':'user not found in the specified category'})
            #         else:
            #             customer_dtls_list = json.loads(json.dumps(customer_dtls, cls=AlchemyEncoder))
            #             return Response({'response': 'success','data':customer_dtls_list,'type':'buyerandseller','category':'customer'})

            #     if request.data['user_type']=='buyer' and request.data['category_type']=='supplier':
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