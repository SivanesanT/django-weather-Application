from django.shortcuts import render,redirect
import requests
from .models import City
# import json
from django.contrib import messages 
# Create your views here.
def home(request):
    # url='https://api.openweathermap.org/data/2.5/weather?q=salem,id=524901&appid=0c9fce9cb51987d87f699353db3538d6'
    url='https://api.openweathermap.org/data/2.5/weather?q={},id=524901&appid=0c9fce9cb51987d87f699353db3538d6'
    if request.method == 'POST':
        cname=request.POST['name']
        ccity=City.objects.filter(name=cname).count()
        if ccity==0:
            res=requests.get(url.format(cname)).json()
            # print(res)
            if res['cod']==200:
                City.objects.create(name=cname)
                messages.success(request, cname  + " Added Successfully......."  )
            else:
                messages.error(request,"This City Known doesn't Exits.....")
        else:
            messages.error(request,"City Alredy Exits....!!!")

    cityes=City.objects.all().order_by('-id')
    # Reserved.objects.filter(client=client_id).order_by('-check_in')

    data=[]
    for city in cityes:
        run=requests.get(url.format(city)).json()
        tet=run['main']['temp']
        tea=tet/10
        city_whether={
            'cityname': city,
            'temp': tea,
            'desc': run['weather'][0]['description'],
            'country': run['sys']['country'],
            'icon': run['weather'][0]['icon'],
        }
        data.append(city_whether)

    return render(request, 'index.html',{ 'data':data })

def citydelete(request,cname):
    City.objects.get(name=cname).delete()
    messages.success(request,cname +" Removed Successfully")
    return redirect('home')

    # city='karachi'
    # res=requests.get(url.format(city)).json()
    # print(res['main']['temp'])

    # gold and silver api------
    # https://www.goldapi.io/api/:symbol/:currency/:date?
    # jsi='https://www.goldapi.io/api/XAU/INR'
    # jsj='https://www.goldapi.io/api/XAG/INR'
    # headers = {
    # "x-access-token": "goldapi-4bxdrrlnu99py7-io"
    # }
    # re=requests.get(jsi,headers=headers).json()
    # print(re)
    # g=re['price_gram_24k']
    # gs=g*6.6/100
    # gl=g+gs
    # print(gl)
    # ren=requests.get(jsj,headers=headers).json()
    # s=ren['price_gram_24k']
    # ss=s*26/100
    # sl=s+ss
    # print(sl)

    # ['price_gram_22k']*100
    # City using the gold price-------
    # url = "https://gold-silver-rates-india.p.rapidapi.com/api/Fetch-Gold-Silver-City/"
    # querystring = {"city":"chennai"}
    # headers = {
    #     "X-RapidAPI-Key": "6fcc89376cmshaf688c65da04f52p176a9bjsnd750206b79ff",
    #     "X-RapidAPI-Host": "gold-silver-rates-india.p.rapidapi.com"
    # }
    # response = requests.get(url, headers=headers, params=querystring).json()
    # print(response['gold_rate'])
    # gr=response['gold_rate']
    # sr=response['silver_rate']
    # ggr=gr/10
    # ssr=sr/1000
    # print(f'gold rate : {ggr}')
    # print(f'silver rate:  {ssr}')
    # print(response)   
    
    # return render(request, 'index.html')