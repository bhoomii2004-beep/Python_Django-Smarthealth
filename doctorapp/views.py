from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
import datetime
import mysql.connector

def getdb():
    mydb = mysql.connector.connect(host="localhost",user="root", passwd="",database="health_db")
    return mydb

def dindex(request):
    try:
        d_id = request.session["did"] 
        
        pasel = "select count(a_id) from appointment_tb a,user_tb u,doctor_tb d,specialization_tb s where a.u_id = u.u_id and a.d_id = d.d_id and a.s_id = s.s_id and a.a_status = 'Pending' and a.d_id='"+str(d_id)+"' order by a.a_id desc" 
        mydb = getdb()
        mycursor = mydb.cursor()
        mycursor.execute(pasel)
        pa_data = mycursor.fetchall()

        apsel = "select count(a_id) from appointment_tb a,user_tb u,doctor_tb d,specialization_tb s where a.u_id = u.u_id and a.d_id = d.d_id and a.s_id = s.s_id and a.a_status = 'Approved' and a.d_id='"+str(d_id)+"' order by a.a_id desc" 
        mydb = getdb()
        mycursor = mydb.cursor()
        mycursor.execute(apsel)
        ap_data = mycursor.fetchall()

        casel = "select count(a_id) from appointment_tb a,user_tb u,doctor_tb d,specialization_tb s where a.u_id = u.u_id and a.d_id = d.d_id and a.s_id = s.s_id and a.a_status = 'Cancel' and a.d_id='"+str(d_id)+"' order by a.a_id desc" 
        mydb = getdb()
        mycursor = mydb.cursor()
        mycursor.execute(casel)
        ca_data = mycursor.fetchall()

        absel="select count(b_id) from bill_tb b, user_tb u,doctor_tb d,appointment_tb a where b.u_id=u.u_id and b.d_id=d.d_id and b.b_bill_id=a.a_id and b.b_type='Appointment' and b.d_id='"+str(d_id)+"' order by b.b_id desc"
        mydb = getdb()
        mycursor = mydb.cursor()
        mycursor.execute(absel)
        ab_data = mycursor.fetchall()

        tbsel="select count(b_id) from bill_tb b, user_tb u,doctor_tb d,treatment_tb t where b.u_id=u.u_id and b.d_id=d.d_id and b.b_bill_id=t.t_id and b.b_type='Treatment' and b.d_id='"+str(d_id)+"' order by b.b_id desc"
        mydb = getdb()
        mycursor = mydb.cursor()
        mycursor.execute(tbsel)
        tb_data = mycursor.fetchall()

        tsel = "select count(t_id) from treatment_tb t, appointment_tb a,user_tb u,doctor_tb d where t.a_id=a.a_id and t.u_id=u.u_id and t.d_id=d.d_id  and t.d_id='"+str(d_id)+"' order by t.t_id desc" 
        mydb = getdb()
        mycursor = mydb.cursor()
        mycursor.execute(tsel)
        t_data = mycursor.fetchall()

        ssel = "select count(s_id) from specialization_tb order by s_id desc"  
        mydb = getdb()
        mycursor = mydb.cursor()
        mycursor.execute(ssel)
        s_data = mycursor.fetchall()

        usel = "select count(u_id) from user_tb order by u_id desc"  
        mydb = getdb()
        mycursor = mydb.cursor()
        mycursor.execute(usel)
        u_data = mycursor.fetchall()

        dsel = "select count(d_id) from doctor_tb d, specialization_tb s where d.s_id=s.s_id and d.d_id != '"+str(d_id)+"' order by d.d_id desc" 
        mydb = getdb()
        mycursor = mydb.cursor()
        mycursor.execute(dsel)
        d_data = mycursor.fetchall()

        fsel = "select count(f_id) from feedback_tb order by f_id desc"  
        mydb = getdb()
        mycursor = mydb.cursor()
        mycursor.execute(fsel)
        f_data = mycursor.fetchall()

        alldata = {
            'pa_data':pa_data,
            'ap_data':ap_data,
            'ca_data':ca_data,
            'ab_data':ab_data,
            'tb_data':tb_data,
            't_data':t_data,
            's_data':s_data,
            'u_data':u_data,
            'd_data':d_data,
            'f_data':f_data
        }

        return render(request,'dindex.html',alldata)
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def dlogin(request):
    try:
        msg=""
        if request.POST:
            d_contact = request.POST.get("d_contact")
            d_password = request.POST.get("d_password")
            
            sel="select * from doctor_tb where d_contact='"+str(d_contact)+"' and d_password= '"+str(d_password)+"'"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            l_data = mycursor.fetchall()
            if len(l_data)>0:

                request.session["did"] = l_data[0]["d_id"]
                request.session["dcontact"] = d_contact
                request.session["dimg"] = l_data[0]["d_image"]
                request.session["dtime"] = str(l_data[0]["d_udate"])
                request.session["dusername"] = l_data[0]["d_name"]
                

                return redirect("dindex")
            else:
                msg="Invalid Username Or Password.!"
                return render(request,'dlogin.html',{'msg':msg})
        else:
            return render(request,'dlogin.html',{'msg':msg})

    except NameError:
        print("internal error")
    except:
        print('Error returned')

