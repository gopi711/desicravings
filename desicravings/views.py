from django.shortcuts import render, redirect
from django.http.response import HttpResponse, JsonResponse

import mysql.connector
from mysql.connector import Error
from tabulate import tabulate
from datetime import datetime
import os
from django.conf import settings
import json
import re
import psycopg2

def start1(request):
    return render(request,'HomePage.html')
    

def Login(request):
    username= request.POST.get('username')
    password= request.POST.get('password')
    try:
        toggle=request.POST.get('toggleswitch')
        msg1=request.POST.get('orderMessage')
        print(toggle)
        print(msg1)
    except:
        print('Except')
    if(username=='admin' and password=='7064milsap'):
        try:
            DATABASE_URL = os.environ.get('DATABASE_URL')
            con = psycopg2.connect(DATABASE_URL)
            #con = psycopg2.connect(DATABASE_URL)
            cur = con.cursor()
            print('connection successful')
            if(toggle=='on'):
                upd_qry="update Accept_Orders set status='Accept',message='' where id=1;"
                print(upd_qry)
                cur.execute(upd_qry)
            elif(toggle=='off'):
                upd_qry="update Accept_Orders set status='Do Not Accept',message='"+str(msg1)+"' where id=1;"
                print(upd_qry)
                cur.execute(upd_qry)
            insrt_qry="select * from Accept_Orders;"
            print(insrt_qry)
            cur.execute(insrt_qry)
            result=cur.fetchall()
            print(result)
            status=result[0][1]
            msg=result[0][2]
            print(status+'-'+msg)
            insrt_qry="select * from orders_items o1,orders_customers o2 where o1.itemstatus='Placed' and o1.orderid=o2.orderid;"
            print(insrt_qry)
            cur.execute(insrt_qry)
            result=cur.fetchall()
            print(result)
            menu_list = []  # Initialize an empty list to store menu items
            for i in result:
                # Construct the JSON-like string with the desired format
                loc_qry="select ImageLoc from Menu_Items where ItemName='"+str(i[1])+"';"
                cur.execute(loc_qry)
                loc_res=cur.fetchall()
                print(loc_res)
                menu_item = {"order_id":str(i[0]),"item_name":str(i[1]),"order_name":str(i[6]),"phone_number":str(i[7]),"quantity":str(i[2]),"status":str(i[4]),"spicy_level":str(i[8]),"order_instructions":str(i[9]),"delivery_option":str(i[10]),"pickup_time":str(i[11]),"order_datetime":str(i[12])}
                #image_filename = str(i[3])  # Get representation of i[3] without escape characters
                #menu_item += image_filename + '" }'  # Complete the menu item string
                menu_list.append(menu_item)  # Append the menu item string to the list
            print(menu_list)
            con.commit()
        except:
            print('Db Connection Unsuccessful')
        return render(request,'Admin.html',{'status':status,'msg':msg,'password':password,'username':username,'orders':menu_list})
    #elif(username=='desicravings' and password=='601fortworth'):
    else:
        try:
            DATABASE_URL = os.environ.get('DATABASE_URL')
            con = psycopg2.connect(DATABASE_URL)
            #con = psycopg2.connect(DATABASE_URL)
            cur = con.cursor()
            print('connection successful')
            insrt_qry="select * from Menu_Items;"
            print(insrt_qry)
            cur.execute(insrt_qry)
            result=cur.fetchall()
            print(result)
            menu_list = []  # Initialize an empty list to store menu items
            for i in result:
                # Construct the JSON-like string with the desired format
                menu_item = {"name":str(i[0]),"description":str(i[2]),"price":("$"+str(i[1])),"quantity":str(i[4]),"image":"/static/"+str(i[3])+''}
                #image_filename = str(i[3])  # Get representation of i[3] without escape characters
                #menu_item += image_filename + '" }'  # Complete the menu item string
                menu_list.append(menu_item)  # Append the menu item string to the list
            print(menu_list)
            acceptorders_qry='select * from Accept_Orders;'
            print(acceptorders_qry)
            cur.execute(acceptorders_qry)
            result=cur.fetchall()
            print(result[0][2])
            if(result[0][1]=='Do Not Accept'):
                print('if')
                msg=str(result[0][2])
                print(msg)
                return render(request,'NotAcceptingOrders.html',{'msg':msg})
        except:
            print('Db Connection Unsuccessful')
        return render(request,'UserPage.html',{'menu_items':menu_list})
    #else:
    #    return render(request,'HomePage.html')

