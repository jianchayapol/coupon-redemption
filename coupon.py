
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import requests
import simplejson
import json

import datetime, pytz


with open('config.json') as json_file:
    gg_sheet_url = json.load(json_file)['GOOGLE_SHEET_URL']

def time_now():
    tz = pytz.timezone('Asia/Bangkok')
    return str(datetime.datetime.now(tz))[11:19]

def activate_coupon(request):
    coupon_id = request.args.get('id')
    print(coupon_id)
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_url(gg_sheet_url)
    
    worksheet = sheet.get_worksheet(0)
    try:
        cell = worksheet.find(coupon_id)
        r = cell.row
        if worksheet.cell(r,2).value != "Activated":
            worksheet.update_cell(r,2,"Activated")
            worksheet.update_cell(r,3,time_now())
            res={}
            res['status']= coupon_id + " - Activated"
            return (json.dumps(res),200)

    except Exception as e: 
            res={}
            res['status']= "Error: {}".format(e)
            return (json.dumps(res),404)

    return ('Error: Coupon Code Already Redeemed',404)


# activate_coupon()
