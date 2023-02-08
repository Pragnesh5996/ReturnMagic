from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
import requests
import datetime
import shopify as shopifyapi
from .models import installer, about_data, Policy_data, Homedata
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json
# import mysql.connector
# import mysql.connector
from django.db.models import Q
from django.shortcuts import redirect as redc


API_KEY = "1c86866d8c638b28da99bbdfe3cd5fce"
SHARED_SECRET = "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"
API_VERSION = "2021-01"

# Replace the following with your shop URL

shop = ""


# Create your views here.
def login(request):
    return render(request, 'login.html')


def about(request):
    about_rec = about_data.objects.all()
    if len(about_rec)!=0:
        title = about_rec[0].title
        des = about_rec[0].description
        return render(request, 'about.html', {'til': title, 'desc':des})
    else:
        return render(request, 'about.html')


def home_page(request):
    home_rec = Homedata.objects.all()
    if home_rec:
        data = home_rec[0].Desctiption
        return render(request, 'home.html', {'home_data':data})
    else:
        return render(request, 'home.html')
    

def contact(request):
    return render(request, 'contact.html')

@csrf_exempt
def contact_detail(request):
    if request.method == "POST":
        if (request.POST['name'] is not None and request.POST['name'] != '') and (request.POST['email'] is not None and request.POST['email'] != '') and (request.POST['get_subject'] is not None and request.POST['get_subject'] != '') and (request.POST['get_message'] is not None and request.POST['get_message'] != ''):
            name = request.POST['name']
            email = request.POST['email']
            get_subject = request.POST['get_subject']
            get_message = request.POST['get_message']
            from .models import contact_details
            conta_data = contact_details()
            conta_data.shopname = shop
            conta_data.fullname = name
            conta_data.email = email
            conta_data.subject_data = get_subject
            conta_data.message_data = get_message
            conta_data.save()
        else:
            return HttpResponse("Some Fields Are Blank")
        return HttpResponse("data added")

def policy(request):
    policy_rec = Policy_data.objects.all()
    if len(policy_rec)!=0:
        pol_title = policy_rec[0].policy_title
        pol_desc = policy_rec[0].policy_description
        return render(request, 'privacy_policy.html', {'p_til': pol_title, 'p_desc': pol_desc})
    else:
        return render(request, 'privacy_policy.html')


def instruct(request):
    return render(request, 'instruction.html')


def pricing(request):
    return render(request, 'price.html')


def refundwocurency(order_id, data_dict):
    main_dict = dict()
    if shop is not None and shop != '':
        data_installer = installer.objects.filter(shop=shop)
        if data_installer:
            token = data_installer[0].access_token
        else:
            message = "shop data not found in database"
            main_dict['error_message'] = message
            return HttpResponse(json.dumps(main_dict), content_type="application/json")

    url = "https://%s:%s@%s/admin/api/%s/orders/%s/refunds/calculate.json" % (API_KEY, SHARED_SECRET, shop, API_VERSION, order_id)

    header = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json",
        "client_id": API_KEY,
        "client_secret": SHARED_SECRET
    }
    
    my_data = {
        "refund": {
            "shipping": {
            "full_refund": "false"
            },
            "refund_line_items": data_dict
        }
    }

    r = requests.post(url=url, headers=header, json=my_data)
    c_data = json.loads(r.text)
    return c_data

def create_refund(order_id, note, da):
    my_json = dict()
    
    if shop is not None and shop != '':
        data_installer = installer.objects.filter(shop=shop)
        if data_installer:
            token = data_installer[0].access_token
        else:
            message = "shop data not found in database"
            main_dict['error_message'] = message
            return HttpResponse(json.dumps(main_dict), content_type="application/json")

    url = "https://%s:%s@%s/admin/api/%s/orders/%s/refunds.json" % (API_KEY, SHARED_SECRET, shop, API_VERSION, order_id)

    header = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json",
        "client_id": API_KEY,
        "client_secret": SHARED_SECRET
    }

    my_json["refund"] = da
    my_json["refund"]['transactions'][0]['kind'] = 'refund'
    my_json['refund']['notify'] = 'true'
    my_json['refund']['note'] = note
    r = requests.post(url=url, headers=header, json=my_json)
    c_json = json.loads(r.text)
    return c_json

