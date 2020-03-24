import requests
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')
import io
with io.open('nagpur1.csv','w',encoding='utf-8') as f1:
    f1.write('id,name,avgRating,address-,cuisines,cost for two'+'\n')
    f1.close()


headers = {
        'authority': 'www.swiggy.com','__fetch_req__': 'true','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36','content-type': 'application/json',
        'accept': '*/*','sec-fetch-site': 'same-origin','sec-fetch-mode': 'cors','referer': 'https://www.swiggy.com/nagpur?page=2','accept-encoding': 'gzip, deflate, br','accept-language': 'en-US,en;q=0.9',
        'cookie': '__SW=HoKO60a2TJk5HNQSliXxoCrZ5HWyjz2D; _device_id=0894e1e8-2d2b-4895-9d14-d612cabd8650; _gcl_aw=GCL.1579978783.EAIaIQobChMImru0zref5wIVGg4rCh0rPQtzEAAYASAAEgJTR_D_BwE; _gcl_au=1.1.537344729.1579978783; _ga=GA1.2.965912730.1579978783; _gac_0=1.1579978783.EAIaIQobChMImru0zref5wIVGg4rCh0rPQtzEAAYASAAEgJTR_D_BwE; optimizelyEndUserId=lo_BOlBS0CG5G4W; order_source=Google-Sok; order_medium=CPC; order_campaign=google_search_sok_food_na_narm_order_web_m_web_clubbedcities_v3_welcome50_neev_competitor_newuser_competitor_bmm; __cfduid=d717f5774b2b57fe77139c34294ac76211582631293; fontsLoaded=1; userLocation=%7B%22lat%22%3A%2221.11021%22%2C%22lng%22%3A%2279.047786%22%2C%22address%22%3A%22Deendayal%20Nagar%2C%20Nagpur%2C%20Maharashtra%20440022%2C%20India%22%2C%22area%22%3A%22Deendayal%20Nagar%22%2C%22id%22%3A%2233379943%22%7D; _gid=GA1.2.1343453737.1582728551; _parsely_session={%22sid%22:2%2C%22surl%22:%22https://bytes.swiggy.com/swiggy-rest-opinionated-crud-library-on-spring-a78715074eb4%22%2C%22sref%22:%22https://www.google.com/%22%2C%22sts%22:1582728550837%2C%22slts%22:1580357610757}; _parsely_visitor={%22id%22:%22pid=d60e514ce147de51e436db833c907f56%22%2C%22session_count%22:2%2C%22last_session_ts%22:1582728550837}; _guest_tid=28fd9621-459a-4e16-9a2d-6daf8f88adba; _sid=lbw58cea-759d-47df-89df-b6ebbc1e349d; _gat_UA-53591212-4=1',
}

params = (
        ('page', '0'),('ignoreServiceability', 'true'),('lat', '21.145800'),('lng', ' 79.088158'),('pageType', 'SEE_ALL'),('sortBy', 'RELEVANCE'),('page_type', 'DESKTOP_SEE_ALL_LISTING'),
)

response = requests.get('https://www.swiggy.com/dapi/restaurants/list/v5', headers=headers, params=params)
data = response.json()
page_nos = data['data']['pages']