def dlogout(request):

    try:
        
        d_id = request.session["did"]
        cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        update = "update doctor_tb set d_udate = '"+cdate+"' where d_id='"+str(d_id)+"'" 
        mydb = getdb()
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute(update)
        mydb.commit()

        request.session["did"] = None
        request.session["dcontact"] = None
        request.session["dimg"] = None
        request.session["dtime"] = None
        request.session["dusername"] = None

        return redirect("dlogin")
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def dprofile(request):
    try:

        if request.POST:
            d_id = request.session["did"] 
            s_id = request.POST.get("s_id")
            d_hospitalname = request.POST.get("d_hospitalname")
            d_name = request.POST.get("d_name")
            d_contact = request.POST.get("d_contact")
            d_address = request.POST.get("d_address")
            d_gender = request.POST.get("d_gender")
            d_experience = request.POST.get("d_experience")

            if request.POST.get("d_image") !="":
                d_image = request.FILES["d_image"]
                img = FileSystemStorage()
                old_img1 = img.save(d_image.name,d_image)
            else:
                old_img1 = request.POST.get("old_img1")

            if request.POST.get("d_certificate") !="":
                d_certificate = request.FILES["d_certificate"]
                img = FileSystemStorage()
                old_img2 = img.save(d_certificate.name,d_certificate)
            else:
                old_img2 = request.POST.get("old_img2")

            d_fees = request.POST.get("d_fees")
            d_password = request.POST.get("d_password")

            cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            update = "update doctor_tb set s_id = '"+str(s_id)+"',d_hospitalname = '"+str(d_hospitalname)+"',d_name = '"+str(d_name)+"',d_address = '"+str(d_address)+"',d_gender = '"+str(d_gender)+"',d_experience = '"+str(d_experience)+"',d_image = '"+str(old_img1)+"',d_certificate = '"+str(old_img2)+"',d_fees = '"+str(d_fees)+"',d_password = '"+str(d_password)+"' , d_udate = '"+cdate+"' where d_id='"+str(d_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(update)
            mydb.commit()
            return redirect("dindex")

        else:
            
            d_id = request.session["did"] 
           
            sel = "select * from doctor_tb where d_id='"+str(d_id)+"'"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            d_data = mycursor.fetchall()

            sels = "select * from specialization_tb where s_status='Active'"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sels)
            s_data = mycursor.fetchall()
            alldata = {


            'd_data':d_data,
            's_data':s_data,
            
            }
            
            return render(request,'dprofile.html',alldata)

    except NameError:
        print("internal error")
    except:
        print('Error returned')

