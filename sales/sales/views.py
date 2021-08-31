from django.shortcuts import render,redirect
from sales.model import TotalSalesData, TotalOpalData, NonMover
from django.http import JsonResponse,HttpResponse
from datetime import datetime, timedelta
from django.db import connection
import pandas as pd
from functools import reduce
import numpy as np
import csv
from django.db.models import Sum
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json




downloadData = ""
fileName = "Data"

def logout_view(request):
    logout(request)
    return redirect('login_view')
    
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('/')
    else: 
        # print("l")
        form = AuthenticationForm()
    return render(request,'sales/login.html',{'form':form})


@login_required(login_url='login_view')
def show(request):
    if request.method == 'POST':
        from_date = request.POST.get('startdate')
        to_date = request.POST.get('todate')
        searchresult = TotalSalesData.objects.filter(date__range=(from_date,to_date))
    

        result = (searchresult.values('sales_channel').annotate(line_total=Sum('line_total')).order_by())
        result_dict = {}
        for i in range(0,len(result)):
            channel = result[i]['sales_channel']
            sale = result[i]['line_total']
            result_dict.update({channel:sale})
   
        

        wayFair = result_dict.get('Wayfair', 0)
        overstock = result_dict.get('Overstock', 0)
        amazonDS = result_dict.get('Amazon VC DSV', 0)
        homeDepot = result_dict.get('Home Depot', 0)
        virVenture = result_dict.get('Vir Venture', 0)
        target = result_dict.get('Target', 0)
        lows = result_dict.get('Lowes', 0)
        walmart = result_dict.get('Walmart', 0)
        doba = result_dict.get('Doba', 0)
        casagear = result_dict.get('Casagear', 0)
        openSky = result_dict.get('Morecommerce', 0)
        amazonFBM = result_dict.get('Manhattan Lane -Amazon SC', 0)
        benzaraWholesale = result_dict.get('Benzara', 0)
        bedBath = result_dict.get('Bed Bath & Beyond', 0)
        uberBazar = result_dict.get('Uber Bazaar', 0)
        cymax = result_dict.get('Cymax', 0)
        heyneedle = result_dict.get('Hayneedle', 0)
        amazonUS = result_dict.get('Amazon Warehouse', 0)
        ojcommer = result_dict.get('OJ COMMERCE', 0)
        ebay = result_dict.get('Ebay', 0)
        unbeatble = result_dict.get('Unbeatable', 0)
        kroger = result_dict.get('Kroger', 0)
        amazonCA = result_dict.get('Amazon CA Warehouse', 0)
        pier1 = result_dict.get('Pier1', 0)
        
        
        global downloadData
        global fileName
        downloadData = searchresult 
        fileName = str(from_date) +"-"+str(to_date)
        print(type(searchresult))
        return render(request,'sales/front.html',{
            'show':True,
            'data':searchresult[0:100],'dollar':"$",
            'wayfair':round(wayFair,2),
            'overstock':round(overstock,2),
            'amazonDS':round(amazonDS,2),
            'homeDepot':round(homeDepot,2),
            'virVenture':round(virVenture,2),
            'target':round(target,2),
            'lowes': round(lows,2),
            'walmart':round(walmart,2),
            'doba':round(doba,2),
            'casagear': round(casagear,2),
            'opensky':round(openSky,2),
            'amazonFBM':round(amazonFBM,2),
            'benzara':round(benzaraWholesale,2),
            'bed':round(bedBath,2),
            'uberBazar':round(uberBazar,2),
            'cymax':round(cymax,2),
            'hayneedle':round(heyneedle,2),
            'amazonUS':round(amazonUS,2),
            'ojCommer':round(ojcommer,2),
            'ebay':round(ebay,2),
            'unbeatbale':round(unbeatble,2),
            'kroger':round(kroger,2),
            'amazonCA':round(amazonCA,2),
            'pier1':round(pier1,2)
        })  
    else:
        return render(request,"sales/front.html")   
@login_required(login_url='login_view')
def sales(request): 
    if request.method == 'POST':
        global downloadData
        global fileName
        from_date = request.POST.get('startdate')
        to_date = request.POST.get('todate')
        channelName = request.POST.get('channelName')
        category = request.POST.get('cat')

        searchresult = TotalSalesData.objects.filter(date__range=(from_date,to_date))


        
        if channelName == 'None' and category == 'Total':
            dic = {}
            result = searchresult.values('sales_channel').annotate(line_total=Sum('line_total')).order_by()
            result_dict = {}
            for i in range(0,len(result)):
                channel = result[i]['sales_channel']
                sale = result[i]['line_total']
                result_dict.update({channel:sale})

            result_dict = dict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True))
          
            channels = []
            lineTotal = []
            for key, value in result_dict.items():
                channels.append(key)
                lineTotal.append(value)

           
           
            text = category + " Sales Data"

            downloadData = searchresult
            fileName = str(from_date)+"-"+str(to_date)+" "+str(category)

            return render(request,'sales/sales.html',{'labels':channels,'data':lineTotal,'salesData':searchresult[0:100],'text':text,'show':True})

        elif channelName == 'vendor' and category == 'Total':
            dic = {}
            print(channelName)
            result = searchresult.values('vendor').annotate(line_total=Sum('line_total')).order_by()
            result_dict = {}
            for i in range(0,len(result)):
                channel = result[i]['vendor']
                sale = result[i]['line_total']
                result_dict.update({channel:sale})

            result_dict = dict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True))
          
            channels = []
            lineTotal = []
            for key, value in result_dict.items():
                channels.append(key)
                lineTotal.append(value)

           
           
            text = channelName + " Sales Data"

            downloadData = searchresult
            fileName = str(from_date)+"-"+str(to_date)+" "+str(category)

            return render(request,'sales/sales.html',{'labels':channels,'data':lineTotal,'salesData':searchresult[0:100],'text':text,'show':True}) 

        elif channelName == 'vendor' and category != 'Total':
            searchresult = searchresult.filter(vendor_type__contains=category)
            dic = {}
            

            result = searchresult.values('vendor').annotate(line_total=Sum('line_total')).order_by()
            result_dict = {}
            for i in range(0,len(result)):
                channel = result[i]['vendor']
                sale = result[i]['line_total']
                result_dict.update({channel:sale})
            result_dict = dict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True))
            channels = []
            lineTotal = []
            for key, value in result_dict.items():
                channels.append(key)
                lineTotal.append(value)


            
            text = category+" "+ channelName+" "+ "Sales Data"

            downloadData = searchresult
            fileName = str(category)+" "+str(from_date)+"-"+str(to_date)
            return render(request,'sales/sales.html',{'labels':channels,'data':lineTotal,'salesData':searchresult[0:100],'text':text,'show':True})

        elif channelName != 'None' and category == 'Total':
            finalResult = searchresult.filter(sales_channel__contains= channelName)
        
            result = finalResult.values('vendor').annotate(line_total=Sum('line_total')).order_by()
            result_dict = {}
            for i in range(0,len(result)):
                ven = result[i]['vendor']
                sale = result[i]['line_total']
                result_dict.update({ven:sale})

            result_dict = dict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True))
         
            vendors = []
            values = []
            for key, value in result_dict.items():
                vendors.append(key)
                values.append(value)

         
            text = channelName +" "+category+" Sales Data"

            downloadData = finalResult
            fileName = str(channelName)+" "+str(from_date)+"-"+str(to_date)
            return render(request,'sales/sales.html',{'vendor':vendors,'values':values,'salesData':finalResult[0:100],'text':text,'show':True})

        elif channelName == 'None' and category != 'Total':
            searchresult = searchresult.filter(vendor_type__contains=category)
            dic = {}
            

            result = searchresult.values('sales_channel').annotate(line_total=Sum('line_total')).order_by()
            result_dict = {}
            for i in range(0,len(result)):
                channel = result[i]['sales_channel']
                sale = result[i]['line_total']
                result_dict.update({channel:sale})
            result_dict = dict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True))
            channels = []
            lineTotal = []
            for key, value in result_dict.items():
                channels.append(key)
                lineTotal.append(value)


            
            text = category + " Sales Data"

            downloadData = searchresult
            fileName = str(category)+" "+str(from_date)+"-"+str(to_date)
            return render(request,'sales/sales.html',{'labels':channels,'data':lineTotal,'salesData':searchresult[0:100],'text':text,'show':True})

        elif channelName != 'None' and category != 'Total':

            finalResult = searchresult.filter(sales_channel__contains= channelName)
            finalResult = finalResult.filter(vendor_type__contains=category)
        
            channelDic = {}
            channle= []
            
           
            result = finalResult.values('vendor').annotate(line_total=Sum('line_total')).order_by()
            result_dict = {}
            for i in range(0,len(result)):
                ven = result[i]['vendor']
                sale = result[i]['line_total']
                result_dict.update({ven:sale})
            result_dict = dict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True))
           
            vendors = []
            values = []
            for key, value in result_dict.items():
                vendors.append(key)
                values.append(value)

            


            text = channelName+" "+category+ " Sales Data"

            downloadData = finalResult
            fileName = str(channelName)+" "+str(category)+" "+str(from_date)+"-"+str(to_date)
            return render(request,'sales/sales.html',{'vendor':vendors,'values':values,'salesData':finalResult[0:100],'text':text,'show':True})


        



    return render(request,'sales/sales.html',{'data':"no",'show':False})

