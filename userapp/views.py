from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
import datetime
import mysql.connector
import random
import requests

def getdb():
    mydb = mysql.connector.connect(host="localhost",user="root", passwd="",database="health_db")
    return mydb

def uindex(request):
    try:

        selsp = "select * from specialization_tb where s_status = 'Active' order by s_id desc " 
        mydb = getdb()
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute(selsp)
        s_data = mycursor.fetchall()

        selfd = "select * from feedback_tb where f_status = 'Show' order by f_id desc " 
        mydb = getdb()
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute(selfd)
        f_data = mycursor.fetchall()
        
        alldata ={
            's_data' : s_data,
            'f_data' : f_data,
        }

        return render(request,'uindex.html',alldata)
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def ucontact(request):
    try:

        if request.POST:
            
            f_name = request.POST.get("f_name")
            f_contact = request.POST.get("f_contact")
            f_message = request.POST.get("f_message")
            f_status = 'Hide'
            cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            ins = "INSERT INTO `feedback_tb`(`f_name`, `f_contact`, `f_message`, `f_status`, `f_cdate`, `f_udate`) VALUES ('"+str(f_name)+"','"+str(f_contact)+"','"+str(f_message)+"','"+str(f_status)+"','"+cdate+"','"+cdate+"')" 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(ins)
            mydb.commit()
            return redirect("ucontact")
        
        else:
            return render(request,'ucontact.html',{})

    except NameError:
        print("internal error")
    except:
        print('Error returned')