def admincancelitem(request):
    orderid=request.POST.get('orderidcancel')
    print(orderid)
    try:
        DATABASE_URL = os.environ.get('DATABASE_URL')
        con = psycopg2.connect(DATABASE_URL)
        #con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        print('connection successful')
        insrt_qry="select * from Accept_Orders;"
        print(insrt_qry)
        cur.execute(insrt_qry)
        result=cur.fetchall()
        print(result)
        status=result[0][1]
        msg=result[0][2]
        print(status+'-'+msg)
        if(orderid.split('-')[0]=='Complete'):
            upd_qry="update orders_items set itemstatus='Completed' where orderid="+str(orderid.split('-')[1].split(',')[0])+" and itemname='"+str(orderid.split('-')[1].split(',')[1])+"';"
            print(upd_qry)
            cur.execute(upd_qry)
        elif(orderid.split('-')[0]=='Cancel'):
            upd_qry="update orders_items set itemstatus='Cancelled' where orderid="+str(orderid.split('-')[1].split(',')[0])+" and itemname='"+str(orderid.split('-')[1].split(',')[1])+"';"
            print(upd_qry)
            cur.execute(upd_qry)
        insrt_qry="select * from orders_items o1,orders_customers o2 where o1.itemstatus='Placed' and o1.orderid=o2.orderid;"
        print(insrt_qry)
        cur.execute(insrt_qry)
        result=cur.fetchall()
        print(result)
        menu_list = []  # Initialize an empty list to store menu items
        for i in result:
            # Construct the JSON-like string with the desired format
            loc_qry="select ImageLoc from Menu_Items where ItemName='"+str(i[1])+"';"
            cur.execute(loc_qry)
            loc_res=cur.fetchall()
            print(loc_res)
            menu_item = {"order_id":str(i[0]),"item_name":str(i[1]),"order_name":str(i[6]),"phone_number":str(i[7]),"quantity":str(i[2]),"status":str(i[4]),"spicy_level":str(i[8]),"order_instructions":str(i[9]),"delivery_option":str(i[10]),"pickup_time":str(i[11]),"order_datetime":str(i[12])}
            #image_filename = str(i[3])  # Get representation of i[3] without escape characters
            #menu_item += image_filename + '" }'  # Complete the menu item string
            menu_list.append(menu_item)  # Append the menu item string to the list
        print(menu_list)
        con.commit()
    except:
        print('Db Connection Unsuccessful')
    return render(request,'Admin.html',{'status':status,'msg':msg,'orders':menu_list})

def adminMenu(request):
    try:
        DATABASE_URL = os.environ.get('DATABASE_URL')
        con = psycopg2.connect(DATABASE_URL)
        #con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        print('connection successful')
        insrt_qry="select * from Menu_Items;"
        print(insrt_qry)
        cur.execute(insrt_qry)
        result=cur.fetchall()
        print(result)
        menu_list=[]
        for i in result:
            dict1={'name':i[0],'price':i[1]}
            menu_list.append(dict1)
    except:
        print('Db Connection Unsuccessful')
    return render(request,'adminMenu.html',{'menu_items':menu_list})