@login_required(login_url='login_view')
def analytics(request):
    if request.method == 'POST':
        
        from_date = request.POST.get('startdate')
        time = request.POST.get('time')
        channelName = request.POST.get('channelName')
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        category = request.POST.get('cat')
    
        dateArr = []
        dateArr.append(from_date)
        for i in range(0,4):
            b = from_date - timedelta(days=int(time))
            dateArr.append(b.date())
            from_date = b

    
        q1 = TotalSalesData.objects.filter(date__range=(str(dateArr[1]),str(dateArr[0].date())))
        q2 = TotalSalesData.objects.filter(date__range=(str(dateArr[2]),str(dateArr[1])))
        q3 = TotalSalesData.objects.filter(date__range=(str(dateArr[3]),str(dateArr[2])))
    

        d1 = {}
        d2 = {}
        d3 = {}
        for i in range(0,len(q1)):
            if q1[i].sales_channel in d1:
                d1[q1[i].sales_channel] += q1[i].quantity
            else:
                d1[q1[i].sales_channel] = 0
        for i in range(0,len(q2)):
            if q2[i].sales_channel in d2:
                d2[q2[i].sales_channel] += q2[i].quantity
            else:
                d2[q2[i].sales_channel] = 0
        for i in range(0,len(q3)):
            if q3[i].sales_channel in d3:
                d3[q3[i].sales_channel] += q3[i].quantity
            else:
                d3[q3[i].sales_channel] = 0
    

        fd1 = {}
        fd2 = {}
        fd3 = {}
        fd4 = {}
        id1 = sorted(d1.items(), key=lambda item: item[1],reverse = True)
        id2 = sorted(d2.items(), key=lambda item: item[1],reverse = True)
        id3 = sorted(d3.items(), key=lambda item: item[1],reverse = True)

        for i in range(0,len(id1)):
            fd1[id1[i][0]] = id1[i][1]
            
        for i in range(0,len(id2)):
            fd2[id2[i][0]] = id2[i][1]
        
        for i in range(0,len(id3)):
            fd3[id3[i][0]] = id3[i][1]
            
        

        sd1 = list(fd1.keys())
        vd1 = list(fd1.values())

        sd2 = list(fd2.keys())
        vd2 = list(fd2.values())

        sd3 = list(fd3.keys())
        vd3 = list(fd3.values())

        
    
        df1 = {'channel':sd1,'quantity1':vd1}
        df2 = {'channel':sd2,'quantity2':vd2}
        df3 = {'channel':sd3,'quantity3':vd3}
        df1 = pd.DataFrame(df1)
        df2 = pd.DataFrame(df2)
        df3 = pd.DataFrame(df3)  

        
        df = reduce(lambda x,y: pd.merge(x,y, on='channel', how='outer'), [df1, df2, df3])
        df = df.replace(np.nan,0)


        salesChannel = list(df['channel'])
        vd1 = list(df['quantity1'])
        vd2 = list(df['quantity2'])
        vd3 = list(df['quantity3'])


       
        totalQuantity1 = int(sum(vd1)) 
        totalQuantity2 = int(sum(vd2))
        totalQuantity3 = int(sum(vd3))


        vd1 = list(map(int, vd1))
        vd2 = list(map(int, vd2))
        vd3 = list(map(int, vd3))
        

        a1 = dateArr[0].date()
        b1 = str(a1).split('-')
        f1 = b1[-1]+"/"+b1[-2]+"/"+b1[0]

        a2 = dateArr[1]
        b2 = str(a2).split('-')
        f2 = b2[-1]+"/"+b2[-2]+"/"+b2[0] 

        a3 = dateArr[2]
        b3 = str(a3).split('-')
        f3 = b3[-1]+"/"+b3[-2]+"/"+b3[0]

        a4 = dateArr[3]
        b4 = str(a4).split('-')
        f4 = b4[-1]+"/"+b4[-2]+"/"+b4[0]

        if channelName == 'None' and category == 'None':
            yes = True
            text = "Quantity Analysis"
            heading = "Channel"
            return render(request,'sales/quantity.html',{
                'show':True,
                'result':yes,'text':text,'heading':heading,
                'total1':totalQuantity1,'total2':totalQuantity2,'total3':totalQuantity3,
                'channel' : salesChannel,'q1':vd1,'q2':vd2,'q3':vd3,
                'date1':f1,'date2':f2,'date3':f3,'date4':f4
            })

        elif channelName == 'vendor' and category == 'None':
            vd1 = {}
            vd2 = {}
            vd3 = {}

            for i in range(0,len(q1)):
                if q1[i].vendor in vd1:
                    vd1[q1[i].vendor] += q1[i].quantity
                else:
                    vd1[q1[i].vendor] = 0

            for i in range(0,len(q2)):
                if q2[i].vendor in vd2:
                    vd2[q2[i].vendor] += q2[i].quantity
                else:
                    vd2[q2[i].vendor] = 0
            for i in range(0,len(q3)):
                if q3[i].vendor in vd3:
                    vd3[q3[i].vendor] += q3[i].quantity
                else:
                    vd3[q3[i].vendor] = 0
            fvd1 = {}
            fvd2 = {}
            fvd3 = {}
            ivd1 = sorted(vd1.items(), key=lambda item: item[1],reverse = True)
            ivd2 = sorted(vd2.items(), key=lambda item: item[1],reverse = True)
            ivd3 = sorted(vd3.items(), key=lambda item: item[1],reverse = True)

            for i in range(0,len(ivd1)):
                fvd1[ivd1[i][0]] = ivd1[i][1]
                
            for i in range(0,len(ivd2)):
                fvd2[ivd2[i][0]] = ivd2[i][1]
            
            for i in range(0,len(ivd3)):
                fvd3[ivd3[i][0]] = ivd3[i][1]
            

            sd1 = list(fvd1.keys())
            vd1 = list(fvd1.values())

            sd2 = list(fvd2.keys())
            vd2 = list(fvd2.values())

            sd3 = list(fvd3.keys())
            vd3 = list(fvd3.values())

            df1 = {'vendor':sd1,'quantity1':vd1}
            df2 = {'vendor':sd2,'quantity2':vd2}
            df3 = {'vendor':sd3,'quantity3':vd3}
            df1 = pd.DataFrame(df1)
            df2 = pd.DataFrame(df2)
            df3 = pd.DataFrame(df3)  

            
            df = reduce(lambda x,y: pd.merge(x,y, on='vendor', how='outer'), [df1, df2, df3])
            df = df.replace(np.nan,0)

            vendorList = list(df['vendor'])
            for i in range(0,len(vendorList)):
                if len(vendorList[i]) > 15:
                    vendorList[i] = vendorList[i][0:15]+"...."

            salesChannel = vendorList
            vd1 = list(df['quantity1'])
            vd2 = list(df['quantity2'])
            vd3 = list(df['quantity3'])


        
            totalQuantity1 = int(sum(vd1)) 
            totalQuantity2 = int(sum(vd2))
            totalQuantity3 = int(sum(vd3))


            vd1 = list(map(int, vd1))
            vd2 = list(map(int, vd2))
            vd3 = list(map(int, vd3))
            

            a1 = dateArr[0].date()
            b1 = str(a1).split('-')
            f1 = b1[-1]+"/"+b1[-2]+"/"+b1[0]

            a2 = dateArr[1]
            b2 = str(a2).split('-')
            f2 = b2[-1]+"/"+b2[-2]+"/"+b2[0] 

            a3 = dateArr[2]
            b3 = str(a3).split('-')
            f3 = b3[-1]+"/"+b3[-2]+"/"+b3[0]

            a4 = dateArr[3]
            b4 = str(a4).split('-')
            f4 = b4[-1]+"/"+b4[-2]+"/"+b4[0]

            
            yes = True
            text = "Vendor Analysis"
            heading = "Vendor"
            return render(request,'sales/quantity.html',{
                'show':True,
                'result':yes,'text':text,'heading':heading,
                'total1':totalQuantity1,'total2':totalQuantity2,'total3':totalQuantity3,
                'channel' : salesChannel,'q1':vd1,'q2':vd2,'q3':vd3,
                'date1':f1,'date2':f2,'date3':f3,'date4':f4
            })

        elif channelName == 'vendor' and category != 'None':
            q1 = q1.filter(vendor_type__contains= category)
            q2 = q2.filter(vendor_type__contains= category)
            q3 = q3.filter(vendor_type__contains= category)

            vd1 = {}
            vd2 = {}
            vd3 = {}

            for i in range(0,len(q1)):
                if q1[i].vendor in vd1:
                    vd1[q1[i].vendor] += q1[i].quantity
                else:
                    vd1[q1[i].vendor] = 0

            for i in range(0,len(q2)):
                if q2[i].vendor in vd2:
                    vd2[q2[i].vendor] += q2[i].quantity
                else:
                    vd2[q2[i].vendor] = 0
            for i in range(0,len(q3)):
                if q3[i].vendor in vd3:
                    vd3[q3[i].vendor] += q3[i].quantity
                else:
                    vd3[q3[i].vendor] = 0
            fvd1 = {}
            fvd2 = {}
            fvd3 = {}
            ivd1 = sorted(vd1.items(), key=lambda item: item[1],reverse = True)
            ivd2 = sorted(vd2.items(), key=lambda item: item[1],reverse = True)
            ivd3 = sorted(vd3.items(), key=lambda item: item[1],reverse = True)

            for i in range(0,len(ivd1)):
                fvd1[ivd1[i][0]] = ivd1[i][1]
                
            for i in range(0,len(ivd2)):
                fvd2[ivd2[i][0]] = ivd2[i][1]
            
            for i in range(0,len(ivd3)):
                fvd3[ivd3[i][0]] = ivd3[i][1]
            

            sd1 = list(fvd1.keys())
            vd1 = list(fvd1.values())

            sd2 = list(fvd2.keys())
            vd2 = list(fvd2.values())

            sd3 = list(fvd3.keys())
            vd3 = list(fvd3.values())

            df1 = {'vendor':sd1,'quantity1':vd1}
            df2 = {'vendor':sd2,'quantity2':vd2}
            df3 = {'vendor':sd3,'quantity3':vd3}
            df1 = pd.DataFrame(df1)
            df2 = pd.DataFrame(df2)
            df3 = pd.DataFrame(df3)  

            
            df = reduce(lambda x,y: pd.merge(x,y, on='vendor', how='outer'), [df1, df2, df3])
            df = df.replace(np.nan,0)

            vendorList = list(df['vendor'])
            for i in range(0,len(vendorList)):
                if len(vendorList[i]) > 15:
                    vendorList[i] = vendorList[i][0:15]+"...."

            salesChannel = vendorList
            vd1 = list(df['quantity1'])
            vd2 = list(df['quantity2'])
            vd3 = list(df['quantity3'])


        
            totalQuantity1 = int(sum(vd1)) 
            totalQuantity2 = int(sum(vd2))
            totalQuantity3 = int(sum(vd3))


            vd1 = list(map(int, vd1))
            vd2 = list(map(int, vd2))
            vd3 = list(map(int, vd3))
            

            a1 = dateArr[0].date()
            b1 = str(a1).split('-')
            f1 = b1[-1]+"/"+b1[-2]+"/"+b1[0]

            a2 = dateArr[1]
            b2 = str(a2).split('-')
            f2 = b2[-1]+"/"+b2[-2]+"/"+b2[0] 

            a3 = dateArr[2]
            b3 = str(a3).split('-')
            f3 = b3[-1]+"/"+b3[-2]+"/"+b3[0]

            a4 = dateArr[3]
            b4 = str(a4).split('-')
            f4 = b4[-1]+"/"+b4[-2]+"/"+b4[0]

            
            yes = True
            text = "Vendor Analysis" +" "+category
            heading = "Vendor"
            return render(request,'sales/quantity.html',{
                'show':True,
                'result':yes,'text':text,'heading':heading,
                'total1':totalQuantity1,'total2':totalQuantity2,'total3':totalQuantity3,
                'channel' : salesChannel,'q1':vd1,'q2':vd2,'q3':vd3,
                'date1':f1,'date2':f2,'date3':f3,'date4':f4
            })

        elif channelName != 'None' and category == 'None':
            finalResult1 = q1.filter(sales_channel__contains= channelName)
            finalResult2 = q2.filter(sales_channel__contains= channelName)
            finalResult3 = q3.filter(sales_channel__contains= channelName)
            

            v1 = {}
            v2 = {}
            v3 = {}



            for i in range(0,len(finalResult1)):
                if finalResult1[i].vendor in v1:
                    v1[finalResult1[i].vendor] += finalResult1[i].line_total
                else:
                    v1[finalResult1[i].vendor] = 0

            for i in range(0,len(finalResult2)):
                if finalResult2[i].vendor in v2:
                    v2[finalResult2[i].vendor] += finalResult2[i].line_total
                else:
                    v2[finalResult2[i].vendor] = 0

            for i in range(0,len(finalResult3)):
                if finalResult3[i].vendor in v3:
                    v3[finalResult3[i].vendor] += finalResult3[i].line_total
                else:
                    v3[finalResult3[i].vendor] = 0


    
            V1 = list(v1.keys())
            L1 = list(v1.values())

            V2 = list(v2.keys())
            L2 = list(v2.values())

            V3 = list(v3.keys())
            L3 = list(v3.values())

            df1 = {'vendor':V1,'lineTotal1':L1}
            df2 = {'vendor':V2,'lineTotal2':L2}
            df3 = {'vendor':V3,'lineTotal3':L3}


            df1 = pd.DataFrame(df1)
            df2 = pd.DataFrame(df2)
            df3 = pd.DataFrame(df3)  

            
            df = reduce(lambda x,y: pd.merge(x,y, on='vendor', how='outer'), [df1, df2, df3])
            df = df.replace(np.nan,0)


            vendorList = list(df['vendor'])
            for i in range(0,len(vendorList)):
                if len(vendorList[i]) > 15:
                    vendorList[i] = vendorList[i][0:15]+"...."

            lt1 = list(df['lineTotal1'])
            lt2 = list(df['lineTotal2'])
            lt3 = list(df['lineTotal3'])

            lt1 = list(map(int, lt1))
            lt2 = list(map(int, lt2))
            lt3 = list(map(int, lt3))

            totalSales1 = sum(lt1)
            totalSales2 = sum(lt2)
            totalSales3 = sum(lt3)


            sv1 = {}
            sv2 = {}
            sv3 = {}

            for i in range(0,len(finalResult1)):
                if finalResult1[i].vendor in sv1:
                    sv1[finalResult1[i].vendor] += finalResult1[i].quantity
                else:
                    sv1[finalResult1[i].vendor] = 0

            for i in range(0,len(finalResult2)):
                if finalResult2[i].vendor in sv2:
                    sv2[finalResult2[i].vendor] += finalResult2[i].quantity
                else:
                    sv2[finalResult2[i].vendor] = 0

            for i in range(0,len(finalResult3)):
                if finalResult3[i].vendor in sv3:
                    sv3[finalResult3[i].vendor] += finalResult3[i].quantity
                else:
                    sv3[finalResult3[i].vendor] = 0

            

            SV1 = list(sv1.keys())
            SQ1 = list(sv1.values())

            SV2 = list(sv2.keys())
            SQ2 = list(sv2.values())

            SV3 = list(sv3.keys())
            SQ3 = list(sv3.values())


            vdf1 = {'vendor':SV1,'Quantity1':SQ1}
            vdf2 = {'vendor':SV2,'Quantity2':SQ2}
            vdf3 = {'vendor':SV3,'Quantity3':SQ3}

            vdf1 = pd.DataFrame(vdf1)
            vdf2 = pd.DataFrame(vdf2)
            vdf3 = pd.DataFrame(vdf3)

            vdf = reduce(lambda x,y: pd.merge(x,y, on='vendor', how='outer'), [vdf1, vdf2, vdf3])
            vdf = vdf.replace(np.nan,0)
            
            # print(vdf['Quantity1'])

            qt1 = list(vdf['Quantity1'])
            qt2 = list(vdf['Quantity2'])
            qt3 = list(vdf['Quantity3'])

            qt1 = list(map(int, qt1))
            qt2 = list(map(int, qt2))
            qt3 = list(map(int, qt3))

            # print(qt1)


            totalQuantity1 = sum(qt1)
            totalQuantity2 = sum(qt2)
            totalQuantity3 = sum(qt3)

            zip1 = zip(lt1,qt1)
            zip2 = zip(lt2,qt2)
            zip3 = zip(lt3,qt3)

            text = "Vendor Analysis"
            heading = "Vendor"

            a1 = dateArr[0].date()
            b1 = str(a1).split('-')
            f1 = b1[-1]+"/"+b1[-2]+"/"+b1[0]

            a2 = dateArr[1]
            b2 = str(a2).split('-')
            f2 = b2[-1]+"/"+b2[-2]+"/"+b2[0] 

            a3 = dateArr[2]
            b3 = str(a3).split('-')
            f3 = b3[-1]+"/"+b3[-2]+"/"+b3[0]

            a4 = dateArr[3]
            b4 = str(a4).split('-')
            f4 = b4[-1]+"/"+b4[-2]+"/"+b4[0]             

            return render(request,'sales/quantity.html',{
                'show':True,
                'text':text,'channel':channelName,'heading':heading,'dollar':'$',
                'totalSale1':totalSales1,'totalSale2':totalSales2,'totalSale3':totalSales3,
                'totalQuantity1':totalQuantity1,'totalQuantity2':totalQuantity2,'totalQuantity3':totalQuantity3,
                'vendor' : vendorList,'lineTotal1':zip1,'lineTotal2':zip2,'lineTotal3':zip3,
                'gv1':lt1,'gv2':lt2,'gv3':lt3,
                'date1':f1,'date2':f2,'date3':f3,'date4':f4
            })

        elif channelName == 'None' and category != 'None':
            q1 = q1.filter(vendor_type__contains= category)
            q2 = q2.filter(vendor_type__contains= category)
            q3 = q3.filter(vendor_type__contains= category)
            

            d1 = {}
            d2 = {}
            d3 = {}
            for i in range(0,len(q1)):
                if q1[i].sales_channel in d1:
                    d1[q1[i].sales_channel] += q1[i].quantity
                else:
                    d1[q1[i].sales_channel] = 0
            for i in range(0,len(q2)):
                if q2[i].sales_channel in d2:
                    d2[q2[i].sales_channel] += q2[i].quantity
                else:
                    d2[q2[i].sales_channel] = 0
            for i in range(0,len(q3)):
                if q3[i].sales_channel in d3:
                    d3[q3[i].sales_channel] += q3[i].quantity
                else:
                    d3[q3[i].sales_channel] = 0
        

            # print(d1)
            # print(d2)
            # print(d3)
            # print(d4)

            fd1 = {}
            fd2 = {}
            fd3 = {}
            fd4 = {}
            id1 = sorted(d1.items(), key=lambda item: item[1],reverse = True)
            id2 = sorted(d2.items(), key=lambda item: item[1],reverse = True)
            id3 = sorted(d3.items(), key=lambda item: item[1],reverse = True)

            for i in range(0,len(id1)):
                fd1[id1[i][0]] = id1[i][1]
                
            for i in range(0,len(id2)):
                fd2[id2[i][0]] = id2[i][1]
            
            for i in range(0,len(id3)):
                fd3[id3[i][0]] = id3[i][1]
                
            

            sd1 = list(fd1.keys())
            vd1 = list(fd1.values())

            sd2 = list(fd2.keys())
            vd2 = list(fd2.values())

            sd3 = list(fd3.keys())
            vd3 = list(fd3.values())

            
            # print(sd1)
            # print(vd1)

            # print(sd2)
            # print(vd2)

            # print(sd3)
            # print(vd3)

            # print(sd4)
            # print(vd4)


            df1 = {'channel':sd1,'quantity1':vd1}
            df2 = {'channel':sd2,'quantity2':vd2}
            df3 = {'channel':sd3,'quantity3':vd3}
            df1 = pd.DataFrame(df1)
            df2 = pd.DataFrame(df2)
            df3 = pd.DataFrame(df3)  

            
            df = reduce(lambda x,y: pd.merge(x,y, on='channel', how='outer'), [df1, df2, df3])
            df = df.replace(np.nan,0)

            salesChannel = list(df['channel'])
            vd1 = list(df['quantity1'])
            vd2 = list(df['quantity2'])
            vd3 = list(df['quantity3'])

            totalQuantity1 = int(sum(vd1)) 
            totalQuantity2 = int(sum(vd2))
            totalQuantity3 = int(sum(vd3))                    

            # sd1 = salesChannel
            # sd2 = salesChannel
            # sd3 = salesChannel
            # print(sd1,vd1)
            # print(sd2,vd2)
            # print(sd3,vd3)
            vd1 = list(map(int, vd1))
            vd2 = list(map(int, vd2))
            vd3 = list(map(int, vd3))
            
            # print(channelName,category)

            a1 = dateArr[0].date()
            b1 = str(a1).split('-')
            f1 = b1[-1]+"/"+b1[-2]+"/"+b1[0]

            a2 = dateArr[1]
            b2 = str(a2).split('-')
            f2 = b2[-1]+"/"+b2[-2]+"/"+b2[0] 

            a3 = dateArr[2]
            b3 = str(a3).split('-')
            f3 = b3[-1]+"/"+b3[-2]+"/"+b3[0]

            a4 = dateArr[3]
            b4 = str(a4).split('-')
            f4 = b4[-1]+"/"+b4[-2]+"/"+b4[0]
                
            yes = True
            text = "Quantity Analysis of "+category
            heading = "Channel"
            return render(request,'sales/quantity.html',{   
                'show':True,
                'result':yes,'text':text,'heading':heading,
                'total1':totalQuantity1,'total2':totalQuantity2,'total3':totalQuantity3,
                'channel' : salesChannel,'q1':vd1,'q2':vd2,'q3':vd3,
                'date1':f1,'date2':f2,'date3':f3,'date4':f4
            })

        elif channelName != 'None' and category != 'None':
            finalResult1 = q1.filter(sales_channel__contains= channelName)
            finalResult2 = q2.filter(sales_channel__contains= channelName)
            finalResult3 = q3.filter(sales_channel__contains= channelName)

            finalResult1 = finalResult1.filter(vendor_type__contains= category)
            finalResult2 = finalResult2.filter(vendor_type__contains= category)
            finalResult3 = finalResult3.filter(vendor_type__contains= category)            


            v1 = {}
            v2 = {}
            v3 = {}



            for i in range(0,len(finalResult1)):
                if finalResult1[i].vendor in v1:
                    v1[finalResult1[i].vendor] += finalResult1[i].line_total
                else:
                    v1[finalResult1[i].vendor] = 0

            for i in range(0,len(finalResult2)):
                if finalResult2[i].vendor in v2:
                    v2[finalResult2[i].vendor] += finalResult2[i].line_total
                else:
                    v2[finalResult2[i].vendor] = 0

            for i in range(0,len(finalResult3)):
                if finalResult3[i].vendor in v3:
                    v3[finalResult3[i].vendor] += finalResult3[i].line_total
                else:
                    v3[finalResult3[i].vendor] = 0


    
            V1 = list(v1.keys())
            L1 = list(v1.values())

            V2 = list(v2.keys())
            L2 = list(v2.values())

            V3 = list(v3.keys())
            L3 = list(v3.values())

            df1 = {'vendor':V1,'lineTotal1':L1}
            df2 = {'vendor':V2,'lineTotal2':L2}
            df3 = {'vendor':V3,'lineTotal3':L3}


            df1 = pd.DataFrame(df1)
            df2 = pd.DataFrame(df2)
            df3 = pd.DataFrame(df3)  

            
            df = reduce(lambda x,y: pd.merge(x,y, on='vendor', how='outer'), [df1, df2, df3])
            df = df.replace(np.nan,0)


            vendorList = list(df['vendor'])
            for i in range(0,len(vendorList)):
                if len(vendorList[i]) > 15:
                    vendorList[i] = vendorList[i][0:15]+"...."

            lt1 = list(df['lineTotal1'])
            lt2 = list(df['lineTotal2'])
            lt3 = list(df['lineTotal3'])

            lt1 = list(map(int, lt1))
            lt2 = list(map(int, lt2))
            lt3 = list(map(int, lt3))

            totalSales1 = sum(lt1)
            totalSales2 = sum(lt2)
            totalSales3 = sum(lt3)

            sv1 = {}
            sv2 = {}
            sv3 = {}

            for i in range(0,len(finalResult1)):
                if finalResult1[i].vendor in sv1:
                    sv1[finalResult1[i].vendor] += finalResult1[i].quantity
                else:
                    sv1[finalResult1[i].vendor] = 0

            for i in range(0,len(finalResult2)):
                if finalResult2[i].vendor in sv2:
                    sv2[finalResult2[i].vendor] += finalResult2[i].quantity
                else:
                    sv2[finalResult2[i].vendor] = 0

            for i in range(0,len(finalResult3)):
                if finalResult3[i].vendor in sv3:
                    sv3[finalResult3[i].vendor] += finalResult3[i].quantity
                else:
                    sv3[finalResult3[i].vendor] = 0

            

            SV1 = list(sv1.keys())
            SQ1 = list(sv1.values())

            SV2 = list(sv2.keys())
            SQ2 = list(sv2.values())

            SV3 = list(sv3.keys())
            SQ3 = list(sv3.values())


            vdf1 = {'vendor':SV1,'Quantity1':SQ1}
            vdf2 = {'vendor':SV2,'Quantity2':SQ2}
            vdf3 = {'vendor':SV3,'Quantity3':SQ3}

            vdf1 = pd.DataFrame(vdf1)
            vdf2 = pd.DataFrame(vdf2)
            vdf3 = pd.DataFrame(vdf3)

            vdf = reduce(lambda x,y: pd.merge(x,y, on='vendor', how='outer'), [vdf1, vdf2, vdf3])
            vdf = vdf.replace(np.nan,0)
            
            # print(vdf['Quantity1'])

            qt1 = list(vdf['Quantity1'])
            qt2 = list(vdf['Quantity2'])
            qt3 = list(vdf['Quantity3'])

            qt1 = list(map(int, qt1))
            qt2 = list(map(int, qt2))
            qt3 = list(map(int, qt3))

            # print(qt1)
            totalQuantity1 = sum(qt1)
            totalQuantity2 = sum(qt2)
            totalQuantity3 = sum(qt3)

            zip1 = zip(lt1,qt1)
            zip2 = zip(lt2,qt2)
            zip3 = zip(lt3,qt3)

            text = "Vendor Analysis of "+category
            heading = "Vendor"

            a1 = dateArr[0].date()
            b1 = str(a1).split('-')
            f1 = b1[-1]+"/"+b1[-2]+"/"+b1[0]

            a2 = dateArr[1]
            b2 = str(a2).split('-')
            f2 = b2[-1]+"/"+b2[-2]+"/"+b2[0] 

            a3 = dateArr[2]
            b3 = str(a3).split('-')
            f3 = b3[-1]+"/"+b3[-2]+"/"+b3[0]

            a4 = dateArr[3]
            b4 = str(a4).split('-')
            f4 = b4[-1]+"/"+b4[-2]+"/"+b4[0]             

            return render(request,'sales/quantity.html',{
                'show':True,
                'text':text,'channel':channelName,'heading':heading,'dollar':'$',
                'totalSale1':totalSales1,'totalSale2':totalSales2,'totalSale3':totalSales3,
                'totalQuantity1':totalQuantity1,'totalQuantity2':totalQuantity2,'totalQuantity3':totalQuantity3,
                'vendor' : vendorList,'lineTotal1':zip1,'lineTotal2':zip2,'lineTotal3':zip3,
                'gv1':lt1,'gv2':lt2,'gv3':lt3,
                'date1':f1,'date2':f2,'date3':f3,'date4':f4
            })


    return render(request,'sales/quantity.html',{'show':False})

