import json
from pickle import FALSE, TRUE
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import Invoice
from .bo import auth, sharedServices
from rest_framework.views import APIView

# Create your views here.
class InvoiceView(APIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self,request, id=0):
        # Validate Token
        _auth = auth()
        token = _auth.getTokenHeader(request)
        if(token == ""):
            datos = {'message':"No autorizado", 'success':False}
            return JsonResponse(datos)

        if(_auth.validToken(token)):
            if id == 0:
                invoices = list(Invoice.objects.values())
                if(len(invoices)):

                    # Get users names
                    _sharedServices = sharedServices()
                    users = _sharedServices.getUsers()

                    for invoice in invoices:
                        for user in users:
                            if(int(invoice['userid']) == int(user['userId'])):
                                invoice['userid'] = user['userName']
                                break

                datos = {'message':'success','invoices':invoices} if len(invoices)>0 else {'message':'Invoices not found...'}
                return JsonResponse(datos)
            else :
                invoices = list(Invoice.objects.filter(id=id).values())
                datos = {'message':'success','invoices':invoices[0]} if len(invoices)>0 else {'message':'Invoice not found...'}
                return JsonResponse(datos)
        else:
            datos = {'message':"No autorizado", 'success':False}
            return JsonResponse(datos)

    def post(self,request):
        # Validate Token
        _auth = auth()
        token = _auth.getTokenHeader(request)
        if(token == ""):
            datos = {'message':"No autorizado", 'success':False}
            return JsonResponse(datos)

        if(_auth.validToken(token)):
            jd = json.loads(request.body)

            # Update qty available by product
            _sharedServices = sharedServices()
            result = _sharedServices.updateQtyAvailableByProduct(jd['itemid'],jd['quantity'])
            if (result):
                Invoice.objects.create(
                    userid = jd['userid'],
                    itemid = jd['itemid'],
                    unitprice = jd['unitprice'],
                    quantity = jd['quantity'],
                    invoicetotal = jd['invoicetotal']
                )
                datos = {'message': 'success', 'success': True}
                return JsonResponse(datos)
            else:
                datos = {'message': 'No fue posible actualizar el inventario. Comuníquese con atención al cliente. ', 'success': False}
                return JsonResponse(datos)

        else:
            datos = {'message':"No autorizado", 'success':False}
            return JsonResponse(datos)

    def put(self,request, id):
        # Validate Token
        _auth = auth()
        token = _auth.getTokenHeader(request)
        if(token == ""):
            datos = {'message':"No autorizado", 'success':False}
            return JsonResponse(datos)

        if(_auth.validToken(token)):
            jd = json.loads(request.body)
            
            # Update qty available by product
            _sharedServices = sharedServices()
            result = _sharedServices.updateQtyAvailableByProduct(jd['itemid'],jd['quantity'])
            if (result):
                invoice = list(Invoice.objects.filter(id=id).values())
                if len(invoice) > 0:
                    invoice = Invoice.objects.get(id=id)
                    invoice.userid = jd['userid']
                    invoice.itemid = jd['itemid']
                    invoice.unitprice = jd['unitprice']
                    invoice.quantity = jd['quantity']
                    invoice.invoicetotal = jd['invoicetotal']
                    invoice.save()
                    datos = {'message': 'success', 'success':True}
                else :
                    datos = {'message': 'Invoice not found...', 'success':False}
            else:
                datos = {'message': 'No fue posible actualizar el inventario. Comuníquese con atención al cliente.', 'success': False}
                return JsonResponse(datos)

            return JsonResponse(datos)
        else:
            datos = {'message':"No autorizado", 'success':False}
            return JsonResponse(datos)

    def delete(self,request, id):
        # Validate Token
        _auth = auth()
        token = _auth.getTokenHeader(request)
        if(token == ""):
            datos = {'message':"No autorizado", 'success':False}
            return JsonResponse(datos)
            
        if(_auth.validToken(token)):
            invoice = list(Invoice.objects.filter(id=id).values())
            if len(invoice) > 0:
                print(invoice)
                # Update qty available by product
                _sharedServices = sharedServices()
                result = _sharedServices.updateQtyAvailableByProduct(invoice[0]['itemid'], invoice[0]['quantity']*-1)
                if (result):
                    Invoice.objects.filter(id=id).delete()
                    datos = {'message': 'success', 'success': True}
                else:
                    datos = {'message': 'No fue posible actualizar el inventario. Comuníquese con atención al cliente.', 'success': False}
                    return JsonResponse(datos)

            else :
                datos = {'message': 'Invoice not found...'}
            return JsonResponse(datos)
        else:
            datos = {'message':"No autorizado", 'success':False}
            return JsonResponse(datos)

    