def uabout(request):
    try:
        
        return render(request,'uabout.html',{})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def ulogin(request):
    try:
        msg=""
        if request.POST:
            u_contact = request.POST.get("u_contact")
            u_password = request.POST.get("u_password")
            
            sel="select * from user_tb where u_contact='"+str(u_contact)+"' and u_password= '"+str(u_password)+"'"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            l_data = mycursor.fetchall()
            if len(l_data)>0:

                request.session["uid"] = l_data[0]["u_id"]
                request.session["ucontact"] = u_contact
                request.session["uimg"] = l_data[0]["u_image"]
                request.session["utime"] = str(l_data[0]["u_udate"])
                request.session["uusername"] = l_data[0]["u_name"]
                

                return redirect("uindex")
            else:
                msg="Invalid Username Or Password.!"
                return render(request,'ulogin.html',{'msg':msg})
        else:
            return render(request,'ulogin.html',{'msg':msg})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def ulogout(request):

    try:
        
        u_id = request.session["uid"]
        cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        update = "update user_tb set u_udate = '"+cdate+"' where u_id='"+str(u_id)+"'" 
        mydb = getdb()
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute(update)
        mydb.commit()

        request.session["uid"] = None
        request.session["ucontact"] = None
        request.session["uimg"] = None
        request.session["utime"] = None
        request.session["uusername"] = None

        return redirect("uindex")
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def uprofile(request):
    try:
        if request.POST:
            u_id = request.session["uid"] 
            u_name = request.POST.get("u_name")
            u_contact = request.POST.get("u_contact")
            u_address = request.POST.get("u_address")
            u_gender = request.POST.get("u_gender")

            if request.POST.get("u_image") !="":
                u_image = request.FILES["u_image"]
                img = FileSystemStorage()
                old_img1 = img.save(u_image.name,u_image)
            else:
                old_img1 = request.POST.get("old_img1")

            if request.POST.get("u_idproof") !="":
                u_idproof = request.FILES["u_idproof"]
                img = FileSystemStorage()
                old_img2 = img.save(u_idproof.name,u_idproof)
            else:
                old_img2 = request.POST.get("old_img2")

            if request.POST.get("u_income") !="":
                u_income = request.FILES["u_income"]
                img = FileSystemStorage()
                old_img3 = img.save(u_income.name,u_income)
            else:
                old_img3 = request.POST.get("old_img3")

            u_dob = request.POST.get("u_dob")
            u_bloodgroup = request.POST.get("u_bloodgroup")
            u_password = request.POST.get("u_password") 
            u_smartcard = request.POST.get("u_smartcard")
            u_discount = request.POST.get("u_discount")

            cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            update = "update user_tb set u_name = '"+str(u_name)+"',u_address = '"+str(u_address)+"',u_gender = '"+str(u_gender)+"',u_image = '"+str(old_img1)+"',u_idproof = '"+str(old_img2)+"',u_income = '"+str(old_img3)+"',u_dob = '"+str(u_dob)+"',u_bloodgroup = '"+str(u_bloodgroup)+"',u_password = '"+str(u_password)+"' , u_udate = '"+cdate+"' where u_id='"+str(u_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(update)
            mydb.commit()
            return redirect("uindex")

        else:
            
            u_id = request.session["uid"] 
           
            sel = "select * from user_tb where u_id='"+str(u_id)+"'"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            u_data = mycursor.fetchall()

        return render(request,'uprofile.html',{'u_data':u_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def usignup(request):
    try:
        msg=""
        if request.POST:

            rtype = request.GET.get("verify")

            if rtype == 'number':

                u_contact= request.POST.get("u_contact")
              

                sel = "select * from user_tb where u_contact='"+str(u_contact)+"' and u_status = 'Active' "
                mydb = getdb()
                mycursor = mydb.cursor(dictionary=True)
                mycursor.execute(sel)
                u_data = mycursor.fetchall()
              

                if len(u_data)>0:
                    msg = "Already Register User.!"
                    return render(request,'usignup.html',{'msg':msg})

                else:
                    otp = random.randrange(1000,9999)
                    mtype = "OTP"
                    request.session['otp'] = otp
                    request.session['contact'] = u_contact

                    sms_url = f"https://invisionsoftwaresolution.in/Student/isssmssend.php?contact={u_contact}&message={otp}&type={mtype}"
                    response = requests.post(sms_url)
                    return redirect('/usignup?verify=otp')
                
            elif rtype == 'otp':
                u_otp = request.POST.get("u_otp")
                otp = request.session['otp']
                if u_otp == str(otp):
                    return redirect('/usignup?verify=usignup')
                else:
                     msg = "Invalid OTP..!"
                     return render(request,'usignup.html',{'msg':msg}) 
            
            else: 
                u_name = request.POST.get("u_name")
                u_contact = request.POST.get("u_contact")
                
                u_dob = request.POST.get("u_dob")
            

                u_image = request.FILES["u_image"]
                img = FileSystemStorage()
                u_image = img.save(u_image.name,u_image)

                u_idproof = request.FILES["u_idproof"]
                img = FileSystemStorage()
                u_idproof = img.save(u_idproof.name,u_idproof)

                u_income = request.FILES["u_income"]
                img = FileSystemStorage()
                u_income = img.save(u_income.name,u_income)                
                
                u_gender = request.POST.get("u_gender")
                u_bloodgroup = request.POST.get("u_bloodgroup")
                u_password = request.POST.get("u_password") 
                u_address = request.POST.get("u_address")
                u_smartcard = '0'
                u_discount = '0'
                u_status = 'Active'

                cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ins = "INSERT INTO `user_tb`( `u_name`, `u_contact`, `u_address`, `u_gender`, `u_image`, `u_idproof`, `u_income`, `u_dob`, `u_bloodgroup`, `u_password`, `u_smartcard`, `u_discount`, `u_status`, `u_cdate`, `u_udate`)VALUES ('"+str(u_name)+"','"+str(u_contact)+"','"+str(u_address)+"','"+str(u_gender)+"','"+str(u_image)+"','"+str(u_idproof)+"','"+str(u_income)+"','"+str(u_dob)+"','"+str(u_bloodgroup)+"','"+str(u_password)+"','"+str(u_smartcard)+"','"+str(u_discount)+"','"+str(u_status)+"','"+cdate+"','"+cdate+"')"
                mydb = getdb()
                mycursor = mydb.cursor(dictionary=True)
                mycursor.execute(ins)
                mydb.commit()
                return redirect("uindex")
        else:
            return render(request,'usignup.html',{'msg':msg})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def resendotp(request):
    try:
        otp = random.randrange(1000,9999)
        mtype = "OTP"
        request.session['otp'] = otp
        u_contact = request.session['contact'] 

        sms_url = f"https://invisionsoftwaresolution.in/Student/isssmssend.php?contact={u_contact}&message={otp}&type={mtype}"
        response = requests.post(sms_url)
        return redirect('/usignup?verify=otp')
        
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def dsignup(request):
    try:
        msg=""
        
        if request.POST:

            rtype = request.GET.get("verify")

            if rtype == 'number':

                d_contact= request.POST.get("d_contact")
        
            
                sel = "select * from doctor_tb where d_contact='"+str(d_contact)+"' and d_status = 'Active' "
                mydb = getdb()
                mycursor = mydb.cursor(dictionary=True)
                mycursor.execute(sel)
                d_data = mycursor.fetchall()

                if len(d_data)>0:
                    msg = "Already Register Doctor.!"
                    return render(request,'dsignup.html',{'msg':msg})

                else:
                    otp = random.randrange(1000,9999)
                    mtype = "OTP"
                    request.session['otp'] = otp
                    request.session['dcontact'] = d_contact

                    sms_url = f"https://invisionsoftwaresolution.in/Student/isssmssend.php?contact={d_contact}&message={otp}&type={mtype}"
                    response = requests.post(sms_url)
                    return redirect('/dsignup?verify=otp')
                
            elif rtype == 'otp':
                u_otp = request.POST.get("u_otp")
                otp = request.session['otp']
                if u_otp == str(otp):
                    return redirect('/dsignup?verify=dsignup')
                else:
                     msg = "Invalid OTP..!"
                     return render(request,'dsignup.html',{'msg':msg}) 
                            
            else: 
                s_id = request.POST.get("s_id")
                d_hospitalname = request.POST.get("d_hospitalname")
                d_name = request.POST.get("d_name")
            
                d_image = request.FILES["d_image"]
                img = FileSystemStorage()
                d_image = img.save(d_image.name,d_image)

                d_certificate = request.FILES["d_certificate"]
                img = FileSystemStorage()
                d_certificate = img.save(d_certificate.name,d_certificate)                
                
                d_contact = request.POST.get("d_contact")
                d_address = request.POST.get("d_address")
                d_gender = request.POST.get("d_gender") 
                d_experience = request.POST.get("d_experience")
                d_fees = request.POST.get("d_fees")
                d_password = request.POST.get("d_password")
                d_status = 'Active'

                cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                ins = "INSERT INTO `doctor_tb`( `s_id`, `d_hospitalname`, `d_name`, `d_contact`, `d_address`, `d_gender`, `d_image`, `d_experience`, `d_certificate`, `d_fees`, `d_password`, `d_status`, `d_cdate`, `d_udate`)  VALUES ('"+str(s_id)+"','"+str(d_hospitalname)+"','"+str(d_name)+"','"+str(d_contact)+"','"+str(d_address)+"','"+str(d_gender)+"','"+str(d_image)+"','"+str(d_experience)+"','"+str(d_certificate)+"','"+str(d_fees)+"','"+str(d_password)+"','"+str(d_status)+"','"+cdate+"','"+cdate+"')"
                mydb = getdb()
                mycursor = mydb.cursor(dictionary=True)
                mycursor.execute(ins)
                mydb.commit()
                return redirect("uindex")
        else:

            sels = "select * from specialization_tb where s_status='Active'"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sels)
            s_data = mycursor.fetchall()
            
            return render(request,'dsignup.html',{'s_data':s_data,'msg':msg,})

    except NameError:
        print("internal error")
    except:
        print('Error returned')

def dresendotp(request):
    try:
        otp = random.randrange(1000,9999)
        mtype = "OTP"
        request.session['otp'] = otp
        d_contact = request.session['dcontact'] 

        sms_url = f"https://invisionsoftwaresolution.in/Student/isssmssend.php?contact={d_contact}&message={otp}&type={mtype}"
        response = requests.post(sms_url)
        return redirect('/dsignup?verify=otp')
        
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def uforgotpassword(request):
    try:
        msg = ""
        if request.POST:
            u_contact = request.POST.get("u_contact")
           
            sel = "select * from user_tb where u_contact =  '"+str(u_contact)+"' and u_status = 'Active'"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            udata = mycursor.fetchall()
            
   
            if len(udata) > 0:
                
                upassword = udata[0]["u_password"]

                mtype = "Forgotpassword"

                sms_url = f"https://invisionsoftwaresolution.in/Student/isssmssend.php?contact={u_contact}&message={upassword}&type={mtype}"
                response = requests.post(sms_url)

                return redirect('/?alert=1')
                
            else:
                msg = "Contact Number Is Not Registered.!" 
                return render(request,'uforgotpassword.html',{'msg':msg})  
        else:
            return render(request,'uforgotpassword.html',{'msg' : msg})
    except NameError:
        print("internal error")
    except:
        print('Error returned')    

def dforgotpassword(request):
    try:
        msg = ""
        if request.POST:
            d_contact = request.POST.get("d_contact")
           
            sel = "select * from doctor_tb where d_contact =  '"+str(d_contact)+"' and d_status = 'Active'"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            udata = mycursor.fetchall()
            
   
            if len(udata) > 0:
                
                upassword = udata[0]["d_password"]

                mtype = "Forgotpassword"

                sms_url = f"https://invisionsoftwaresolution.in/Student/isssmssend.php?contact={d_contact}&message={upassword}&type={mtype}"
                response = requests.post(sms_url)

                return redirect('/?alert=1')
                
            else:
                msg = "Contact Number Is Not Registered.!" 
                return render(request,'dforgotpassword.html',{'msg':msg})  
        else:
            return render(request,'dforgotpassword.html',{'msg' : msg})
    except NameError:
        print("internal error")
    except:
        print('Error returned')    

def umyappointment(request):
    try:
         if request.GET.get("a_id") !=None:
            a_id = request.GET.get("a_id")

            dele = "delete from appointment_tb where a_id='"+str(a_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(dele)
            mydb.commit()
            return redirect("umyappointment")
        
         else:
            u_id = request.session["uid"]
            sel = "select * from appointment_tb a,user_tb u,doctor_tb d,specialization_tb s where a.u_id = u.u_id and a.d_id = d.d_id and a.s_id = s.s_id and a.u_id='"+str(u_id)+"' order by a.a_id desc" 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            a_data = mycursor.fetchall()

            return render(request,'umyappointment.html',{'a_data':a_data})

    except NameError:
        print("internal error")
    except:
        print('Error returned')

def umytreatment(request):
    try:

        a_id = request.GET.get("a_id")

        sel = "select * from treatment_tb t, appointment_tb a,user_tb u,doctor_tb d where t.a_id=a.a_id and t.u_id=u.u_id and t.d_id=d.d_id  and t.a_id='"+str(a_id)+"' order by t.t_id desc " 
        mydb = getdb()
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute(sel)
        t_data = mycursor.fetchall()

        return render(request,'umytreatment.html',{'t_data':t_data})

    except NameError:
        print("internal error")
    except:
        print('Error returned')

def udoctor(request):

    try:
        if request.GET.get("s_id") !=None:
            s_id = request.GET.get("s_id")

            sel="select * from doctor_tb d,specialization_tb s where d.s_id = s.s_id and d.d_status='Active' and d.s_id = '"+str(s_id)+"'"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            d_data = mycursor.fetchall()

            return render(request,'udoctor.html',{'d_data':d_data})

        elif request.GET.get("search") != None:
            search = request.GET.get("search")

            sel = "select * from doctor_tb d, specialization_tb s where d.s_id = s.s_id and (d.d_name like '%" + search + "%' or s.s_name like '%" + search + "%') and d.d_status='Active'"

            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            d_data = mycursor.fetchall()


            return render(request, 'udoctor.html', {'d_data': d_data})

        else:

            sel="select * from doctor_tb d,specialization_tb s where d.s_id = s.s_id and d.d_status='Active'"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            d_data = mycursor.fetchall()

            return render(request,'udoctor.html',{'d_data':d_data})

    except NameError:
        print("internal error")
    except:
        print('Error returned')

def udocdetails(request):
    try:
        msg=""
        if request.POST:
            u_id = request.session["uid"] 
            d_id = request.GET.get("d_id")
            s_id = request.POST.get("s_id")
            a_title = request.POST.get("a_title")
            a_symptoms = request.POST.get("a_symptoms")
            a_date = request.POST.get("a_date")
            a_fees = request.POST.get("d_fees")
            a_status = 'Pending'
            cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            sel = "select * from appointment_tb where u_id ='"+str(u_id)+"' and d_id ='"+str(d_id)+"' and a_date ='"+str(a_date)+"'"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            a_data = mycursor.fetchall()

            if len(a_data)>0:
                msg = "Appointment Is Alredy Booked.!"
               
                sel = "select * from doctor_tb d, specialization_tb s where d.s_id=s.s_id and d.d_id ='"+str(d_id)+"'"
                mydb = getdb()
                mycursor = mydb.cursor(dictionary=True)
                mycursor.execute(sel)
                d_data = mycursor.fetchall()

                alldata = {
                    'd_data':d_data,
                    'msg':msg,
                }

                return render(request,'udocdetails.html',alldata)

            else:

                ins = "INSERT INTO `appointment_tb`(`u_id`, `d_id`, `s_id`, `a_title`, `a_symptoms`, `a_date`, `a_fees`,`a_status`, `a_cdate`, `a_udate`) VALUES('"+str(u_id)+"','"+str(d_id)+"','"+str(s_id)+"','"+str(a_title)+"','"+str(a_symptoms)+"','"+str(a_date)+"','"+str(a_fees)+"','"+str(a_status)+"','"+cdate+"','"+cdate+"')"
                mydb = getdb()
                mycursor = mydb.cursor(dictionary=True)
                mycursor.execute(ins)
                mydb.commit()
                return redirect("umyappointment")

        else:

            d_id = request.GET.get("d_id")

            sel = "select * from doctor_tb d, specialization_tb s where d.s_id=s.s_id and d.d_id ='"+str(d_id)+"'"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            d_data = mycursor.fetchall()

            alldata = {
                'd_data':d_data,
                'msg':msg,
            }

            return render(request,'udocdetails.html',alldata)

    except NameError:
        print("internal error")
    except:
        print('Error returned')

def uappointmentbill(request):
    try:
        u_id = request.session["uid"] 

        sel="select * from bill_tb b, user_tb u,doctor_tb d,appointment_tb a where b.u_id=u.u_id and b.d_id=d.d_id and b.b_bill_id=a.a_id and b.b_type='Appointment' and b.u_id ='"+str(u_id)+"' order by b.b_id desc"
        mydb = getdb()
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute(sel)
        a_data = mycursor.fetchall()

        return render(request,'uappointmentbill.html',{'a_data':a_data})

    except NameError:
        print("internal error")
    except:
        print('Error returned')

def utreatmentbill(request):
    try:
        u_id = request.session["uid"] 

        sel="select * from bill_tb b, user_tb u,doctor_tb d,treatment_tb t where b.u_id=u.u_id and b.d_id=d.d_id and b.b_bill_id=t.t_id and b.b_type='Treatment' and b.u_id ='"+str(u_id)+"' order by b.b_id desc"
        mydb = getdb()
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute(sel)
        t_data = mycursor.fetchall()
        
        return render(request,'utreatmentbill.html',{'t_data':t_data})

    except NameError:
        print("internal error")
    except:
        print('Error returned')

def uterms(request):
    try:

        return render(request,'uterms.html',{})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def uaboutcard(request):
    try:

        return render(request,'uaboutcard.html',{})
    except NameError:
        print("internal error")
    except:
        print('Error returned')