@login_required(login_url='login_view')
def weekly(request):
    if request.method == 'POST':
        
        from_date = request.POST.get('startdate')
        channelName = request.POST.get('channelName')
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        category = request.POST.get('cat')
        
        a = from_date.date()
        dateArr = []
        for i in range(0,5):
            b = from_date - timedelta(days=7)
            dateArr.append(b.date())
            from_date = b
    
        q1 = TotalSalesData.objects.filter(date__range=(str(dateArr[1]),str(dateArr[0])))
        q2 = TotalSalesData.objects.filter(date__range=(str(dateArr[2]),str(dateArr[1])))
        q3 = TotalSalesData.objects.filter(date__range=(str(dateArr[3]),str(dateArr[2])))
        q4 = TotalSalesData.objects.filter(date__range=(str(dateArr[4]),str(dateArr[3])))

        if channelName == 'None' and category == 'Total':
            lineTotalWeek1 = 0
            lineTotalWeek2 = 0
            lineTotalWeek3 = 0
            lineTotalWeek4 = 0


            for i in range(0,len(q1)):
                lineTotalWeek1 += q1[i].line_total

            for i in range(0,len(q2)):
                lineTotalWeek2 += q2[i].line_total
                # q2[i].line_total += lineTotalWeek2

            for i in range(0,len(q3)):
                lineTotalWeek3 += q3[i].line_total
                # q3[i].line_total += lineTotalWeek3
            
            for i in range(0,len(q4)):
                lineTotalWeek4 += q4[i].line_total
                # q4[i].line_total += lineTotalWeek4
        
            lineTotalWeek1 =  round(lineTotalWeek1,2)
            lineTotalWeek2 =  round(lineTotalWeek2,2)
            lineTotalWeek3 =  round(lineTotalWeek3,2)
            lineTotalWeek4 =  round(lineTotalWeek4,2)

            lineTotalArr = []
            lineTotalArr.append(lineTotalWeek1)
            lineTotalArr.append(lineTotalWeek2)
            lineTotalArr.append(lineTotalWeek3)
            lineTotalArr.append(lineTotalWeek4)

            # for i in range(0,len(dateArr)):
            #     print(dateArr[i])

            keys = ['Week1','Week2','Week3','Week4']
            yes = True
            text = category + " Weekly Sales Analysis"


            return render(request,'sales/weekly.html',{
                'show':True,
                'text':text,'check':yes,
                'date1':a,'date2':dateArr[0],'date3':dateArr[1],'date4':dateArr[2],'date5':dateArr[3],
                'week1':lineTotalWeek1,'week2':lineTotalWeek2,'week3':lineTotalWeek3,'week4':lineTotalWeek4,
                'label':keys,'value':lineTotalArr
            })


        elif channelName != 'None' and category == 'Total':
            finalResult1 = q1.filter(sales_channel__contains= channelName)
            finalResult2 = q2.filter(sales_channel__contains= channelName)
            finalResult3 = q3.filter(sales_channel__contains= channelName)
            finalResult4 = q4.filter(sales_channel__contains= channelName)

            
            lineTotalChannel1 = 0
            lineTotalChannel2 = 0
            lineTotalChannel3 = 0
            lineTotalChannel4 = 0


            for i in range(0,len(finalResult1)):
                lineTotalChannel1 += finalResult1[i].line_total

            for i in range(0,len(finalResult2)):
                lineTotalChannel2 += finalResult2[i].line_total
                # q2[i].line_total += lineTotalWeek2

            for i in range(0,len(finalResult3)):
                lineTotalChannel3 += finalResult3[i].line_total
                # q3[i].line_total += lineTotalWeek3
            
            for i in range(0,len(finalResult4)):
                lineTotalChannel4 += finalResult4[i].line_total
                # q4[i].line_total += lineTotalWeek4
        
            lineTotalChannel1 =  round(lineTotalChannel1,2)
            lineTotalChannel2 =  round(lineTotalChannel2,2)
            lineTotalChannel3 =  round(lineTotalChannel3,2)
            lineTotalChannel4 =  round(lineTotalChannel4,2)

            lineTotalArr = []
            lineTotalArr.append(lineTotalChannel1)
            lineTotalArr.append(lineTotalChannel2)
            lineTotalArr.append(lineTotalChannel3)
            lineTotalArr.append(lineTotalChannel4)

            # for i in range(0,len(dateArr)):
            #     print(dateArr[i])

            keys = ['Week1','Week2','Week3','Week4']
            text = category + " Weekly Sales Analysis"
            return render(request,'sales/weekly.html',{
                'show':True,
                'text':text,'channel':channelName,
                'date1':a,'date2':dateArr[0],'date3':dateArr[1],'date4':dateArr[2],'date5':dateArr[3],
                'week1':lineTotalChannel1,'week2':lineTotalChannel2,'week3':lineTotalChannel3,'week4':lineTotalChannel4,
                'label':keys,'value':lineTotalArr
            })

        elif channelName == 'None' and category != 'Total':
            finalResult1 = q1.filter(vendor_type__contains= category)
            finalResult2 = q2.filter(vendor_type__contains= category)
            finalResult3 = q3.filter(vendor_type__contains= category)
            finalResult4 = q4.filter(vendor_type__contains= category)

            
            lineTotalChannel1 = 0
            lineTotalChannel2 = 0
            lineTotalChannel3 = 0
            lineTotalChannel4 = 0


            for i in range(0,len(finalResult1)):
                lineTotalChannel1 += finalResult1[i].line_total

            for i in range(0,len(finalResult2)):
                lineTotalChannel2 += finalResult2[i].line_total
                # q2[i].line_total += lineTotalWeek2

            for i in range(0,len(finalResult3)):
                lineTotalChannel3 += finalResult3[i].line_total
                # q3[i].line_total += lineTotalWeek3
            
            for i in range(0,len(finalResult4)):
                lineTotalChannel4 += finalResult4[i].line_total
                # q4[i].line_total += lineTotalWeek4
        
            lineTotalChannel1 =  round(lineTotalChannel1,2)
            lineTotalChannel2 =  round(lineTotalChannel2,2)
            lineTotalChannel3 =  round(lineTotalChannel3,2)
            lineTotalChannel4 =  round(lineTotalChannel4,2)

            lineTotalArr = []
            lineTotalArr.append(lineTotalChannel1)
            lineTotalArr.append(lineTotalChannel2)
            lineTotalArr.append(lineTotalChannel3)
            lineTotalArr.append(lineTotalChannel4)

            # for i in range(0,len(dateArr)):
            #     print(dateArr[i])

            keys = ['Week1','Week2','Week3','Week4']
            text = category + " Weekly Sales Analysis"
            return render(request,'sales/weekly.html',{
                'show':True,
                'text':text,'channel':channelName,
                'date1':a,'date2':dateArr[0],'date3':dateArr[1],'date4':dateArr[2],'date5':dateArr[3],
                'week1':lineTotalChannel1,'week2':lineTotalChannel2,'week3':lineTotalChannel3,'week4':lineTotalChannel4,
                'label':keys,'value':lineTotalArr
            })
            
        elif channelName != 'None' and category != 'Total':

            finalResult1 = q1.filter(sales_channel__contains= channelName)
            finalResult2 = q2.filter(sales_channel__contains= channelName)
            finalResult3 = q3.filter(sales_channel__contains= channelName)
            finalResult4 = q4.filter(sales_channel__contains= channelName)

            finalResult1 = finalResult1.filter(vendor_type__contains= category)
            finalResult2 = finalResult2.filter(vendor_type__contains= category)
            finalResult3 = finalResult3.filter(vendor_type__contains= category)
            finalResult4 = finalResult4.filter(vendor_type__contains= category)

            
            lineTotalChannel1 = 0
            lineTotalChannel2 = 0
            lineTotalChannel3 = 0
            lineTotalChannel4 = 0


            for i in range(0,len(finalResult1)):
                lineTotalChannel1 += finalResult1[i].line_total

            for i in range(0,len(finalResult2)):
                lineTotalChannel2 += finalResult2[i].line_total
                # q2[i].line_total += lineTotalWeek2

            for i in range(0,len(finalResult3)):
                lineTotalChannel3 += finalResult3[i].line_total
                # q3[i].line_total += lineTotalWeek3
            
            for i in range(0,len(finalResult4)):
                lineTotalChannel4 += finalResult4[i].line_total
                # q4[i].line_total += lineTotalWeek4
        
            lineTotalChannel1 =  round(lineTotalChannel1,2)
            lineTotalChannel2 =  round(lineTotalChannel2,2)
            lineTotalChannel3 =  round(lineTotalChannel3,2)
            lineTotalChannel4 =  round(lineTotalChannel4,2)

            lineTotalArr = []
            lineTotalArr.append(lineTotalChannel1)
            lineTotalArr.append(lineTotalChannel2)
            lineTotalArr.append(lineTotalChannel3)
            lineTotalArr.append(lineTotalChannel4)

            # for i in range(0,len(dateArr)):
            #     print(dateArr[i])

            keys = ['Week1','Week2','Week3','Week4']
            text = category + " Weekly Sales Analysis"
            return render(request,'sales/weekly.html',{
                'show':True,
                'text':text,'channel':channelName,
                'date1':a,'date2':dateArr[0],'date3':dateArr[1],'date4':dateArr[2],'date5':dateArr[3],
                'week1':lineTotalChannel1,'week2':lineTotalChannel2,'week3':lineTotalChannel3,'week4':lineTotalChannel4,
                'label':keys,'value':lineTotalArr
            })
            
        
    return render(request,'sales/weekly.html',{'show':False})