def duser(request):

    try:

        if request.GET.get("u_id") !=None:
            u_id = request.GET.get("u_id")

            udel = "delete from user_tb where u_id='"+str(u_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(udel)
            mydb.commit()
            return redirect("duser")

        elif request.GET.get("u_status") !=None:
            cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            u_status = request.GET.get("u_status")
            uedt = request.GET.get("uedt")

            if u_status == 'Active':
                u_status = 'Deactive'
            else:
                u_status = 'Active'

            upd = "update user_tb set u_status = '"+str(u_status)+"' , u_udate = '"+cdate+"' where u_id='"+str(uedt)+"'"
           
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(upd)
            mydb.commit()
            return redirect("duser")
        
        else:

            usel = "select * from user_tb order by u_id desc " 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(usel)
            u_data = mycursor.fetchall()

            return render(request,'duser.html',{'u_data':u_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def dfeedback(request):
    try:

        if request.GET.get("f_id") !=None:
            f_id = request.GET.get("f_id")

            fdel = "delete from feedback_tb where f_id='"+str(f_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(fdel)
            mydb.commit()
            return redirect("dfeedback")

        elif request.GET.get("f_status") !=None:
            
            f_status = request.GET.get("f_status")
            fedt = request.GET.get("fedt")

            cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if f_status == 'Show':
                f_status = 'Hide'
            else:
                f_status = 'Show'

            fupdate = "update feedback_tb set f_status = '"+str(f_status)+"' , f_udate = '"+cdate+"' where f_id='"+str(fedt)+"'"
           
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(fupdate)
            mydb.commit()
            return redirect("dfeedback")
        
        else:

            self = "select * from feedback_tb order by f_id desc " 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(self)
            f_data = mycursor.fetchall()

            return render(request,'dfeedback.html',{'f_data':f_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def ddoctor(request):
    try:

        if request.GET.get("d_id") !=None:
            d_id = request.GET.get("d_id")

            deld = "delete from doctor_tb where d_id='"+str(d_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(deld)
            mydb.commit()
            return redirect("ddoctor")

        elif request.GET.get("d_status") !=None:
            cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            d_status = request.GET.get("d_status")
            dedt = request.GET.get("dedt")

            if d_status == 'Active':
                d_status = 'Deactive'
            else:
                d_status = 'Active'

            upd = "update doctor_tb set d_status = '"+str(d_status)+"' , d_udate = '"+cdate+"' where d_id='"+str(dedt)+"'"
           
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(upd)
            mydb.commit()
            return redirect("ddoctor")
        
        else:
            d_id = request.session["did"] 
            sel = "select * from doctor_tb d, specialization_tb s where d.s_id=s.s_id and d.d_id != '"+str(d_id)+"' order by d.d_id desc " 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            d_data = mycursor.fetchall()

            return render(request,'ddoctor.html',{'d_data':d_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def dspecialization(request):
    try:

        if request.GET.get("s_id") !=None:
       
            s_id = request.GET.get("s_id")
            sdel = "delete from specialization_tb where s_id='"+str(s_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sdel)
            mydb.commit()
            return redirect("dspecialization")
        
        else:

            sel = "select * from specialization_tb order by s_id desc " 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            s_data = mycursor.fetchall()
            return render(request,'dspecialization.html',{'s_data':s_data})
    
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def dpendingappointment(request):
    try:

        if request.GET.get("a_id") !=None:
            a_id = request.GET.get("a_id")

            delp = "delete from appointment_tb where a_id='"+str(a_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(delp)
            mydb.commit()
            return redirect("dpendingappointment")

        elif request.GET.get("a_status") !=None:
            cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            a_status = request.GET.get("a_status")
            pedt = request.GET.get("pedt")

            if a_status == 'Pending':
                a_status = 'Approved'
            elif a_status == 'Approved':
                a_status = 'Cancel'   
            else:
                a_status = 'Pending'

            upd = "update appointment_tb set a_status = '"+str(a_status)+"' , a_udate = '"+cdate+"' where a_id='"+str(pedt)+"'"
           
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(upd)
            mydb.commit()
            return redirect("dpendingappointment")
        
        else:

            d_id = request.session["did"]
            sel = "select * from appointment_tb a,user_tb u,doctor_tb d,specialization_tb s where a.u_id = u.u_id and a.d_id = d.d_id and a.s_id = s.s_id and a.a_status = 'Pending' and a.d_id='"+str(d_id)+"' order by a.a_id desc" 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            p_data = mycursor.fetchall()

            return render(request,'dpendingappointment.html',{'p_data':p_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def dapprovedappointment(request):
    try:

        if request.GET.get("a_id") !=None:
            a_id = request.GET.get("a_id")

            dele = "delete from appointment_tb where a_id='"+str(a_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(dele)
            mydb.commit()
            return redirect("dapprovedappointment")

        elif request.GET.get("a_status") !=None:
            cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            a_status = request.GET.get("a_status")
            aedt = request.GET.get("aedt")

            if a_status == 'Pending':
                a_status = 'Approved'
            elif a_status == 'Approved':
                a_status = 'Cancel'   
            else:
                a_status = 'Pending'

            upd = "update appointment_tb set a_status = '"+str(a_status)+"' , a_udate = '"+cdate+"' where a_id='"+str(aedt)+"'"
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(upd)
            mydb.commit()
            return redirect("dapprovedappointment")
        
        else:
            d_id = request.session["did"]
            sel = "select * from appointment_tb a,user_tb u,doctor_tb d,specialization_tb s where a.u_id = u.u_id and a.d_id = d.d_id and a.s_id = s.s_id and a.a_status = 'Approved'and a.d_id='"+str(d_id)+"' order by a.a_id desc" 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            a_data = mycursor.fetchall()

            return render(request,'dapprovedappointment.html',{'a_data':a_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def dcancelappointment(request):
    try:

        if request.GET.get("a_id") !=None:
            a_id = request.GET.get("a_id")

            dele = "delete from appointment_tb where a_id='"+str(a_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(dele)
            mydb.commit()
            return redirect("dcancelappointment")

        elif request.GET.get("a_status") !=None:
            cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            a_status = request.GET.get("a_status")
            cedt = request.GET.get("cedt")

            if a_status == 'Pending':
                a_status = 'Approved'
            elif a_status == 'Approved':
                a_status = 'Cancel'   
            else:
                a_status = 'Pending'

            upd = "update appointment_tb set a_status = '"+str(a_status)+"' , a_udate = '"+cdate+"' where a_id='"+str(cedt)+"'"
           
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(upd)
            mydb.commit()
            return redirect("dcancelappointment")
        
        else:
            d_id = request.session["did"]
            sel = "select * from appointment_tb a,user_tb u,doctor_tb d,specialization_tb s where a.u_id = u.u_id and a.d_id = d.d_id and a.s_id = s.s_id and a.a_status = 'Cancel' and a.d_id='"+str(d_id)+"' order by a.a_id desc" 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            c_data = mycursor.fetchall()

            return render(request,'dcancelappointment.html',{'c_data':c_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def dappointmentbill(request):
    try:

        if request.GET.get("b_id") !=None:
            b_id = request.GET.get("b_id")

            dele = "delete from bill_tb where b_id='"+str(b_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(dele)
            mydb.commit()
            return redirect("dappointmentbill")

        elif request.GET.get("b_status") !=None:
            cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            b_status = request.GET.get("b_status")
            aedt = request.GET.get("aedt")

            if b_status == 'Paid':
                b_status = 'Unpaid'
            else:
                b_status = 'Paid'

            upd = "update bill_tb set b_status = '"+str(b_status)+"' , b_udate = '"+cdate+"' where b_id='"+str(aedt)+"'"
           
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(upd)
            mydb.commit()
            return redirect("dappointmentbill")
        
        else:
            d_id = request.session["did"]
            sel="select * from bill_tb b, user_tb u,doctor_tb d,appointment_tb a where b.u_id=u.u_id and b.d_id=d.d_id and b.b_bill_id=a.a_id and b.b_type='Appointment' and b.d_id='"+str(d_id)+"' order by b.b_id desc"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            a_data = mycursor.fetchall()

            return render(request,'dappointmentbill.html',{'a_data':a_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def dtreatmentbill(request):

    try:

        if request.GET.get("b_id") !=None:
            b_id = request.GET.get("b_id")

            dele = "delete from bill_tb where b_id='"+str(b_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(dele)
            mydb.commit()
            return redirect("dtreatmentbill")

        elif request.GET.get("b_status") !=None:
            cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            b_status = request.GET.get("b_status")
            tedt = request.GET.get("tedt")

            if b_status == 'Paid':
                b_status = 'Unpaid'
            else:
                b_status = 'Paid'

            upd = "update bill_tb set b_status = '"+str(b_status)+"' , b_udate = '"+cdate+"' where b_id='"+str(tedt)+"'"
           
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(upd)
            mydb.commit()
            return redirect("dtreatmentbill")
        
        else:
            d_id = request.session["did"]
            sel="select * from bill_tb b, user_tb u,doctor_tb d,treatment_tb t where b.u_id=u.u_id and b.d_id=d.d_id and b.b_bill_id=t.t_id and b.b_type='Treatment' and b.d_id='"+str(d_id)+"' order by b.b_id desc"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            t_data = mycursor.fetchall()

            return render(request,'dtreatmentbill.html',{'t_data':t_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def dtreatmentreport(request):
    try:
        if request.POST:
            start = request.POST.get("start")
            end = request.POST.get("end")
            d_id = request.session["did"]

            sel="select * from treatment_tb t, appointment_tb a,user_tb u,doctor_tb d where t.a_id=a.a_id and t.u_id=u.u_id and t.d_id=d.d_id and date(t.t_cdate) between '"+str(start)+"' and '"+str(end)+"'  and t.d_id='"+str(d_id)+"' "
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            t_data = mycursor.fetchall()
            
            return render(request,'dtreatmentreport.html',{'t_data':t_data})
        else:
             return render(request,'dtreatmentreport.html',{})
        
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def dappointmentreport(request):
    try:
        if request.POST:
            start = request.POST.get("start")
            end = request.POST.get("end")
            a_status = request.POST.get("a_status")
            d_id = request.session["did"]

            sel="select * from appointment_tb a,user_tb u,doctor_tb d,specialization_tb s where a.u_id = u.u_id and a.d_id = d.d_id and a.s_id = s.s_id and a.a_status='"+str(a_status)+"' and date(a.a_cdate) between '"+str(start)+"' and '"+str(end)+"'  and a.d_id='"+str(d_id)+"' "
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            a_data = mycursor.fetchall()
            
            return render(request,'dappointmentreport.html',{'a_data':a_data})
        else:
                return render(request,'dappointmentreport.html',{})
        
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def dappointmentbillreport(request):
    try:
        if request.POST:
            start = request.POST.get("start")
            end = request.POST.get("end")
            b_status = request.POST.get("b_status")
            d_id = request.session["did"]
            
            sel="select * from bill_tb b, user_tb u,doctor_tb d,appointment_tb a where b.u_id=u.u_id and b.d_id=d.d_id and b.b_bill_id=a.a_id and b.b_type='Appointment' and b.d_id='"+str(d_id)+"' and b.b_status='"+str(b_status)+"' and date(b.b_cdate) between '"+str(start)+"' and '"+str(end)+"' order by b.b_id desc"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            a_data = mycursor.fetchall()
            
            return render(request,'dappointmentbillreport.html',{'a_data':a_data})
        else:
                return render(request,'dappointmentbillreport.html',{})
        
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def dtreatmentbillreport(request):
    try:
        if request.POST:
            start = request.POST.get("start")
            end = request.POST.get("end")
            b_status = request.POST.get("b_status")
            d_id = request.session["did"]
            
            sel="select * from bill_tb b, user_tb u,doctor_tb d,treatment_tb t where b.u_id=u.u_id and b.d_id=d.d_id and b.b_bill_id=t.t_id and b.b_type='Treatment' and b.d_id='"+str(d_id)+"' and b.b_status='"+str(b_status)+"' and date(b.b_cdate) between '"+str(start)+"' and '"+str(end)+"' order by b.b_id desc"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            t_data = mycursor.fetchall()

            return render(request,'dtreatmentbillreport.html',{'t_data':t_data})
        else:
            return render(request,'dtreatmentbillreport.html',{})
        
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def dbillgenerate(request):
    try:
        if request.POST:

            b_type = request.POST.get("b_type")
            start = request.POST.get("start")
            end = request.POST.get("end")
            d_id = request.session["did"]
 
            if b_type == "Appointment":
                smartcard = request.POST.get("smartcard")
                
                sel = "select * from appointment_tb a,user_tb u,doctor_tb d,specialization_tb s where a.u_id = u.u_id and a.d_id = d.d_id and a.s_id = s.s_id and a.a_status = 'Approved'and a.d_id='"+str(d_id)+"' and u.u_smartcard = '"+str(smartcard)+"' and date(a.a_date) between '"+str(start)+"' and '"+str(end)+"' order by a.a_id desc" 
                mydb = getdb()
                mycursor = mydb.cursor(dictionary=True)
                mycursor.execute(sel)
                a_data = mycursor.fetchall()

                alldata = {
                    'b_type' : b_type,
                    'a_data' : a_data

                }
                return render(request,'dbillgenerate.html',alldata)

            else:
                smartcard = request.POST.get("smartcard")
                tsel = "select * from treatment_tb t, appointment_tb a,user_tb u,doctor_tb d where t.a_id=a.a_id and t.u_id=u.u_id and t.d_id=d.d_id  and t.d_id='"+str(d_id)+"' and u.u_smartcard = '"+str(smartcard)+"' and date(t.t_date) between '"+str(start)+"' and '"+str(end)+"' order by t.t_id desc " 
                mydb = getdb()
                mycursor = mydb.cursor(dictionary=True)
                mycursor.execute(tsel)
                a_data = mycursor.fetchall()

                alldata = {
                    'b_type' : b_type,
                    'a_data' : a_data

                }
                return render(request,'dbillgenerate.html',alldata)   

            
        else:
            return render(request,'dbillgenerate.html',{})
        
       
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def dtreatment(request):

    try:

        if request.GET.get("t_id") !=None:
            t_id = request.GET.get("t_id")

            dele = "delete from treatment_tb where t_id='"+str(t_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(dele)
            mydb.commit()
            return redirect("dtreatment")
        
        else:
            d_id = request.session["did"]

            sel = "select * from treatment_tb t, appointment_tb a,user_tb u,doctor_tb d where t.a_id=a.a_id and t.u_id=u.u_id and t.d_id=d.d_id  and t.d_id='"+str(d_id)+"' order by t.t_id desc " 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            t_data = mycursor.fetchall()

            return render(request,'dtreatment.html',{'t_data':t_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def daddtreatment(request):
    try:

        if request.POST:
            a_id = request.GET.get("a_id")
            u_id = request.POST.get("u_id")
            d_id = request.session["did"]
            t_title = request.POST.get("t_title")

            if request.POST.get("t_file") !="":
                t_file = request.FILES["t_file"]
                img = FileSystemStorage()
                old_img = img.save(t_file.name,t_file)
            else:
                old_img = 'nofile.png'

            t_fees = request.POST.get("t_fees")
            t_treatment = request.POST.get("t_treatment")
            t_date = request.POST.get("t_date")
            cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            ins = "INSERT INTO `treatment_tb`(`a_id`, `u_id`, `d_id`, `t_title`, `t_treatment`, `t_file`, `t_fees`, `t_date`, `t_cdate`, `t_udate`) VALUES ('"+str(a_id)+"','"+str(u_id)+"','"+str(d_id)+"','"+str(t_title)+"','"+str(t_treatment)+"','"+str(old_img)+"','"+str(t_fees)+"','"+str(t_date)+"','"+cdate+"','"+cdate+"')" 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(ins)
            mydb.commit()
            return redirect("dtreatment")

        else:
            
            a_id = request.GET.get("a_id")
            
            sel = "select * from appointment_tb a,user_tb u,doctor_tb d,specialization_tb s where a.u_id = u.u_id and a.d_id = d.d_id and a.s_id = s.s_id and a.a_id='"+str(a_id)+"'  order by a.a_id desc" 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            a_data = mycursor.fetchall()
            
            return render(request,'daddtreatment.html',{'a_data':a_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def dedittreatment(request):
    try:

        if request.POST:
            t_id = request.GET.get("t_id")
            u_id = request.POST.get("u_id")
            d_id = request.session["did"]
            t_title = request.POST.get("t_title")

            if request.POST.get("t_file") !="":
                t_file = request.FILES["t_file"]
                img = FileSystemStorage()
                old_img = img.save(t_file.name,t_file)
            else:
                old_img = request.POST.get("old_img")

            t_fees = request.POST.get("t_fees")
           
            t_treatment = request.POST.get("t_treatment")
            t_date = request.POST.get("t_date")
            cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            upd = "update treatment_tb set t_title = '"+str(t_title)+"' ,t_file = '"+str(old_img)+"' ,t_fees = '"+str(t_fees)+"' ,t_treatment = '"+str(t_treatment)+"',t_date = '"+str(t_date)+"' , t_udate = '"+cdate+"' where t_id='"+str(t_id)+"'"
        
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(upd)
            mydb.commit()
            return redirect("dtreatment")

        else:
            
            t_id = request.GET.get("t_id")
            

            sel = "select * from treatment_tb t, appointment_tb a,user_tb u,doctor_tb d where t.a_id=a.a_id and t.u_id=u.u_id and t.d_id=d.d_id  and t.t_id='"+str(t_id)+"' order by t.t_id desc " 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            a_data = mycursor.fetchall()
            
            return render(request,'dedittreatment.html',{'a_data':a_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def daddtreatmentbill(request):
    try:
        msg=""
        if request.POST:
           
            u_id = request.POST.get("u_id")
            d_id = request.session["did"]
            b_type = 'Treatment'
            t_id = request.GET.get("t_id")
            t_fees = request.POST.get("t_fees")
            u_smartcard = request.POST.get("u_smartcard")
            u_discount = request.POST.get("u_discount")
            b_total = request.POST.get("b_total")
            b_status = request.POST.get("b_status")
            cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            sel="select * from bill_tb where b_type='Treatment' and u_id='"+str(u_id)+"' and d_id='"+str(d_id)+"' and b_bill_id='"+str(t_id)+"' order by b_id desc"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            t_data = mycursor.fetchall()

            if len(t_data) > 0 : 
                msg1 = 1
                return render(request,'daddtreatmentbill.html',{'msg1':msg1})
            else:
                sel="select * from user_tb where u_id = '"+str(u_id)+"' and u_smartcard='"+str(u_smartcard)+"'"
                
                mydb = getdb()
                mycursor = mydb.cursor(dictionary=True)
                mycursor.execute(sel)
                u_data = mycursor.fetchall()

                if len(u_data) > 0:
            
                    ins = "INSERT INTO `bill_tb`(`u_id`, `d_id`, `b_type`, `b_bill_id`, `b_amount`, `u_smartcard`, `u_discount`, `b_total`, `b_status`, `b_cdate`, `b_udate`) VALUES ('"+str(u_id)+"','"+str(d_id)+"','"+str(b_type)+"','"+str(t_id)+"','"+str(t_fees)+"','"+str(u_smartcard)+"','"+str(u_discount)+"','"+str(b_total)+"','"+str(b_status)+"','"+cdate+"','"+cdate+"')" 
                    mydb = getdb()
                    mycursor = mydb.cursor(dictionary=True)
                    mycursor.execute(ins)
                    mydb.commit()
                    return redirect("dtreatmentbill")
                else:
                    msg = "Invalid Smartcard .!"

                    sel = "select * from treatment_tb t, appointment_tb a,user_tb u,doctor_tb d where t.a_id=a.a_id and t.u_id=u.u_id and t.d_id=d.d_id and t.t_id = '"+str(t_id)+"' and t.d_id='"+str(d_id)+"' order by t.t_id desc " 
                    mydb = getdb()
                    mycursor = mydb.cursor(dictionary=True)
                    mycursor.execute(sel)
                    t_data = mycursor.fetchall()

                    alldata = {
                        'msg':msg,
                        't_data':t_data
                    }
                    return render(request,'daddtreatmentbill.html',alldata)
                

        else:

            d_id = request.session["did"]
            t_id = request.GET.get("t_id")
            sel = "select * from treatment_tb t, appointment_tb a,user_tb u,doctor_tb d where t.a_id=a.a_id and t.u_id=u.u_id and t.d_id=d.d_id and t.t_id = '"+str(t_id)+"' and t.d_id='"+str(d_id)+"' order by t.t_id desc " 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            t_data = mycursor.fetchall()

            alldata = {
                'msg':msg,
                't_data':t_data
            }
            return render(request,'daddtreatmentbill.html',alldata)

    except NameError:
        print("internal error")
    except:
        print('Error returned')

def daddappointmentbill(request):
    try:
        msg=""
        if request.POST:
           
            u_id = request.POST.get("u_id")
            d_id = request.session["did"]
            b_type = 'Appointment'
            a_id = request.GET.get("a_id")
            a_fees = request.POST.get("a_fees")
            u_smartcard = request.POST.get("u_smartcard")
            
            u_discount = request.POST.get("u_discount")
            b_total = request.POST.get("b_total")
            b_status = request.POST.get("b_status")
            cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            sel="select * from bill_tb where b_type='Appointment' and u_id='"+str(u_id)+"' and d_id='"+str(d_id)+"' and b_bill_id='"+str(a_id)+"' order by b_id desc"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            a_data = mycursor.fetchall()

            if len(a_data) > 0 : 
                msg1 = 1
                return render(request,'daddappointmentbill.html',{'msg1':msg1})
            else:
                sel="select * from user_tb where u_id = '"+str(u_id)+"' and u_smartcard='"+str(u_smartcard)+"'"
                
                mydb = getdb()
                mycursor = mydb.cursor(dictionary=True)
                mycursor.execute(sel)
                u_data = mycursor.fetchall()
                

                if len(u_data) > 0:

                    ins = "INSERT INTO `bill_tb`(`u_id`, `d_id`, `b_type`, `b_bill_id`, `b_amount`, `u_smartcard`, `u_discount`, `b_total`, `b_status`, `b_cdate`, `b_udate`) VALUES ('"+str(u_id)+"','"+str(d_id)+"','"+str(b_type)+"','"+str(a_id)+"','"+str(a_fees)+"','"+str(u_smartcard)+"','"+str(u_discount)+"','"+str(b_total)+"','"+str(b_status)+"','"+cdate+"','"+cdate+"')" 
                    
                    mydb = getdb()
                    mycursor = mydb.cursor(dictionary=True)
                    mycursor.execute(ins)
                    mydb.commit()
                    return redirect("dappointmentbill")
                    
                else:
                    msg = "Invalid Smartcard .!"

                    sel = "select * from appointment_tb a,user_tb u,doctor_tb d,specialization_tb s where a.u_id = u.u_id and a.d_id = d.d_id and a.s_id = s.s_id and a.a_status = 'Approved' and a.a_id = '"+str(a_id)+"' and a.d_id='"+str(d_id)+"' order by a.a_id desc" 
                    mydb = getdb()
                    mycursor = mydb.cursor(dictionary=True)
                    mycursor.execute(sel)
                    t_data = mycursor.fetchall()

                    alldata = {
                        'msg':msg,
                        't_data':t_data
                    }
                    return render(request,'daddappointmentbill.html',alldata)
                    

        else:

            d_id = request.session["did"]
            a_id = request.GET.get("a_id")

                
            sel = "select * from appointment_tb a,user_tb u,doctor_tb d,specialization_tb s where a.u_id = u.u_id and a.d_id = d.d_id and a.s_id = s.s_id and a.a_status = 'Approved' and a.a_id = '"+str(a_id)+"' and a.d_id='"+str(d_id)+"' order by a.a_id desc" 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            t_data = mycursor.fetchall()

            alldata = {
                'msg':msg,
                't_data':t_data
            }
            return render(request,'daddappointmentbill.html',alldata)
    
    except NameError:
        print("internal error")
    except:
        print('Error returned')