pag = 0
for i in range(page_nos):
    headers = {
        'authority': 'www.swiggy.com','__fetch_req__': 'true','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36','content-type': 'application/json',
        'accept': '*/*','sec-fetch-site': 'same-origin','sec-fetch-mode': 'cors','referer': 'https://www.swiggy.com/nagpur?page=2','accept-encoding': 'gzip, deflate, br','accept-language': 'en-US,en;q=0.9',
        'cookie': '__SW=HoKO60a2TJk5HNQSliXxoCrZ5HWyjz2D; _device_id=0894e1e8-2d2b-4895-9d14-d612cabd8650; _gcl_aw=GCL.1579978783.EAIaIQobChMImru0zref5wIVGg4rCh0rPQtzEAAYASAAEgJTR_D_BwE; _gcl_au=1.1.537344729.1579978783; _ga=GA1.2.965912730.1579978783; _gac_0=1.1579978783.EAIaIQobChMImru0zref5wIVGg4rCh0rPQtzEAAYASAAEgJTR_D_BwE; optimizelyEndUserId=lo_BOlBS0CG5G4W; order_source=Google-Sok; order_medium=CPC; order_campaign=google_search_sok_food_na_narm_order_web_m_web_clubbedcities_v3_welcome50_neev_competitor_newuser_competitor_bmm; __cfduid=d717f5774b2b57fe77139c34294ac76211582631293; fontsLoaded=1; userLocation=%7B%22lat%22%3A%2221.11021%22%2C%22lng%22%3A%2279.047786%22%2C%22address%22%3A%22Deendayal%20Nagar%2C%20Nagpur%2C%20Maharashtra%20440022%2C%20India%22%2C%22area%22%3A%22Deendayal%20Nagar%22%2C%22id%22%3A%2233379943%22%7D; _gid=GA1.2.1343453737.1582728551; _parsely_session={%22sid%22:2%2C%22surl%22:%22https://bytes.swiggy.com/swiggy-rest-opinionated-crud-library-on-spring-a78715074eb4%22%2C%22sref%22:%22https://www.google.com/%22%2C%22sts%22:1582728550837%2C%22slts%22:1580357610757}; _parsely_visitor={%22id%22:%22pid=d60e514ce147de51e436db833c907f56%22%2C%22session_count%22:2%2C%22last_session_ts%22:1582728550837}; _guest_tid=28fd9621-459a-4e16-9a2d-6daf8f88adba; _sid=lbw58cea-759d-47df-89df-b6ebbc1e349d; _gat_UA-53591212-4=1',
    }

    params = (
        ('page', '0'),('ignoreServiceability', 'true'),('lat', '21.145800'),('lng', ' 79.088158'),('pageType', 'SEE_ALL'),('sortBy', 'RELEVANCE'),('page_type', 'DESKTOP_SEE_ALL_LISTING'),
    )

    response = requests.get('https://www.swiggy.com/dapi/restaurants/list/v5', headers=headers, params=params)
    
    pag += 1
    print("page no is "+ str(pag))
    data1 = response.json()
    data1 = data1['data']['cards']

    for i in range(len(data1)):
        id = data1[i]['data']['data']['id']
        name = data1[i]['data']['data']['name']
        avgRating = data1[i]['data']['data']['avgRating']
        address = data1[i]['data']['data']['address']
        address = address.replace(',',';')
        cuisines = data1[i]['data']['data']['cuisines']
        cuisines = str(cuisines)
        cuisines = cuisines.replace(',',' ')
        costForTwo= data1[i]['data']['data']['costForTwo']
        costForTwo = str(costForTwo)
        scrapped_data = (str(id)+","+name+","+avgRating+","+address+","+str(cuisines)+","+costForTwo)
        with io.open('nagpur1.csv','a',encoding='utf-8') as f2:
            f2.write(scrapped_data+ '\n')
            f2.close()


# headers = {
#         'authority': 'www.swiggy.com','__fetch_req__': 'true','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36','content-type': 'application/json',
#         'accept': '*/*','sec-fetch-site': 'same-origin','sec-fetch-mode': 'cors','referer': 'https://www.swiggy.com/nagpur?page=2','accept-encoding': 'gzip, deflate, br','accept-language': 'en-US,en;q=0.9',
#         'cookie': '__SW=HoKO60a2TJk5HNQSliXxoCrZ5HWyjz2D; _device_id=0894e1e8-2d2b-4895-9d14-d612cabd8650; _gcl_aw=GCL.1579978783.EAIaIQobChMImru0zref5wIVGg4rCh0rPQtzEAAYASAAEgJTR_D_BwE; _gcl_au=1.1.537344729.1579978783; _ga=GA1.2.965912730.1579978783; _gac_0=1.1579978783.EAIaIQobChMImru0zref5wIVGg4rCh0rPQtzEAAYASAAEgJTR_D_BwE; optimizelyEndUserId=lo_BOlBS0CG5G4W; order_source=Google-Sok; order_medium=CPC; order_campaign=google_search_sok_food_na_narm_order_web_m_web_clubbedcities_v3_welcome50_neev_competitor_newuser_competitor_bmm; __cfduid=d717f5774b2b57fe77139c34294ac76211582631293; fontsLoaded=1; userLocation=%7B%22lat%22%3A%2221.11021%22%2C%22lng%22%3A%2279.047786%22%2C%22address%22%3A%22Deendayal%20Nagar%2C%20Nagpur%2C%20Maharashtra%20440022%2C%20India%22%2C%22area%22%3A%22Deendayal%20Nagar%22%2C%22id%22%3A%2233379943%22%7D; _gid=GA1.2.1343453737.1582728551; _parsely_session={%22sid%22:2%2C%22surl%22:%22https://bytes.swiggy.com/swiggy-rest-opinionated-crud-library-on-spring-a78715074eb4%22%2C%22sref%22:%22https://www.google.com/%22%2C%22sts%22:1582728550837%2C%22slts%22:1580357610757}; _parsely_visitor={%22id%22:%22pid=d60e514ce147de51e436db833c907f56%22%2C%22session_count%22:2%2C%22last_session_ts%22:1582728550837}; _guest_tid=28fd9621-459a-4e16-9a2d-6daf8f88adba; _sid=lbw58cea-759d-47df-89df-b6ebbc1e349d; _gat_UA-53591212-4=1',
#         }