@login_required(login_url='login_view')
def export(request):
    # print(downloadData)
    # print("yes")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename='+fileName+'.csv'
    writer = csv.writer(response)   
    writer.writerow(['Date','Channel Name','Sales Order ID','Ship to Name','SKU','Normal SKU','Vendor','Quantity','Line Total','Channel Order ID','vendor type'])
    for i in downloadData:
        writer.writerow([i.date,i.sales_channel,i.sales_order_id,i.ship_to_name,i.sku,i.normal_sku,i.vendor,i.quantity,i.line_total,i.channel_order_id,i.vendor_type])
    return response



#for net sale

downloadOpalData = ""
opalFileName = "Data"
@login_required(login_url='login_view')
def net(request):

    show = False
    if request.method == 'POST':
        from_date = request.POST.get('startdate')
        to_date = request.POST.get('todate')
        channelName = request.POST.get('channelName')
        category = request.POST.get('cat')

        searchresult = TotalOpalData.objects.filter(orderdate__range=(from_date,to_date))
        global downloadOpalData
        global opalFileName
        downloadOpalData = searchresult

        opalData = TotalOpalData.objects.filter(orderstatus__contains="Cancelled")
        cancelData = opalData.filter(orderdate__range=(from_date,to_date))

        if channelName == 'None' and category == 'Total':

            result = (searchresult.values('customername').annotate(quantity=Sum('quantity')).order_by())

            totalDic = {}
            for i in range(0,len(result)):
                channel = result[i]['customername']
                sale = result[i]['quantity']
                totalDic.update({channel:sale})
            
            tv = list(totalDic.keys())
            tq = list(totalDic.values())

            df1 = {'channel':tv,'quantity':tq}
            tdf = pd.DataFrame(df1)

            #for cancellation 
            cancelResult = (cancelData.values('customername').annotate(quantity=Sum('quantity')).order_by())
            cancelDic = {}
            for i in range(0,len(cancelResult)):
                channel = cancelResult[i]['customername']
                sale = cancelResult[i]['quantity']
                cancelDic.update({channel:sale})

            ctv = list(cancelDic.keys())
            ctq = list(cancelDic.values())

            df2 = {'channel':ctv,'cancelled':ctq}
            cdf = pd.DataFrame(df2)

            df = tdf.merge(cdf,on='channel',how='outer')
            df = df.replace(np.nan,0)
            df.sort_values(by=['quantity'], inplace=True,ascending=False)
            # print(df)

            ch = list(df['channel'])
            qu = list(df['quantity'])
            cqu = list(df['cancelled'])

            qu = list(map(int, qu))
            cqu = list(map(int, cqu))
            net = []
            
            cancelsalePer = []
            for i in range(0,len(qu)):
                net.append(qu[i]-cqu[i])
                try :
                    a = (cqu[i]/qu[i])*100
                    cancelsalePer.append(round(a,2))
                    
                except:
                    cancelsalePer.append(0)
            # print(cancelsalePer)

            salPer = []
            for i in range(0,len(cancelsalePer)):
                salPer.append(100 - cancelsalePer[i])
            # print(salPer)

            

            z = zip(qu,cqu,net)
            c = zip(salPer,cancelsalePer)
            opalFileName = "opal data"+from_date+" - "+to_date
            message = category+" "+"Net Sale from"+" "+from_date+" - "+to_date
            return render(request,'sales/netSale.html',{
                'zip':z,'channel':ch,'per':c,'message':"Vednor Name",
                'sym':"%",'heading':message,'data':searchresult[0:100],'show':True
                })

        elif channelName == 'vendor' and category == 'Total':
            result = (searchresult.values('vendor').annotate(quantity=Sum('quantity')).order_by())

            totalDic = {}
            for i in range(0,len(result)):
                channel = result[i]['vendor']
                sale = result[i]['quantity']
                totalDic.update({channel:sale})
            
            # print(totalDic)

            tv = list(totalDic.keys())
            tq = list(totalDic.values())

            df1 = {'vendor':tv,'quantity':tq}
            tdf = pd.DataFrame(df1)

            #for cancellation 
            cancelResult = (cancelData.values('vendor').annotate(quantity=Sum('quantity')).order_by())
            cancelDic = {}
            for i in range(0,len(cancelResult)):
                channel = cancelResult[i]['vendor']
                sale = cancelResult[i]['quantity']
                cancelDic.update({channel:sale})

            # print(cancelDic)

            ctv = list(cancelDic.keys())
            ctq = list(cancelDic.values())

            df2 = {'vendor':ctv,'cancelled':ctq}
            cdf = pd.DataFrame(df2)



            df = tdf.merge(cdf,on='vendor',how='outer')
            df = df.replace(np.nan,0)
            df.sort_values(by=['quantity'], inplace=True,ascending=False)
            # print(df)

            ch = list(df['vendor'])
            qu = list(df['quantity'])
            cqu = list(df['cancelled'])

            for i in range(0,len(ch)):
                try:
                    ch[i] = ch[i][0:20]+" ...."
                    # print(ch[i])
                except:
                    ch[i] = 'Name not Avaliable'

            qu = list(map(int, qu))
            cqu = list(map(int, cqu))
            net = []
            
            cancelsalePer = []
            for i in range(0,len(qu)):
                net.append(qu[i]-cqu[i])
                try :
                    a = (cqu[i]/qu[i])*100
                    cancelsalePer.append(round(a,2))
                    
                except:
                    cancelsalePer.append(0)
            # print(cancelsalePer)

            salPer = []
            for i in range(0,len(cancelsalePer)):
                salPer.append(100 - cancelsalePer[i])
            # print(salPer)

            

            z = zip(qu,cqu,net)
            c = zip(salPer,cancelsalePer)
            opalFileName = "opal data"+from_date+" - "+to_date
            message = channelName+" "+category+" "+"Net Sale from"+" "+from_date+" - "+to_date
            return render(request,'sales/netSale.html',{
                'zip':z,'channel':ch,'per':c,'message':"Vednor Name",
                'sym':"%",'heading':message,'data':searchresult[0:100],'show':True
                })

        elif channelName == 'vendor' and category != 'Total':
            searchresult = searchresult.filter(vendortype__contains=category)

            result = (searchresult.values('vendor').annotate(quantity=Sum('quantity')).order_by())

            totalDic = {}
            for i in range(0,len(result)):
                channel = result[i]['vendor']
                sale = result[i]['quantity']
                totalDic.update({channel:sale})
            
            # print(totalDic)

            tv = list(totalDic.keys())
            tq = list(totalDic.values())

            df1 = {'vendor':tv,'quantity':tq}
            tdf = pd.DataFrame(df1)

            #for cancellation 
            cancelData = cancelData.filter(vendortype__contains=category)
            cancelResult = (cancelData.values('vendor').annotate(quantity=Sum('quantity')).order_by())
            cancelDic = {}
            for i in range(0,len(cancelResult)):
                channel = cancelResult[i]['vendor']
                sale = cancelResult[i]['quantity']
                cancelDic.update({channel:sale})

            # print(cancelDic)

            ctv = list(cancelDic.keys())
            ctq = list(cancelDic.values())

            df2 = {'vendor':ctv,'cancelled':ctq}
            cdf = pd.DataFrame(df2)



            df = tdf.merge(cdf,on='vendor',how='outer')
            df = df.replace(np.nan,0)
            df.sort_values(by=['quantity'], inplace=True,ascending=False)
            # print(df)

            ch = list(df['vendor'])
            qu = list(df['quantity'])
            cqu = list(df['cancelled'])

            for i in range(0,len(ch)):
                try:
                    ch[i] = ch[i][0:20]+" ...."
                    # print(ch[i])
                except:
                    ch[i] = 'Name not Avaliable'

            qu = list(map(int, qu))
            cqu = list(map(int, cqu))
            net = []
            
            cancelsalePer = []
            for i in range(0,len(qu)):
                net.append(qu[i]-cqu[i])
                try :
                    a = (cqu[i]/qu[i])*100
                    cancelsalePer.append(round(a,2))
                    
                except:
                    cancelsalePer.append(0)
            # print(cancelsalePer)

            salPer = []
            for i in range(0,len(cancelsalePer)):
                salPer.append(100 - cancelsalePer[i])
            # print(salPer)

            

            z = zip(qu,cqu,net)
            c = zip(salPer,cancelsalePer)
            opalFileName = "opal data"+from_date+" - "+to_date
            message = channelName+" "+category+" "+"Net Sale from"+" "+from_date+" - "+to_date
            return render(request,'sales/netSale.html',{
                'zip':z,'channel':ch,'per':c,'message':"Vednor Name",
                'sym':"%",'heading':message,'data':searchresult[0:100],'show':True
                })


        elif channelName == 'None' and category != 'Total':
            searchresult = searchresult.filter(vendortype__contains=category)
            # print(category)
            result = (searchresult.values('customername').annotate(quantity=Sum('quantity')).order_by())
            # print(result)
            totalDic = {}
            for i in range(0,len(result)):
                channel = result[i]['customername']
                sale = result[i]['quantity']
                totalDic.update({channel:sale})
            
            tv = list(totalDic.keys())
            tq = list(totalDic.values())

            df1 = {'channel':tv,'quantity':tq}
            tdf = pd.DataFrame(df1)

            #for cancellation 
            
            cancelData = cancelData.filter(vendortype__contains=category)
            cancelResult = (cancelData.values('customername').annotate(quantity=Sum('quantity')).order_by())
            cancelDic = {}
            for i in range(0,len(cancelResult)):
                channel = cancelResult[i]['customername']
                sale = cancelResult[i]['quantity']
                cancelDic.update({channel:sale})

            ctv = list(cancelDic.keys())
            ctq = list(cancelDic.values())

            df2 = {'channel':ctv,'cancelled':ctq}
            cdf = pd.DataFrame(df2)

            df = tdf.merge(cdf,on='channel',how='outer')
            df = df.replace(np.nan,0)
            df.sort_values(by=['quantity'], inplace=True,ascending=False)
            # print(df)

            ch = list(df['channel'])
            qu = list(df['quantity'])
            cqu = list(df['cancelled'])

            qu = list(map(int, qu))
            cqu = list(map(int, cqu))
            net = []
            
            cancelsalePer = []
            for i in range(0,len(qu)):
                net.append(qu[i]-cqu[i])
                try :
                    a = (cqu[i]/qu[i])*100
                    cancelsalePer.append(round(a,2))
                    
                except:
                    cancelsalePer.append(0)
            # print(cancelsalePer)

            salPer = []
            for i in range(0,len(cancelsalePer)):
                salPer.append(100 - cancelsalePer[i])
            # print(salPer)

            

            z = zip(qu,cqu,net)
            c = zip(salPer,cancelsalePer)
            opalFileName = "opal data"+from_date+" - "+to_date
            message = category+" "+"Net Sale from"+" "+from_date+" - "+to_date
            return render(request,'sales/netSale.html',{
                'zip':z,'channel':ch,'per':c,'message':"Vednor Name",
                'sym':"%",'heading':message,'data':searchresult[0:100],'show':True
                })

        elif channelName != 'None' and category == 'Total':

            searchresult = searchresult.filter(customername__contains=channelName)
            result = (searchresult.values('vendor').annotate(quantity=Sum('quantity')).order_by())

            totalDic = {}
            for i in range(0,len(result)):
                channel = result[i]['vendor']
                sale = result[i]['quantity']
                totalDic.update({channel:sale})
            
            tv = list(totalDic.keys())
            tq = list(totalDic.values())

            df1 = {'channel':tv,'quantity':tq}
            tdf = pd.DataFrame(df1)

            #for cancellation
            cancelData = cancelData.filter(customername__contains=channelName)
            cancelResult = (cancelData.values('vendor').annotate(quantity=Sum('quantity')).order_by())
            cancelDic = {}
            for i in range(0,len(cancelResult)):
                channel = cancelResult[i]['vendor']
                sale = cancelResult[i]['quantity']
                cancelDic.update({channel:sale})

            ctv = list(cancelDic.keys())
            ctq = list(cancelDic.values())

            df2 = {'channel':ctv,'cancelled':ctq}
            cdf = pd.DataFrame(df2)

            df = tdf.merge(cdf,on='channel',how='outer')
            df = df.replace(np.nan,0)
            df.sort_values(by=['quantity'], inplace=True,ascending=False)
            # print(df)

            ch = list(df['channel'])
            qu = list(df['quantity'])
            cqu = list(df['cancelled'])

            for i in range(0,len(ch)):
                try:
                    ch[i] = ch[i][0:20]+" ...."
                    # print(ch[i])
                except:
                    ch[i] = 'Name not Avaliable'
            qu = list(map(int, qu))
            cqu = list(map(int, cqu))
            net = []
            
            cancelsalePer = []
            for i in range(0,len(qu)):
                net.append(qu[i]-cqu[i])
                try :
                    a = (cqu[i]/qu[i])*100
                    cancelsalePer.append(round(a,2))
                    
                except:
                    cancelsalePer.append(0)
            # print(cancelsalePer)

            salPer = []
            for i in range(0,len(cancelsalePer)):
                salPer.append(100 - cancelsalePer[i])
            # print(salPer)

            

            z = zip(qu,cqu,net)
            c = zip(salPer,cancelsalePer)
            # print(len(ch))

            opalFileName = "opal data"+from_date+" - "+to_date
            message = channelName+" "+category+" "+"Net Sale from"+" "+from_date+" - "+to_date
            return render(request,'sales/netSale.html',{
                'zip':z,'channel':ch,'per':c,'message':"Vendor Name",
                'sym':"%",'heading':message,'data':searchresult[0:100],'show':True
                })

        elif channelName != 'None' and category != 'Total':
            # print(category)
            searchresult = searchresult.filter(vendortype__contains=category)
            # print(searchresult)
            searchresult = searchresult.filter(customername__contains=channelName)
            # print(searchresult)
            result = (searchresult.values('vendor').annotate(quantity=Sum('quantity')).order_by())
            # print(result)
            totalDic = {}
            for i in range(0,len(result)):
                channel = result[i]['vendor']
                sale = result[i]['quantity']
                totalDic.update({channel:sale})
            
            tv = list(totalDic.keys())
            tq = list(totalDic.values())

            df1 = {'channel':tv,'quantity':tq}
            tdf = pd.DataFrame(df1)

            c = cancelData.filter(vendortype__contains=category)
            cancelData = c.filter(customername__contains=channelName)
            cancelResult = (cancelData.values('vendor').annotate(quantity=Sum('quantity')).order_by())
            cancelDic = {}

            for i in range(0,len(cancelResult)):
                channel = cancelResult[i]['vendor']
                sale = cancelResult[i]['quantity']
                cancelDic.update({channel:sale})

            ctv = list(cancelDic.keys())
            ctq = list(cancelDic.values())

            df2 = {'channel':ctv,'cancelled':ctq}
            cdf = pd.DataFrame(df2)

            df = tdf.merge(cdf,on='channel',how='outer')
            df = df.replace(np.nan,0)
            df.sort_values(by=['quantity'], inplace=True,ascending=False)
            # print(df)

            ch = list(df['channel'])
            qu = list(df['quantity'])
            cqu = list(df['cancelled'])

            for i in range(0,len(ch)):
                try:
                    ch[i] = ch[i][0:20]+" ...."
                    # print(ch[i])
                except:
                    ch[i] = 'Name not Avaliable'
            qu = list(map(int, qu))
            cqu = list(map(int, cqu))
            net = []
            
            cancelsalePer = []
            for i in range(0,len(qu)):
                net.append(qu[i]-cqu[i])
                try :
                    a = (cqu[i]/qu[i])*100
                    cancelsalePer.append(round(a,2))
                    
                except:
                    cancelsalePer.append(0)
            # print(cancelsalePer)

            salPer = []
            for i in range(0,len(cancelsalePer)):
                salPer.append(100 - cancelsalePer[i])
            # print(salPer)

            

            z = zip(qu,cqu,net)
            c = zip(salPer,cancelsalePer)
            # print(len(ch))

            opalFileName = "opal data"+from_date+" - "+to_date
            message = channelName+" "+category+" "+"Net Sale from"+" "+from_date+" - "+to_date
            return render(request,'sales/netSale.html',{
                'zip':z,'channel':ch,'per':c,'message':"Vendor Name",
                'sym':"%",'heading':message,'data':searchresult[0:100],'show':True
                })

    return render(request,'sales/netSale.html',{'show':False})