def addnewitem(request):
    print('request:',request.FILES)
    name=request.POST.get('name')
    price=request.POST.get('price')
    description=request.POST.get('itemdescription')
    imageloc=''
    print('image name:'+str(imageloc))
    if 'image1' in request.FILES:
        uploaded_file = request.FILES['image1']
        imageloc=request.FILES['image1']
        upload_dir = os.path.join(settings.BASE_DIR, "static")
        with open(os.path.join(upload_dir, uploaded_file.name), 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
    try:
        DATABASE_URL = os.environ.get('DATABASE_URL')
        con = psycopg2.connect(DATABASE_URL)
        #con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        print('connection successful')
        insrt_qry="insert into Menu_Items values('"+str(name)+"',"+str(price)+",'"+str(description)+"','"+str(imageloc)+"',0);"
        print(insrt_qry)
        cur.execute(insrt_qry)
        #print('query executed:'+insrt_qry)
        insrt_qry="select * from Menu_Items;"
        print(insrt_qry)
        cur.execute(insrt_qry)
        result=cur.fetchall()
        print(result)
        menu_list=[]
        for i in result:
            dict1={'name':i[0],'price':i[1]}
            menu_list.append(dict1)
        con.commit()
    except:
        print('Db Connection Unsuccessful')
    return render(request,'addnewitem.html',{'menu_items':menu_list})

def UpdateItem(request):
    try:
        DATABASE_URL = os.environ.get('DATABASE_URL')
        con = psycopg2.connect(DATABASE_URL)
        #con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        print('connection successful')
        insrt_qry="select * from Menu_Items;"
        print(insrt_qry)
        cur.execute(insrt_qry)
        result=cur.fetchall()
        print(result)
        items=[]
        for i in result:
            dict1={'name':i[0]}
            items.append(dict1)
    except:
        print('except')
    print(items)
    return render(request,'UpdateItem.html',{'items':items})

def UpdateItemData(request):
    name=request.POST.get('selected_item_name1')
    if(name is None):
        name=request.POST.get('selected_item_name')
    action=request.POST.get('performupdate')
    price=request.POST.get('updateprice')
    description=request.POST.get('updatedescription')
    quantity=request.POST.get('updatequantity')
    location=''
    print(request.FILES)
    if 'updateimage1' in request.FILES:
        uploaded_file = request.FILES['updateimage1']
        location=request.FILES['updateimage1']
        upload_dir = os.path.join(settings.BASE_DIR, "static")
        with open(os.path.join(upload_dir, uploaded_file.name), 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
    print('name:'+str(name)+str(price)+str(description)+str(quantity)+str(action))
    try:
        DATABASE_URL = os.environ.get('DATABASE_URL')
        con = psycopg2.connect(DATABASE_URL)
        #con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        print('connection successful')
        insrt_qry="select * from Menu_Items;"
        print(insrt_qry)
        cur.execute(insrt_qry)
        result=cur.fetchall()
        print(result)
        items=[]
        for i in result:
            dict1={'name':i[0]}
            items.append(dict1)
        select_qry="select * from Menu_Items where ItemName='"+str(name)+"';"
        print(select_qry)
        cur.execute(select_qry)
        result=cur.fetchall()
        print(result)
        try:
            selecteditemname=result[0][0]
            selecteditemprice=result[0][1]
            selecteditemdescription=result[0][2]
            print(selecteditemdescription)
            selecteditemquantity=result[0][4]
        except:
            print('no item selected')
        print('update pending')
        if(action=='Update'):
            print('action update')
            if(location==''):
                upd_qry="update Menu_Items set ItemPrice="+str(price)+",ItemDescription='"+str(description)+"',quantity="+str(quantity)+" where ItemName='"+str(name)+"';"
            else:
                upd_qry="update Menu_Items set ItemPrice="+str(price)+",ItemDescription='"+str(description)+"',quantity="+str(quantity)+",ImageLoc='"+str(location)+"' where ItemName='"+str(name)+"';"
            print(upd_qry)
            cur.execute(upd_qry)
            con.commit()
            return render(request,'UpdateItem.html',{'items':items})
    except:
        print('except')
    print(items)
    return render(request,'UpdateItemdata.html',{'items':items,'selecteditemname':selecteditemname,'selecteditemprice':selecteditemprice,'selecteditemdescription':selecteditemdescription,'selecteditemquantity':selecteditemquantity})

def DeleteItem(request):
    try:
        DATABASE_URL = os.environ.get('DATABASE_URL')
        con = psycopg2.connect(DATABASE_URL)
        #con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        print('connection successful')
        insrt_qry="select * from Menu_Items;"
        print(insrt_qry)
        cur.execute(insrt_qry)
        result=cur.fetchall()
        print(result)
        items=[]
        for i in result:
            dict1={'name':i[0]}
            items.append(dict1)
    except:
        print('except')
    print(items)
    return render(request,'DeleteItem.html',{'items':items})

def DeleteItemData(request):
    name=request.POST.get('selected_item_name1')
    if(name is None):
        name=request.POST.get('selected_item_name')
    action=request.POST.get('performupdate')
    price=request.POST.get('updateprice')
    description=request.POST.get('updatedescription')
    quantity=request.POST.get('updatequantity')
    print('name:'+str(name)+str(price)+str(description)+str(quantity)+str(action))
    try:
        DATABASE_URL = os.environ.get('DATABASE_URL')
        con = psycopg2.connect(DATABASE_URL)
        #con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        print('connection successful')
        if(action=='Delete'):
            print('action delete')
            upd_qry="delete from Menu_Items where ItemName='"+str(name)+"';"
            print(upd_qry)
            cur.execute(upd_qry)
        insrt_qry="select * from Menu_Items;"
        print(insrt_qry)
        cur.execute(insrt_qry)
        result=cur.fetchall()
        print(result)
        items=[]
        for i in result:
            dict1={'name':i[0]}
            items.append(dict1)
        select_qry="select * from Menu_Items where ItemName='"+str(name)+"';"
        print(select_qry)
        cur.execute(select_qry)
        result=cur.fetchall()
        print(result)
        try:
            selecteditemname=result[0][0]
            selecteditemprice=result[0][1]
            selecteditemdescription=result[0][2]
            print(selecteditemdescription)
            selecteditemquantity=result[0][4]
        except:
            print('no item selected')
        print('delete pending')
        if(action=='Delete'):
            con.commit()
            return render(request,'DeleteItem.html',{'items':items})
    except:
        print('except')
    print(items)
    return render(request,'DeleteItemdata.html',{'items':items,'selecteditemname':selecteditemname,'selecteditemprice':selecteditemprice,'selecteditemdescription':selecteditemdescription,'selecteditemquantity':selecteditemquantity})

def cartitems(request):
    cart_items=request.POST.get('cart-items','')
    print('cart items')
    print(cart_items)
    return render(request,'Cart.html',{'cartitemslist':cart_items})

def personal_info(request):
    itemslist=request.POST.get('personal_info')
    print(itemslist)
    return render(request,'personal_info.html',{'orderlistitems':itemslist})

def placeorder(request):
    itemslist=request.POST.get('orderlistitems')
    orderPersonalInfo=request.POST.get('orderPersonalInfo')
    #print(itemslist)
    #print(orderPersonalInfo)
    orderPersonalInfo=orderPersonalInfo[orderPersonalInfo.index('orderName'):orderPersonalInfo.index(',orderPersonalInfo-')]
    print(orderPersonalInfo)
    attributes={}
    pattern = r'(\w+)-([\w\s:]+),'
    matches = re.findall(pattern,orderPersonalInfo)
    for match in matches:
        key = match[0]
        value = match[1]
        attributes[key] = value
    print(attributes)
    items_start_index = orderPersonalInfo.find("orderlistitems-") + len("orderlistitems-")
    items_end_index = orderPersonalInfo.find(",,", items_start_index)
    items_list = orderPersonalInfo[items_start_index:items_end_index]
    items = items_list.split(',')

    item_details = []
    for item in items:
        details = item.strip().split()
        item_name = ' '.join(details[:-3])
        quantity = int(details[-3])
        total_price = float(details[-1])
        item_details.append((item_name, quantity, total_price))
    print(item_details)
    try:
        DATABASE_URL = os.environ.get('DATABASE_URL')
        con = psycopg2.connect(DATABASE_URL)
        #con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        print('connection successful')
        insrt_qry="select max(orderid) from orders_customers;"
        print(insrt_qry)
        cur.execute(insrt_qry)
        result=cur.fetchall()
        print(result)
        orderid=1
        try:
            if(result[0][0]>0):
                orderid=result[0][0]+1
        except:
            print('Issue with orderid')
        print(orderid)
        currentdate_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(attributes)
        keys = attributes.keys()
        print(keys)
        values = [attributes[key] for key in keys]
        values=[orderid]+values
        print(values)
        if 'pickupTimeSelect' in keys:
            print('if')
            insrt_qry="INSERT INTO orders_customers (orderid, ordername, phonenumber, spicylevel, orderInstructions, deliveryoption, pickuptime,order_date) VALUES ("+str(values[0])+",'"+str(values[1])+"','"+str(values[2])+"','"+str(values[3])+"','"+str(values[4])+"','"+str(values[5])+"','"+str(values[6])+"','"+str(currentdate_time)+"');"
            print(insrt_qry)
            cur.execute(insrt_qry)
        else:
            print('else')
            cur.execute("INSERT INTO orders_customers (orderid, ordername, phonenumber, spicylevel, orderInstructions, deliveryoption,order_date) VALUES ("+str(values[0])+",'"+str(values[1])+"','"+str(values[2])+"','"+str(values[3])+"','"+str(values[4])+"','"+str(values[5])+"','"+str(currentdate_time)+"');")
        for item in item_details:
            print('items')
            insrt_qry="INSERT INTO orders_items VALUES ("+str(orderid)+",'"+str(item[0])+"',"+str(item[1])+","+str(item[2])+",'Placed');"
            print(insrt_qry)
            cur.execute(insrt_qry)
        con.commit()
    except:
        print('except')
    return render(request,'placeorder.html',{'itemslist':itemslist,'currentdate_time':currentdate_time,'orderid':orderid})

def track(request):
    phonenumber='0'
    try:
        orderid=request.POST.get('orderid')
        print(orderid)
        phonenumber=request.POST.get('mobile')
        print(phonenumber)
    except:
        print('Except')
    try:
        DATABASE_URL = os.environ.get('DATABASE_URL')
        con = psycopg2.connect(DATABASE_URL)
        #con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        print('connection successful')
        if(phonenumber is not None and phonenumber!=''):
            ord_find_qry="SELECT o1.orderid FROM orders_items o1,orders_customers o2 WHERE o1.orderid=o2.orderid and o1.itemstatus = 'Placed' and o2.phonenumber='"+str(phonenumber)+"' UNION SELECT MAX(o3.orderid) FROM orders_items o3,orders_customers o4 where o3.orderid=o4.orderid and o4.phonenumber='"+str(phonenumber)+"' and NOT EXISTS (SELECT 1 FROM orders_items o1,orders_customers o2 WHERE o1.orderid=o2.orderid and o1.itemstatus = 'Placed' and o2.phonenumber='"+str(phonenumber)+"');"
            print(ord_find_qry)
            cur.execute(ord_find_qry)
            result=cur.fetchall()
            print(result)
            orderid='('
            if(result[-1][0] is None):
                n=len(result)-1
            else:
                n=len(result)
            for i in range(0,n):
                print(orderid)
                orderid=str(orderid)+str(result[i][0])+','
                print(result[i][0])
            orderid=orderid[:len(orderid)-1]+')'
            insrt_qry="select * from orders_items where orderid in "+str(orderid)+";"
            orderid=orderid.replace('(','').replace(')','')
        else:
            insrt_qry="select * from orders_items where orderid="+str(orderid)+";"
        print(insrt_qry)
        cur.execute(insrt_qry)
        result=cur.fetchall()
        print(result)
        menu_list = []  # Initialize an empty list to store menu items
        for i in result:
            # Construct the JSON-like string with the desired format
            loc_qry="select ImageLoc from Menu_Items where ItemName='"+str(i[1])+"';"
            cur.execute(loc_qry)
            loc_res=cur.fetchall()
            print(loc_res)
            menu_item = {"name":str(i[1]),"quantity":str(i[2]),"image":"/static/"+str(loc_res[0][0])+'',"status":str(i[4]),"orderid":str(i[0])}
            #image_filename = str(i[3])  # Get representation of i[3] without escape characters
            #menu_item += image_filename + '" }'  # Complete the menu item string
            menu_list.append(menu_item)  # Append the menu item string to the list
        print(menu_list)
    except:
        print('Except: Track')
        return render(request,'input_tracking.html')
    return render(request,'tracking.html',{'orderid':orderid,'order_items':menu_list})

def completeorder(request):
    response_data = {'message': 'Success!'}
    return JsonResponse(response_data)

def usercancelitem(request):
    item_id = request.POST.get('orderid')
    itemName=request.POST.get('itemname')
    print(item_id)
    print(itemName)
    orderid=item_id
    try:
        DATABASE_URL = os.environ.get('DATABASE_URL')
        con = psycopg2.connect(DATABASE_URL)
        #con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        print('connection successful')
        insrt_qry="update orders_items set itemstatus='Cancelled' where orderid="+str(item_id)+" and itemname='"+itemName+"';"
        print(insrt_qry)
        cur.execute(insrt_qry)
        insrt_qry="select * from orders_items where orderid="+str(orderid)+";"
        print(insrt_qry)
        cur.execute(insrt_qry)
        result=cur.fetchall()
        print(result)
        menu_list = []  # Initialize an empty list to store menu items
        for i in result:
            # Construct the JSON-like string with the desired format
            loc_qry="select ImageLoc from Menu_Items where ItemName='"+str(i[1])+"';"
            cur.execute(loc_qry)
            loc_res=cur.fetchall()
            print(loc_res)
            menu_item = {"name":str(i[1]),"quantity":str(i[2]),"image":"/static/"+str(loc_res[0][0])+'',"status":str(i[4]),"orderid":str(i[0])}
            #image_filename = str(i[3])  # Get representation of i[3] without escape characters
            #menu_item += image_filename + '" }'  # Complete the menu item string
            menu_list.append(menu_item)  # Append the menu item string to the list
        print(menu_list)
        con.commit()
    except:
        print('Except: UserCancellation')
    return render(request,'tracking.html',{'orderid':orderid,'order_items':menu_list})

def trackorder(request):
    return render(request,'input_tracking.html')