@csrf_exempt
@xframe_options_exempt
def returnapprove(request):
    count = 0
    final_dict = {}
    my_dict = dict()
    if (request.GET.get('orderid') is not None and request.GET.get('orderid')!='') and (request.GET.get('vari') is not None and request.GET.get('vari')!='') and (request.GET.get('id') is not None and request.GET.get('id')!='') and (request.GET.get('quantity') is not None and request.GET.get('quantity')!=''):
        note = request.GET.get('note')
        orderid = request.GET.get('orderid')

        if ((',' in request.GET.get('id')) and (',' in request.GET.get('quantity')) and (',' in request.GET.get('vari'))):
            itemid = request.GET.get('id').split(',')
            quan = request.GET.get('quantity').split(',')
            itemvari = request.GET.get('vari').split(',')
        else:
            itemid = request.GET.get('id')
            count = 999
            quan = request.GET.get('quantity')
            itemvari = request.GET.get('vari')

            
        if ((',' in request.GET.get('id')) and (',' in request.GET.get('quantity')) and (',' in request.GET.get('vari'))):
            if len(itemid) == len(quan) == len(itemvari):
                item_da = ','.join(itemid)
                qunt_da = ','.join(quan)
                itemvari_da = ','.join(itemvari)
            else:
                message = "something went wrong!"
                my_dict['error_message'] = message
                return HttpResponse(json.dumps(my_dict), content_type="application/json")
        else:
            item_da = itemid
            count = 999
            qunt_da = quan
            itemvari_da = itemvari


        data_list = list()
    
        if count == 999:
            data = dict()
            data['line_item_id'] = item_da
            data['quantity'] = qunt_da
            data['restock_type'] = "return"
            data_list.append(data)
        else:
            if len(itemid) == len(quan) == len(itemvari):
                for x in itemid:
                    data = dict()
                    for y in  quan:
                        data_y = y
                    data_x = x

                    data['line_item_id'] = data_x
                    data['quantity'] = data_y
                    data['restock_type'] = "return"
                    data_list.append(data)              
            else:
                message = "Invalid Item!"
                my_dict['error_message'] = message
                return HttpResponse(json.dumps(my_dict), content_type="application/json")
        main_dict = dict()
        final_dict = data_list
        calculate_refund = refundwocurency(order_id=orderid, data_dict=final_dict)

        main_dict['shipping'] = calculate_refund['refund']['shipping']
        main_dict['refund_line_items'] = calculate_refund['refund']['refund_line_items']
        main_dict['transactions'] = calculate_refund['refund']['transactions']
        main_dict['currency'] = calculate_refund['refund']['currency']
        refund_process = create_refund(order_id=orderid, note=note, da=main_dict)

        data_id = ''
        for refund_x in refund_process['refund']['transactions']:
            if refund_x['status'] == "success":
                from .models import detail_order
                get_data_rec = detail_order.objects.filter(Q(shop_data=shop), Q(ordid=str(orderid)), Q(variants=str(itemvari_da)), Q(quantity=str(qunt_da)))
                if get_data_rec:
                    data_id = get_data_rec[0].id

        if data_id:
            from .models import detail_order
            date = datetime.datetime.now()
            get_data_update = detail_order.objects.filter(id=data_id).update(status="APPROVED", upda_date=date, order_note=note)
            my_dict['status'] = "APPROVED"
            return HttpResponse(json.dumps(my_dict), content_type="application/json")
        else:
            message = "No data Found!"
            my_dict['error_message'] = message
            return HttpResponse(json.dumps(my_dict), content_type="application/json")    
    return HttpResponse(final_dict)

