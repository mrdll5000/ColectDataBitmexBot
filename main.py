from oauth2client.service_account import ServiceAccountCredentials
import gspread
import ccxt
from datetime import datetime
import time
from config import sheet_id


def write_to_excel(list=[],sheet_id='1QQgx_j19FIlrm2fau9t_pZv3A3EchFXHX3M0s8TMcPA'):
    scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
    #sheet_id = 1QQgx_j19FIlrm2fau9t_pZv3A3EchFXHX3M0s8TMcPA
    credentials = ServiceAccountCredentials.from_json_keyfile_name('kardia-714ac37990e2.json', scope)

    gc = gspread.authorize(credentials)

    sht1 = gc.open_by_key(sheet_id)
    worksheet=sht1.sheet1
    worksheet.insert_row(list,index=2)
#write_to_excel(["a","b","c","d"])
def fetch_order_book(pair,name):
    exchange_class = getattr(ccxt, name)
    exchange = exchange_class({

        'timeout': 30000,
        'enableRateLimit': True,
    })
    try:
        orderbook = exchange.fetch_order_book (pair)
    except Exception as err:
        print(err)
        time.sleep(60)
        get_data()
    bid = orderbook['bids'][0] if len(orderbook['bids']) > 0 else None
    return bid

def get_data():
    for sheet in sheet_id:
        ticker=fetch_order_book(sheet['name'],"bitmex")
        date_time=str(datetime.now())
        excel=[]
        excel.append(str(date_time))
        excel.append("XRPH19")
        excel.append(ticker[0])#piece
        excel.append(ticker[1])#volume
        print(excel)
        try:
            write_to_excel(excel,sheet_id=sheet['id'])
        except Exception as err:
            print(err)
            pass
def run():
    while 1:
        get_data()
        time.sleep(3600)

if __name__=="__main__":
    run()