def opalNetExport(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename='+opalFileName+'.csv'
    writer = csv.writer(response)   
    writer.writerow(['orderDate','orderId','customerReferenceNumber','invoiceNumber','itemName','quantity','price','amount','Customer Name','orderStatus','shippingCarrier','Vendor'])
    for i in downloadOpalData:
        writer.writerow([i.orderdate,i.orderid,i.customerreferencenumber,i.invoicenumber,i.itemname,i.quantity,i.price,i.amount,i.customername,i.orderstatus,i.shippingcarrier,i.vendor])
    return response


#for opal export
opalTabData = ""
opalTabFileName = ""
@login_required(login_url='login_view')
def opalData(request):
    show = False
    if request.method == 'POST':
        from_date = request.POST.get('startdate')
        to_date = request.POST.get('todate')
        channelName = request.POST.get('channelName')
        status = request.POST.get('status')

        searchresult = TotalOpalData.objects.filter(orderdate__range=(from_date,to_date))
        global opalTabData
        global opalTabFileName
        # downloadOpalData = searchresult

        # print("yes")
        # print(status)
        if channelName == 'None' and status == 'all':

            opalTabData = searchresult
            opalTabFileName = "Opal Data"+" "+from_date+"-"+to_date
            # print(searchresult)
            heading = "Data from"+" "+from_date+" - "+to_date
            return render(request,'sales/opalData.html',{'show':True,'data':searchresult[0:100],
            'heading':heading})

        elif channelName != 'None' and status == 'all':
            searchresult = searchresult.filter(customername__contains=channelName)

            opalTabData = searchresult
            opalTabFileName = channelName+" "+"Opal Data"+" "+from_date+"-"+to_date
            # print(searchresult)
            heading = "Data of "+" "+channelName+" "+from_date+" - "+to_date
            return render(request,'sales/opalData.html',{'show':True,'data':searchresult[0:100],
            'heading':heading
            })

        elif channelName == 'None' and status != 'all':
            searchresult = searchresult.filter(orderstatus__contains=status)

            opalTabData = searchresult
            opalTabFileName = "Opal Data"+" "+status+" "+from_date+"-"+to_date
            # print(searchresult)
            heading = status+" "+"Data"+" "+from_date+" - "+to_date
            return render(request,'sales/opalData.html',{'show':True,'data':searchresult[0:100],
            'heading':heading
            })
    
        elif channelName != 'None' and status != 'all':
            searchresult = searchresult.filter(orderstatus__contains=status)
            searchresult = searchresult.filter(customername__contains=channelName)

            opalTabData = searchresult
            opalTabFileName = channelName+" "+"Opal Data"+" "+status+" "+from_date+"-"+to_date
            # print(searchresult)
            heading = channelName+" "+status+" "+"Data"+" "+from_date+" - "+to_date
            return render(request,'sales/opalData.html',{'show':True,'data':searchresult[0:100],
            'heading':heading
            })
                

    
    return render(request,'sales/opalData.html',{'show':False})
def opalTabExport(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename='+opalTabFileName+'.csv'
    writer = csv.writer(response)   
    writer.writerow(['orderDate','orderId','customerReferenceNumber','invoiceNumber','itemName','quantity','price','amount','Customer Name','orderStatus','shippingCarrier','Vendor'])
    for i in opalTabData:
        writer.writerow([i.orderdate,i.orderid,i.customerreferencenumber,i.invoicenumber,i.itemname,i.quantity,i.price,i.amount,i.customername,i.orderstatus,i.shippingcarrier,i.vendor])
    return response



downloadnon_moverData = ""
fileName_non_mover = "Data"
@login_required(login_url='login_view')
def non_mover(request):

    if request.method == 'POST':

        global downloadnon_moverData
        global fileName_non_mover
        date = request.POST.get('startdate')
        channelName = request.POST.get('channelName')
        time = request.POST.get('time')
        from_date = datetime.strptime(date, '%Y-%m-%d')
        
        dateArr = []
        dateArr.append(from_date)
        for i in range(0,4):
            b = from_date - timedelta(days=int(time))
            dateArr.append(b.date())
            c = b - timedelta(days=int(1))
            dateArr.append(c.date())
            from_date = c
        print(dateArr)

        downloadnon_moverData = TotalOpalData.objects.filter(orderdate__range=(str(dateArr[5]),str(dateArr[0].date())))

        q1 = TotalOpalData.objects.filter(orderdate__range=(str(dateArr[1]),str(dateArr[0].date())))
        q2 = TotalOpalData.objects.filter(orderdate__range=(str(dateArr[3]),str(dateArr[2])))
        q3 = TotalOpalData.objects.filter(orderdate__range=(str(dateArr[5]),str(dateArr[4])))

        nonmover_sku = list(NonMover.objects.values_list('sku',flat=True))
        
        #for download the data
        downloadnon_moverData = downloadnon_moverData.filter(itemname__in=nonmover_sku)


        inter1 = q1.filter(itemname__in = nonmover_sku)
        inter2 = q2.filter(itemname__in = nonmover_sku)
        inter3 = q3.filter(itemname__in = nonmover_sku)

        d1 = {}
        d2 = {}
        d3 = {}
        for i in range(0,len(inter1)):
            if inter1[i].customername in d1:
                d1[inter1[i].customername] += inter1[i].quantity
            else:
                d1[inter1[i].customername] = inter1[i].quantity
        for i in range(0,len(inter2)):
            if inter2[i].customername in d2:
                d2[inter2[i].customername] += inter2[i].quantity
            else:
                d2[inter2[i].customername] = inter2[i].quantity
        for i in range(0,len(inter3)):
            if inter3[i].customername in d3:
                d3[inter3[i].customername] += inter3[i].quantity
            else:
                d3[inter3[i].customername] = inter3[i].quantity

        fd1 = {}
        fd2 = {}
        fd3 = {}
        id1 = sorted(d1.items(), key=lambda item: item[1],reverse = True)
        id2 = sorted(d2.items(), key=lambda item: item[1],reverse = True)
        id3 = sorted(d3.items(), key=lambda item: item[1],reverse = True)

        for i in range(0,len(id1)):
            fd1[id1[i][0]] = id1[i][1]
            
        for i in range(0,len(id2)):
            fd2[id2[i][0]] = id2[i][1]
        
        for i in range(0,len(id3)):
            fd3[id3[i][0]] = id3[i][1]

        # print(fd1)
        # print(fd2)
        # print(fd3)
        sd1 = list(fd1.keys())
        vd1 = list(fd1.values())

        sd2 = list(fd2.keys())
        vd2 = list(fd2.values())

        sd3 = list(fd3.keys())
        vd3 = list(fd3.values())

        
    
        df1 = {'channel':sd1,'quantity1':vd1}
        df2 = {'channel':sd2,'quantity2':vd2}
        df3 = {'channel':sd3,'quantity3':vd3}
        df1 = pd.DataFrame(df1)
        df2 = pd.DataFrame(df2)
        df3 = pd.DataFrame(df3)  

        
        df = reduce(lambda x,y: pd.merge(x,y, on='channel', how='outer'), [df1, df2, df3])
        df = df.replace(np.nan,0)


        salesChannel = list(df['channel'])
        vd1 = list(df['quantity1'])
        vd2 = list(df['quantity2'])
        vd3 = list(df['quantity3'])


       
        totalQuantity1 = int(sum(vd1)) 
        totalQuantity2 = int(sum(vd2))
        totalQuantity3 = int(sum(vd3))


        vd1 = list(map(int, vd1))
        vd2 = list(map(int, vd2))
        vd3 = list(map(int, vd3))
        

        a1 = dateArr[0].date()
        b1 = str(a1).split('-')
        f1 = b1[-1]+"/"+b1[-2]+"/"+b1[0]

        a2 = dateArr[1]
        b2 = str(a2).split('-')
        f2 = b2[-1]+"/"+b2[-2]+"/"+b2[0] 

        a3 = dateArr[2]
        b3 = str(a3).split('-')
        f3 = b3[-1]+"/"+b3[-2]+"/"+b3[0]

        a4 = dateArr[3]
        b4 = str(a4).split('-')
        f4 = b4[-1]+"/"+b4[-2]+"/"+b4[0]

        a5 = dateArr[4]
        b5 = str(a5).split('-')
        f5 = b5[-1]+"/"+b5[-2]+"/"+b5[0] 

        a6 = dateArr[5]
        b6 = str(a6).split('-')
        f6 = b6[-1]+"/"+b6[-2]+"/"+b6[0] 
        print(f1, f2, f3, f4, f5, f6)

        if channelName == 'None':
            yes = True
            text = "Quantity Analysis of Non Mover"
            heading = "Channel"
            return render(request,'sales/nonmover.html',{
                'show':True,
                'result':yes,'text':text,'heading':heading,
                'total1':totalQuantity1,'total2':totalQuantity2,'total3':totalQuantity3,
                'channel' : salesChannel,'q1':vd1,'q2':vd2,'q3':vd3,
                'date1':f1,'date2':f2,'date3':f3,'date4':f4, 'date5':f5, 'date6':f6
            })

        elif channelName!='None':

            finalResult1 = inter1.filter(customername__contains= channelName)
            finalResult2 = inter2.filter(customername__contains= channelName)
            finalResult3 = inter3.filter(customername__contains= channelName)
            



            # print("yes1")
            v1 = {}
            v2 = {}
            v3 = {}


            p1 = {}
            p2 = {}
            p3 = {}
            


            for i in range(0,len(finalResult1)):
                if finalResult1[i].itemname in v1:
                    v1[finalResult1[i].itemname] += finalResult1[i].quantity
                    p1[finalResult1[i].itemname] += finalResult1[i].amount
                else:
                    v1[finalResult1[i].itemname] = finalResult1[i].quantity
                    p1[finalResult1[i].itemname] = finalResult1[i].amount

            for i in range(0,len(finalResult2)):
                if finalResult2[i].itemname in v2:
                    v2[finalResult2[i].itemname] += finalResult2[i].quantity
                    p2[finalResult2[i].itemname] += finalResult2[i].amount
                else:
                    v2[finalResult2[i].itemname] = finalResult2[i].quantity
                    p2[finalResult2[i].itemname] = finalResult2[i].amount
            for i in range(0,len(finalResult3)):
                if finalResult3[i].itemname in v3:
                    v3[finalResult3[i].itemname] += finalResult3[i].quantity
                    p3[finalResult3[i].itemname] += finalResult3[i].amount
                else:
                    v3[finalResult3[i].itemname] = finalResult3[i].quantity
                    p3[finalResult3[i].itemname] = finalResult3[i].amount

            

            fsd1 = {}
            fsd2 = {}
            fsd3 = {}

            isd1 = sorted(v1.items(), key=lambda item: item[1],reverse = True)
            isd2 = sorted(v2.items(), key=lambda item: item[1],reverse = True)
            isd3 = sorted(v3.items(), key=lambda item: item[1],reverse = True)

            for i in range(0,len(isd1)):
                fsd1[isd1[i][0]] = isd1[i][1]
            for i in range(0,len(isd2)):
                fsd2[isd2[i][0]] = isd2[i][1]
            for i in range(0,len(isd3)):
                fsd3[isd3[i][0]] = isd3[i][1]

            V1 = list(fsd1.keys())
            L1 = list(fsd1.values())

            V2 = list(fsd2.keys())
            L2 = list(fsd2.values())

            V3 = list(fsd3.keys())
            L3 = list(fsd3.values())

                   


            df1 = {'sku':V1,'quantity1':L1}
            df2 = {'sku':V2,'quantity2':L2}
            df3 = {'sku':V3,'quantity3':L3}


            df1 = pd.DataFrame(df1)
            df2 = pd.DataFrame(df2)
            df3 = pd.DataFrame(df3)

            df = reduce(lambda x,y: pd.merge(x,y, on='sku', how='outer'), [df1, df2, df3])
            df = df.replace(np.nan,0)

            #for price one
            s1 = list(p1.keys())
            sp1 = list(p1.values())
            s2 = list(p2.keys())
            sp2 = list(p2.values())
            s3 = list(p3.keys())
            sp3 = list(p3.values())

            pdf1 = {'sku':s1,'price1':sp1}
            pdf2 = {'sku':s2,'price2':sp2}
            pdf3 = {'sku':s3,'price3':sp3}

            pdf1 = pd.DataFrame(pdf1)
            pdf2 = pd.DataFrame(pdf2)
            pdf3 = pd.DataFrame(pdf3)


            # print("yes1")
            pdf = reduce(lambda x,y: pd.merge(x,y, on='sku', how='outer'), [pdf1, pdf2, pdf3])
            pdf = pdf.replace(np.nan,0) 

            # print(pdf)  

            finalDf = pd.merge(df,pdf,on='sku',how='outer')

            q1 = list(finalDf['quantity1'])[0:100]
            q2 = list(finalDf['quantity2'])[0:100]
            q3 = list(finalDf['quantity3'])[0:100]
            totalquan1 = sum(q1)
            totalquan2 = sum(q2)
            totalquan3 = sum(q3)

            p1 = list(finalDf['price1'])[0:100]
            p2 = list(finalDf['price2'])[0:100]
            p3 = list(finalDf['price3'])[0:100]

            p1 = [round(i,2) for i in p1]
            p2 = [round(i,2) for i in p2]
            p3 = [round(i,2) for i in p3]

            totalprice1 = sum(p1)
            totalprice2 = sum(p2)
            totalprice3 = sum(p3)

            totalprice1 = round(totalprice1,2)
            totalprice2 = round(totalprice2,2)
            totalprice3 = round(totalprice3,2)

            sku = list(finalDf['sku'])[0:100]

            zip1 = zip(p1,q1)
            zip2 = zip(p2,q2)
            zip3 = zip(p3,q3)

            text = 'SKU Analysis'
            heading = 'SKU' 

            a1 = dateArr[0].date()
            b1 = str(a1).split('-')
            f1 = b1[-1]+"/"+b1[-2]+"/"+b1[0]

            a2 = dateArr[1]
            b2 = str(a2).split('-')
            f2 = b2[-1]+"/"+b2[-2]+"/"+b2[0] 

            a3 = dateArr[2]
            b3 = str(a3).split('-')
            f3 = b3[-1]+"/"+b3[-2]+"/"+b3[0]

            a4 = dateArr[3]
            b4 = str(a4).split('-')
            f4 = b4[-1]+"/"+b4[-2]+"/"+b4[0] 

            a5 = dateArr[4]
            b5 = str(a5).split('-')
            f5 = b5[-1]+"/"+b5[-2]+"/"+b5[0] 

            a6 = dateArr[5]
            b6 = str(a6).split('-')
            f6 = b6[-1]+"/"+b6[-2]+"/"+b6[0] 
            print(f1, f2, f3, f4, f5, f6)


            FinalTotalQuantity = totalquan1+totalquan2+totalquan3
            FinalTotalSales = totalprice1+totalprice2+totalprice3

            return render(request,'sales/nonmover.html',{
                'show':True,
                'text':text,'channel':channelName,'heading':heading,'dollar':'$',
                'finalSales':FinalTotalSales,'finalquantity':FinalTotalQuantity,
                'totalSale1':totalprice1,'totalSale2':totalprice2,'totalSale3':totalprice3,
                'totalQuantity1':totalquan1,'totalQuantity2':totalquan2,'totalQuantity3':totalquan3,
                'vendor' : sku,'lineTotal1':zip1,'lineTotal2':zip2,'lineTotal3':zip3,
                'gv1':p1,'gv2':p2,'gv3':p3,
                'date1':f1,'date2':f2,'date3':f3,'date4':f4,'date5':f5,'date6':f6
            })
            



    return render(request,'sales/nonmover.html')
def non_mover_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename='+"Non Mover"+'.csv'
    writer = csv.writer(response)   
    writer.writerow(['orderDate','orderId','customerReferenceNumber','invoiceNumber','itemName','quantity','price','amount','Customer Name','orderStatus','shippingCarrier','Vendor'])
    for i in downloadnon_moverData:
        writer.writerow([i.orderdate,i.orderid,i.customerreferencenumber,i.invoicenumber,i.itemname,i.quantity,i.price,i.amount,i.customername,i.orderstatus,i.shippingcarrier,i.vendor])
    return response


def importDashoard(request):
    scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
    
    gc = gspread.service_account(filename='sales/forreordering-38e3f0bc72c3.json')
    
    wks = gc.open("RE-ORDER Sheet").sheet1
    
    data = wks.get_all_values()
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    imagesLinks = []
    for i in range(0,len(df['image'])):
        if len(df['image'][i]) > 1:
            link = df['image'][i].split('(')[-1]
            imagesLinks.append(link.split(')')[0])
        else:
            imagesLinks.append("")
    df['image'] = imagesLinks
    
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    print(data)
    context = {'d': data}
  


    return render(request,'sales/import.html',context)