def rejected(request):
    data_id = ''
    count = 0
    my_dict = dict()
    main_dict = dict()
    
    if (request.GET.get('orderid') is not None and request.GET.get('orderid')!='') and (request.GET.get('vari') is not None and request.GET.get('vari')!='') and (request.GET.get('id') is not None and request.GET.get('id')!='') and (request.GET.get('quantity') is not None and request.GET.get('quantity')!=''):
        note = request.GET.get('note')
        orderid = request.GET.get('orderid')

        if ((',' in request.GET.get('id')) and (',' in request.GET.get('quantity')) and (',' in request.GET.get('vari'))):
            itemid = request.GET.get('id').split(',')
            quan = request.GET.get('quantity').split(',')
            itemvari = request.GET.get('vari').split(',')
        else:
            itemid = request.GET.get('id')
            count = 999
            quan = request.GET.get('quantity')
            itemvari = request.GET.get('vari')

            
        if ((',' in request.GET.get('id')) and (',' in request.GET.get('quantity')) and (',' in request.GET.get('vari'))):
            if len(itemid) == len(quan) == len(itemvari):
                item_da = ','.join(itemid)
                qunt_da = ','.join(quan)
                itemvari_da = ','.join(itemvari)
               
            else:
                message = "something went wrong!"
                my_dict['error_message'] = message
                return HttpResponse(json.dumps(my_dict), content_type="application/json")
        else:
            item_da = itemid
            count = 999
            qunt_da = quan
            itemvari_da = itemvari
           
        if count == 999:
            from .models import detail_order
            get_data_rec = detail_order.objects.filter(Q(shop_data=shop), Q(ordid=str(orderid)), Q(variants=str(itemvari_da)))
            if get_data_rec:

                data_id = get_data_rec[0].id
            else:
                message = "No data Found!"
                my_dict['error_message'] = message
                return HttpResponse(json.dumps(my_dict), content_type="application/json")
        else:
            from .models import detail_order
            get_data_rec = detail_order.objects.filter(Q(shop_data=shop), Q(ordid=str(orderid)), Q(variants=str(itemvari_da)))
            if get_data_rec:

                data_id = get_data_rec[0].id
            else:
                message = "No data Found!"
                my_dict['error_message'] = message
                return HttpResponse(json.dumps(my_dict), content_type="application/json")

        if data_id:
            from .models import detail_order
            date = datetime.datetime.now()
            get_data_update = detail_order.objects.filter(id=data_id).update(status="REJECTED", upda_date=date, order_note=note)
            my_dict['status'] = "REJECTED"
            return HttpResponse(json.dumps(my_dict), content_type="application/json")
        else:
            message = "No data Found!"
            my_dict['error_message'] = message
            return HttpResponse(json.dumps(my_dict), content_type="application/json")    
    return render(request, 'order.html')

@xframe_options_exempt
def order_page(request):
    '''
    order.html data parsing
    '''
    from django.core.paginator import Paginator
    from .models import detail_order
    posts = detail_order.objects.all()
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)  
    
    ''' BELOW FUNCTION CALL FOR GET ORDER VARIANT BY IT'S ID '''
    main_dict = dict()
    main_sub_dict = dict()

    for x in posts:
        o_page_id = x.ordid
        print(o_page_id, "pages")
        if (',' in x.variants):
            y =  x.variants.split(',')
        else:
            y = x.variants
        
        if (',' in x.quantity):
            q_qunt = x.quantity.split(',')
        else:
            q_qunt = x.quantity

        c_json_data = ''
        if o_page_id is not None and o_page_id != '':
            if shop is not None and shop != '':
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

                    main_sub_dict[x.id] = {'datavaritan':y, 'dataqnt':q_qunt,'variants':c_json_data['order']['line_items']}
                    main_dict = main_sub_dict.copy() 
    variant_data = main_dict
    # print(variant_data, "variants_dict")
    return render(request, 'order.html', {'order_requests': posts, 'line_items': variant_data})


def token(code, shop):

    ur = "https://" + shop + "/admin/oauth/access_token"

    s = {
        "client_id": API_KEY,
        "client_secret": SHARED_SECRET,
        "code": code
    }
    r = requests.post(url=ur, json=s)
    x = json.loads(r.text)
    return x


def get_token(request):  # if hmac is get then go to welcome.html otherwise go to index.html
    if request.method == "GET":
        if request.GET.get('hmac') is not None:
            code = request.GET.get('code')
            shop = request.GET.get('shop')
            a = token(code=code, shop=shop)

        else:
            HttpResponse("Don't Get HMAC")
    return a