#         params = (
#             ('page', '0'),('ignoreServiceability', 'true'),('lat', '21.145800'),('lng', ' 79.088158'),('pageType', 'SEE_ALL'),('sortBy', 'RELEVANCE'),('page_type', 'DESKTOP_SEE_ALL_LISTING'),
#         )

#         response = requests.get('https://www.swiggy.com/dapi/restaurants/list/v5', headers=headers, params=params)
#         response = response.text
#         data = json.loads(response)
#         page_nos = data['data']['pages']

#         pag = 0
#         for i in range(page_nos):
#             headers = {
#                 'authority': 'www.swiggy.com','__fetch_req__': 'true','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36','content-type': 'application/json',
#                 'accept': '*/*','sec-fetch-site': 'same-origin','sec-fetch-mode': 'cors','referer': 'https://www.swiggy.com/nagpur?page=2','accept-encoding': 'gzip, deflate, br','accept-language': 'en-US,en;q=0.9',
#                 'cookie': '__SW=HoKO60a2TJk5HNQSliXxoCrZ5HWyjz2D; _device_id=0894e1e8-2d2b-4895-9d14-d612cabd8650; _gcl_aw=GCL.1579978783.EAIaIQobChMImru0zref5wIVGg4rCh0rPQtzEAAYASAAEgJTR_D_BwE; _gcl_au=1.1.537344729.1579978783; _ga=GA1.2.965912730.1579978783; _gac_0=1.1579978783.EAIaIQobChMImru0zref5wIVGg4rCh0rPQtzEAAYASAAEgJTR_D_BwE; optimizelyEndUserId=lo_BOlBS0CG5G4W; order_source=Google-Sok; order_medium=CPC; order_campaign=google_search_sok_food_na_narm_order_web_m_web_clubbedcities_v3_welcome50_neev_competitor_newuser_competitor_bmm; __cfduid=d717f5774b2b57fe77139c34294ac76211582631293; fontsLoaded=1; userLocation=%7B%22lat%22%3A%2221.11021%22%2C%22lng%22%3A%2279.047786%22%2C%22address%22%3A%22Deendayal%20Nagar%2C%20Nagpur%2C%20Maharashtra%20440022%2C%20India%22%2C%22area%22%3A%22Deendayal%20Nagar%22%2C%22id%22%3A%2233379943%22%7D; _gid=GA1.2.1343453737.1582728551; _parsely_session={%22sid%22:2%2C%22surl%22:%22https://bytes.swiggy.com/swiggy-rest-opinionated-crud-library-on-spring-a78715074eb4%22%2C%22sref%22:%22https://www.google.com/%22%2C%22sts%22:1582728550837%2C%22slts%22:1580357610757}; _parsely_visitor={%22id%22:%22pid=d60e514ce147de51e436db833c907f56%22%2C%22session_count%22:2%2C%22last_session_ts%22:1582728550837}; _guest_tid=28fd9621-459a-4e16-9a2d-6daf8f88adba; _sid=lbw58cea-759d-47df-89df-b6ebbc1e349d; _gat_UA-53591212-4=1',
#             }

#             params = (
#                 ('page', pag),('ignoreServiceability', 'true'),('lat', '21.145800'),('lng', ' 79.088158'),('str', cuisine),('pageType', 'SEE_ALL'),('sortBy', 'RELEVANCE'),('page_type', 'DESKTOP_SEE_ALL_LISTING'),
#             )
 
#             response = requests.get('https://www.swiggy.com/dapi/restaurants/list/v5', headers=headers, params=params)
#             response = response.text
#             pag += 1
#             #print("page no is "+ str(pag))
#             data1 = json.loads(response)
#             data1 = data1['data']['cards']