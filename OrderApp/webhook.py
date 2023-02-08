import requests
import json
import base64
from .models import installer, uninstall_data
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import hmac
import datetime
import hashlib

API_KEY = "1c86866d8c638b28da99bbdfe3cd5fce"
SHARED_SECRET = "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"
API_VERSION = "2021-01"


class WebhookApi:

    @csrf_exempt
    def webhook_uninstall(request):
        print(request, "REQUEST MAIN")
        if request.method == 'POST':
            if ((request.body != "") and (request.headers.get('X-Shopify-Hmac-Sha256') != "")):
                data = request.body
                hmac_header = request.headers.get('X-Shopify-Hmac-Sha256')
                digest = hmac.new(SHARED_SECRET.encode('utf-8'), data, hashlib.sha256).digest()
                computed_hmac = base64.b64encode(digest)
                if computed_hmac == hmac_header.encode('utf-8'):
                    topic = request.headers.get('X-Shopify-Topic')
                    shop_url = request.headers.get('X-Shopify-Shop-Domain')
                    if shop_url != "":
                        uninstallap = installer.objects.filter(shop=str(shop_url))
                        if uninstallap:
                            date = datetime.datetime.now()
                            data = uninstall_data()
                            data.uninstall_shop = uninstallap[0].shop
                            data.uninstall_time = date
                            data.save()
                            uninstallap.delete()
                    else:
                        return HttpResponse("NO shop domain")
                else:
                    return HttpResponse("FALSE")
        return HttpResponse('Success')