def installation(request):
    # global main
    if request.method == "POST":
        url = request.POST['shop']
        s_url = url.strip('/')
        # print(s_url)
        api_key = API_KEY
        # print(api_key)
        link = '%s/admin/oauth/authorize?client_id=%s&redirect_uri=https://python.penveel.com/final&scope=read_products,write_products,read_customers,write_customers,read_orders,write_orders' % (s_url, api_key)
        # print(link)
        li = link.strip("/")
        # print(li)
        # URL = li
        redirect = HttpResponseRedirect(f'{li}')
        # ds = redirect
        # print(ds)
    return redirect


def redirect(request):
    if request.GET.get('shop') is not None:
        shop = request.GET.get('shop')
        redir = HttpResponseRedirect(redirect_to='https://' + shop + '/admin/apps/productreturn')
        # if redir.status_code == 302:
        #     return render(request, 'index.html')
    return redir


def getid(setshop, accesstoken):
    my_dict = dict()
    url = "https://" + setshop + "/admin/api/2020-07/shop.json"
    headers = {
        "X-Shopify-Access-Token": accesstoken,
        "Content-Type": "application/json",
        "client_id": API_KEY,
        "client_secret": SHARED_SECRET
    }
    r = requests.get(url, headers=headers)
    # print(r.text)
    result = json.loads(r.text)
    # print(result, "hello id")
    my_dict["id"] = result['shop']['id']
    my_dict["store_name"] = result['shop']['domain']
    return my_dict


def unistaller_second(request):

    # shop_name = request.GET.get('shop')
    # print(shop_name, "uninstaller_second shop")
    if len(shop) != 0:
        webrec = installer.objects.filter(shop=shop)
        if webrec:
            token = webrec[0].access_token
            hmac_data = webrec[0].hmac
        else:
            HttpResponse("Invalid shop detail")

        url = "https://" + shop + "/admin/api/2020-07/webhooks.json"

        # print(url, "url data2")
        # print(token, "token2")
        # print(hmac_data, "hmac2")

        headers = {
            'X-Shopify-Access-Token': token,
            'X-Shopify-Topic': 'app/uninstalled',
            'X-Shopify-Hmac-Sha256': hmac_data,
            'X-Shopify-Shop-Domain': shop,
            'X-Shopify-API-Version': API_VERSION
        } 

        my = {
            "webhook": {
                "topic": "app/uninstalled",
                "address": 'https://python.penveel.com/uninstall',
                "format": "json"
            }
        }
        # print(API_KEY, SHARED_SECRET)
        r = requests.post(url=url, json=my, headers=headers)
        # print(r, "Webh")
        c = json.loads(r.text)
        return HttpResponse(json.dumps(c), content_type="application/json")


@xframe_options_exempt
def final(request):
    if request.GET.get('hmac') is not None:
        hmac = request.GET.get('hmac')
        global shop
        shop = request.GET.get('shop')
        if request.GET.get('code') is not None:
            code = request.GET.get('code')
            if len(code) != 0:
                record = installer.objects.filter(shop=shop)
                if record:
                    get_code = record[0].code

                    get_access_token = record[0].access_token
                    return redirect(request=request)
                else:
                    accesstoken = token(code=code, shop=shop)
                    rec = installer()
                    rec.shop = shop
                    rec.code = code
                    rec.hmac = hmac
                    rec.access_token = accesstoken['access_token']
                    rec.save()

                    # unistaller(request=request)
                    unistaller_second(request=request)
                    return redirect(request=request)
                return redirect(request=request)
        else:
            record = installer.objects.filter(shop=shop)
            if record:
                getaccess = record[0].access_token
                getshop = record[0].shop

                # samu = uninstall(shop_name=shop, token=getaccess)
                # get_data = getid(setshop=getshop, accesstoken=getaccess)
                # print(get_data)
                return render(request, 'final.html')
            else:
                return HttpResponse("No Data Found")
    else:
        return render(request, 'login.html')