import shopify
import json
import requests
import datetime
from .models import installer
from django.db.models import Q
from django.utils.html import strip_tags
from django.http import JsonResponse, HttpResponse

API_KEY = "1c86866d8c638b28da99bbdfe3cd5fce"
SHARED_SECRET = "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"
API_VERSION = "2021-01"


class App_api:
    @staticmethod
    def get_order_detail(request):
        # global data
        my_dict = dict()
        shop_detail = strip_tags(request.GET.get('shop'))
        cus_email = strip_tags(request.GET.get('email'))
        cus_id = strip_tags(request.GET.get('customer'))
        ord_id = strip_tags(request.GET.get('order'))
        reas_note = strip_tags(request.GET.get('reason'))
        
        if (shop_detail is not None and shop_detail!='') and (cus_email is not None and cus_email!='') and (cus_id is not None and cus_id!='') and (ord_id is not None and ord_id!=''):
            shop_domain = shop_detail + ".myshopify.com"        
            get_rec = installer.objects.filter(shop=shop_domain)
            # print(get_rec.query)
            if get_rec:
                token = get_rec[0].access_token
            else:
                message = "Invalid Store Data"
                my_dict['error_message'] = message
                return HttpResponse(json.dumps(my_dict), content_type="application/json") 

            
            ur = "https://%s/admin/orders.json?customer_id=%s&financial_status=paid,partially_refunded,refunded&status=any" % (shop_domain, cus_id)
            # print(shop_domain, ur, "Data")
            headers = {
                "X-Shopify-Access-Token": token,
                "Content-Type": "application/json",
                "client_id": API_KEY,
                "client_secret": SHARED_SECRET
            }
            r = requests.get(url=ur, headers=headers)
            c_data = json.loads(r.text)
            get_data = dict()
            data_vari_dict = dict()
            # print(reas_note, "REASON IS HERE")
            if c_data != "":
                for x in c_data["orders"]:
                    if x['financial_status'] == "refunded":
                        message = "Order fully refunded"
                        my_dict['error_message'] = message
                        return HttpResponse(json.dumps(my_dict), content_type="application/json")
                    else:
                        global data_dict_data
                        '''new added'''
                        data = x
                        data_dict_data = data
                        if data['email'] == cus_email and str(data['order_number']) == str(ord_id):
                            
                            or_id = data["id"]
                            from .models import detail_order
                            data_detail_variant = detail_order.objects.filter(Q(shop_data=shop_domain), Q(ordid=str(or_id)), Q(order_id=str(ord_id)), Q(custom_id=str(cus_id)))
                            # data_vari_dict = {
                            # }

                            if data_detail_variant:
                                count = 0
                                data_vari_dict['line_items'] = list()
                                for data_detail in data_detail_variant:
                                    vda_variants = data_detail.variants
                                    vda_quant = data_detail.quantity
                                    #print(vda_variants, vda_quant, "FRM database")

                                    if ',' in vda_variants:
                                        count = 0
                                        vdata_vari = vda_variants.split(',')
                                        # print(vdata_vari, type(vdata_vari), "step1 vari")
                                    else:
                                        count = 999
                                        vdata_vari = vda_variants
                                        # print(vdata_vari, type(vdata_vari), "step2 vari")

                                    if ',' in vda_quant:
                                        count = 0
                                        vdata_quant = vda_quant.split(',')
                                        # print(vdata_quant, type(vdata_quant), "step1 quant")
                                    else:
                                        count = 999
                                        vdata_quant = vda_quant
                                        # print(vdata_quant, type(vdata_quant), "step12 quant")

                                    # ENABLED #

                                    if count == 999: 
                                        data = dict()
                                        data_y = vdata_quant
                                        data_x = vdata_vari
                                    
                                        # print(data_x, data_y, "step1" , type(data_x), type(data_y))
                                        
                                        update = "false"
                                        if len(data_vari_dict['line_items']) != 0:
                                            for d in data_vari_dict['line_items']:
                                                # print(d['quant'], "step main")
                                                if str(d['variants']) == str(data_x):
                                                    # print(d['quant'], "htfgh")
                                                    d['quant'] = int(data_y) + int(d['quant'])
                                                    # print(d['quant'], "D quant")
                                                    update = "true"
                                                    break
                                        if update == "false":
                                            da = {
                                                "variants":data_x,
                                                "quant":data_y
                                            }
                                            data_vari_dict['line_items'].append(da)
                                        # print(data_vari_dict, "single")
                                    else:
                                        if len(vdata_vari) == len(vdata_quant):
                                            for x in range(len(vdata_vari)):
                                                data = dict()
                                                data_y = vdata_quant[x]
                                                data_x = vdata_vari[x]

                                                update = "false"
                                                if len(data_vari_dict['line_items']) != 0:
                                                    for d in data_vari_dict['line_items']:
                                                        
                                                        if str(d['variants']) == str(data_x):
                                                           
                                                            d['quant'] = int(data_y) + int(d['quant'])
                                                            
                                                            update = "true"
                                                            break
                                                if update == "false":
                                                    da = {
                                                        "variants":data_x,
                                                        "quant":data_y
                                                    }
                                                    data_vari_dict['line_items'].append(da) 
                                                
                                if len(data_vari_dict['line_items']) > 0 and len(data_dict_data['line_items']) > 0:
                                    for l, data_line in enumerate(data_dict_data['line_items'], start=0):
                                        for data_database in data_vari_dict['line_items']:
                                            # print(data_database,'l')
                                            if int(data_line['variant_id']) == int(data_database['variants']):
                                                if int(data_line['quantity']) == int(data_database['quant']):
                                                    # print(data_line, "data_line")
                                                    # print(data_database, "data_database")
                                                    data_dict_data['line_items'][l] = ''
                                                    break
                                                elif int(data_line['quantity']) > int(data_database['quant']):
                                                    data_line['quantity'] = int(data_line['quantity']) - int(data_database['quant'])
                                                    break
                                        # print(data_dict_data['line_items'])
                                data_dict_data['line_items'] = list(filter(None, data_dict_data['line_items']))
                                # print(data_dict_data['line_items'])
                              
                            if (request.GET.get('variants') is not None) and (request.GET.get('quantity') is not None):
                                total = 0
                                quant = 0
                                ful_stat = ''
                                if (',' in request.GET.get('variants')) and (',' in request.GET.get('quantity')):
                                    
                                    variants = request.GET.get('variants').split(',')
                                    quantity = request.GET.get('quantity').split(',')
                                    # print(data_vari_dict, "step1")
                                    if len(data_vari_dict) != 0:
                                        for dvdata in data_vari_dict['line_items']: # json 
                                            for j in range(len(variants)):
                                                dvvari = variants[j]
                                                if str(dvvari) == str(dvdata['variants']):
                                                    if int(dvdata['quant']) < int(quantity[j]):
                                                        message = "wrong quantity error"
                                                        my_dict['error_message'] = message
                                                        return HttpResponse(json.dumps(my_dict), content_type="application/json")
                                    # print(data_dict_data, "json data")
                                    for xdata in data_dict_data['line_items']: # json 
                                        for i in range(len(variants)): #re
                                            xvari = variants[i]
                                            if str(xvari) == str(xdata['variant_id']):
                                                if int(xdata['quantity']) >= int(quantity[i]):
                                                    if xdata['fulfillment_status'] == "fulfilled":
                                                        quant = int(quantity[i]) + int(quant)
                                                        total = float(float(xdata["price"]) * float(quant))
                                                        ful_stat = xdata['fulfillment_status']
                                                else:
                                                    message = "wrong quantity error"
                                                    my_dict['error_message'] = message
                                                    return HttpResponse(json.dumps(my_dict), content_type="application/json")
                                else:
                                    variants = request.GET.get('variants')
                                    quantity = request.GET.get('quantity')
                                    # print(data_vari_dict, "step2")
                                    if len(data_vari_dict) != 0:
                                        for dvdata in data_vari_dict['line_items']: # json 
                                            dvvari = variants
                                            if str(dvvari) == str(dvdata['variants']):
                                                if int(dvdata['quant']) < int(quantity):
                                                    message = "wrong quantity error"
                                                    my_dict['error_message'] = message
                                                    return HttpResponse(json.dumps(my_dict), content_type="application/json")

                                    # print(variants, quantity, "MAINA")
                                    for xdata in data_dict_data['line_items']:
                                        # print(xdata)
                                        if str(variants) == str(xdata['variant_id']):
                                            if int(xdata['quantity']) >= int(quantity):
                                                if xdata['fulfillment_status'] == "fulfilled":
                                                    quant = int(quantity)
                                                    # print(quant)
                                                    total = str(float(xdata["price"]) * float(quant))
                                                    # print(total)
                                                    ful_stat = xdata['fulfillment_status']
                                            else:
                                                message = "wrong quantity error"
                                                my_dict['error_message'] = message
                                                return HttpResponse(json.dumps(my_dict), content_type="application/json")
                            
                                if (',' in request.GET.get('variants')) and (',' in request.GET.get('quantity')):
                                    
                                    if len(variants) == len(quantity):
                                        variant_da = ','.join(variants)
                                        qunt_da = ','.join(quantity)
                                    else:
                                        message = "something went wrong!"
                                        my_dict['error_message'] = message
                                        return HttpResponse(json.dumps(my_dict), content_type="application/json")
                                else:
                                    variant_da = variants
                                    qunt_da = quantity

                                date = datetime.datetime.now().strftime("%d"+"/"+"%m"+"/"+"%Y")
                                from .models import detail_order
                                get_rec_data_read = detail_order.objects.filter(Q(shop_data=shop_domain), Q(order_id=str(ord_id)), Q(variants=str(variant_da)), Q(quantity=str(qunt_da)), Q(custom_id=str(cus_id)))
                                # print(get_rec_data_read.query, "QUERY IS HERE")
                                if get_rec_data_read:
                                    message = "Already requested for return!"
                                    my_dict['error_message'] = message
                                    return HttpResponse(json.dumps(my_dict), content_type="application/json")
                                else:
                                    get_rec_data = detail_order()
                                    get_rec_data.order_total = total
                                    get_rec_data.order_fulfill_status = ful_stat
                                    get_rec_data.shop_data = shop_domain
                                    get_rec_data.variants = variant_da
                                    get_rec_data.quantity = qunt_da
                                    get_rec_data.tquant = quant
                                    get_rec_data.order_id = ord_id
                                    get_rec_data.ordid = or_id
                                    get_rec_data.order_reason = reas_note
                                    get_rec_data.order_note = ""
                                    get_rec_data.status = "PENDING"
                                    get_rec_data.custom_id = cus_id
                                    get_rec_data.crea_date = date
                                    get_rec_data.upda_date = date
                                    get_rec_data.save()
                                    return HttpResponse(json.dumps(get_data), content_type="application/json")
                            else:
                                # data_dict_data['line_items'] = data_line
                                # print(data_dict_data, "hellodata")
                                if(len(data_dict_data['line_items']) > 0):
                                    get_data = data_dict_data
                                    return HttpResponse(json.dumps(get_data), content_type="application/json")
                                else:
                                    message = "all items requested for return"
                                    my_dict['error_message'] = message
                                    return HttpResponse(json.dumps(my_dict), content_type="application/json") 
                        else:
                            message = "matching Order not found"
                            my_dict['error_message'] = message
                            return HttpResponse(json.dumps(my_dict), content_type="application/json") 
                        '''end new added'''

            else:
                message = "Order not found!"
                my_dict['error_message'] = message
                return HttpResponse(json.dumps(my_dict), content_type="application/json")                 
        else:
            message = "Some filed are missing"
            my_dict['error_message'] = message
            return HttpResponse(json.dumps(my_dict), content_type="application/json")
        return HttpResponse(json.dumps(get_data), content_type="application/json") 

    @staticmethod
    def get_customer(request):
        error_dict = dict()
        custome_id = request.GET.get('customer')
        shop = request.GET.get('shop')
        if (custome_id is not None and custome_id != '') and (shop is not None and shop != ''):
            shop = shop +'.myshopify.com'
            from .models import detail_order
            posts = detail_order.objects.filter(Q(custom_id=custome_id), Q(shop_data=shop))  
            # print(posts.query)
            if posts:
                ''' BELOW FUNCTION CALL FOR GET ORDER VARIANT BY IT'S ID '''
                main_dict = dict()
                main_sub_dict = dict()

                # print(posts,'asdsa')
                for x in posts:
                    o_id = x.id
                    o_page_id = x.ordid
                    c_order_id = x.order_id
                    c_order_fulfill_status = x.order_fulfill_status
                    c_crea_date = x.crea_date
                    c_status = x.status  
                    c_refund_date = x.upda_date
                    if (',' in x.variants):
                        y =  x.variants.split(',')
                    else:
                        y = x.variants

                    if (',' in x.quantity):
                        q =  x.quantity.split(',')
                    else:
                        q = x.quantity
                    
                    c_json_data = ''
                    if o_page_id is not None and o_page_id != '':
                        # print(shop, o_page_id)
                        d_rec = installer.objects.filter(shop=shop)
                        if d_rec:
                            token = d_rec[0].access_token
                            # print(token, shop, "Data")
                            url = "https://%s/admin/api/%s/orders/%s.json" % (shop, API_VERSION, o_page_id)

                            headers = {
                                "X-Shopify-Access-Token": token,
                                "Content-Type": "application/json",
                                "client_id": API_KEY,
                                "client_secret": SHARED_SECRET
                            }

                            r = requests.get(url=url, headers=headers)
                            c_json_data = json.loads(r.text)
                            main_sub_dict[o_id] = {'datavaritan':y, 'dataqnt':q,'variants':c_json_data['order']['line_items'],'order_no':c_order_id,'order_status':c_order_fulfill_status,'create_date':c_crea_date,'refund_date':c_refund_date,'refund_status':c_status}
                            main_dict = main_sub_dict.copy() 
                variant_data = main_dict
                # print(variant_data, "DAADADA")
                return HttpResponse(json.dumps(variant_data), content_type="application/json")
            else:
                message = "no data founds"
                error_dict['error_message'] = message
                return HttpResponse(json.dumps(error_dict), content_type="application/json")
        else:
            message = "Some filed are missing"
            error_dict['error_message'] = message
            return HttpResponse(json.dumps(error_dict), content_type="application/json")