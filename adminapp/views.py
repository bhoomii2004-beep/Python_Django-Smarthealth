from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
import datetime
import mysql.connector

def getdb():
    mydb = mysql.connector.connect(host="localhost",user="root", passwd="",database="health_db")
    return mydb

def index(request):
    try:
        pasel = "select count(a_id) from appointment_tb a,user_tb u,doctor_tb d,specialization_tb s where a.u_id = u.u_id and a.d_id = d.d_id and a.s_id = s.s_id and a.a_status = 'Pending' order by a.a_id desc" 
        mydb = getdb()
        mycursor = mydb.cursor()
        mycursor.execute(pasel)
        pa_data = mycursor.fetchall()

        apsel = "select count(a_id) from appointment_tb a,user_tb u,doctor_tb d,specialization_tb s where a.u_id = u.u_id and a.d_id = d.d_id and a.s_id = s.s_id and a.a_status = 'Approved' order by a.a_id desc" 
        mydb = getdb()
        mycursor = mydb.cursor()
        mycursor.execute(apsel)
        ap_data = mycursor.fetchall()

        casel = "select count(a_id) from appointment_tb a,user_tb u,doctor_tb d,specialization_tb s where a.u_id = u.u_id and a.d_id = d.d_id and a.s_id = s.s_id and a.a_status = 'Cancel' order by a.a_id desc" 
        mydb = getdb()
        mycursor = mydb.cursor()
        mycursor.execute(casel)
        ca_data = mycursor.fetchall()

        absel="select count(b_id) from bill_tb b, user_tb u,doctor_tb d,appointment_tb a where b.u_id=u.u_id and b.d_id=d.d_id and b.b_bill_id=a.a_id and b.b_type='Appointment' order by b.b_id desc"
        mydb = getdb()
        mycursor = mydb.cursor()
        mycursor.execute(absel)
        ab_data = mycursor.fetchall()

        tbsel="select count(b_id) from bill_tb b, user_tb u,doctor_tb d,treatment_tb t where b.u_id=u.u_id and b.d_id=d.d_id and b.b_bill_id=t.t_id and b.b_type='Treatment' order by b.b_id desc"
        mydb = getdb()
        mycursor = mydb.cursor()
        mycursor.execute(tbsel)
        tb_data = mycursor.fetchall()

        tsel = "select count(t_id) from treatment_tb t, appointment_tb a,user_tb u,doctor_tb d where t.a_id=a.a_id and t.u_id=u.u_id and t.d_id=d.d_id order by t.t_id desc " 
        mydb = getdb()
        mycursor = mydb.cursor()
        mycursor.execute(tsel)
        t_data = mycursor.fetchall()

        ssel = "select count(s_id) from specialization_tb order by s_id desc " 
        mydb = getdb()
        mycursor = mydb.cursor()
        mycursor.execute(ssel)
        s_data = mycursor.fetchall()

        usel = "select count(u_id) from user_tb order by u_id desc " 
        mydb = getdb()
        mycursor = mydb.cursor()
        mycursor.execute(usel)
        u_data = mycursor.fetchall()

        dsel = "select count(d_id) from doctor_tb d, specialization_tb s where d.s_id=s.s_id order by d.d_id desc " 
        mydb = getdb()
        mycursor = mydb.cursor()
        mycursor.execute(dsel)
        d_data = mycursor.fetchall()

        fsel = "select count(f_id) from feedback_tb order by f_id desc " 
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

        return render(request,'index.html',alldata)
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def specialization(request):
    try:
        if request.POST:
            s_name = request.POST.get("s_name")

            s_image = request.FILES["s_image"]
            img = FileSystemStorage()
            s_image = img.save(s_image.name,s_image)

            s_status = request.POST.get("s_status")
            cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            ins = "INSERT INTO `specialization_tb`(`s_name`, `s_image`, `s_status`, `s_cdate`, `s_udate`) VALUES ('"+str(s_name)+"','"+str(s_image)+"','"+str(s_status)+"','"+cdate+"','"+cdate+"')" 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(ins)
            mydb.commit()
            return redirect("specialization")

        elif request.GET.get("s_id") !=None:
       
            s_id = request.GET.get("s_id")
            sdel = "delete from specialization_tb where s_id='"+str(s_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sdel)
            mydb.commit()
            return redirect("specialization")
        
        else:

            sel = "select * from specialization_tb order by s_id desc " 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            s_data = mycursor.fetchall()
            return render(request,'specialization.html',{'s_data':s_data})
    
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def specializationedit(request):
    try:

        if request.POST:
            s_id = request.GET.get("s_id")
            s_name = request.POST.get("s_name")

            if request.POST.get("s_image") !="":
                s_image = request.FILES["s_image"]
                img = FileSystemStorage()
                old_img = img.save(s_image.name,s_image)
            else:
                old_img = request.POST.get("old_img")

            s_status = request.POST.get("s_status")
            cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            update = "update specialization_tb set s_name = '"+str(s_name)+"',s_image = '"+str(old_img)+"',s_status = '"+str(s_status)+"' , s_udate = '"+cdate+"' where s_id='"+str(s_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(update)
            mydb.commit()
            return redirect("specialization")

        else:
            
            s_id = request.GET.get("s_id")
           
            sel = "select * from specialization_tb where s_id='"+str(s_id)+"'"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            s_data = mycursor.fetchall()
            
            return render(request,'specializationedit.html',{'s_data':s_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def feedback(request):
    try:

        if request.GET.get("f_id") !=None:
            f_id = request.GET.get("f_id")

            fdel = "delete from feedback_tb where f_id='"+str(f_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(fdel)
            mydb.commit()
            return redirect("feedback")

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
            return redirect("feedback")
        
        else:

            self = "select * from feedback_tb order by f_id desc " 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(self)
            f_data = mycursor.fetchall()

            return render(request,'feedback.html',{'f_data':f_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def user(request):
    try:

        if request.GET.get("u_id") !=None:
            u_id = request.GET.get("u_id")

            udel = "delete from user_tb where u_id='"+str(u_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(udel)
            mydb.commit()
            return redirect("user")

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
            return redirect("user")
        
        else:

            usel = "select * from user_tb order by u_id desc " 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(usel)
            u_data = mycursor.fetchall()

            return render(request,'user.html',{'u_data':u_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def userdetails(request):
    try:
        msg = ""
        if request.POST:
            
            u_smartcard = request.POST.get("u_smartcard")
            operation = request.POST.get("operation")
            
            if operation == "Generate":
                
                sel = "select * from user_tb where u_smartcard = '"+str(u_smartcard)+"'"
           
                mydb = getdb()
                mycursor = mydb.cursor(dictionary=True)
                mycursor.execute(sel)
                u_data = mycursor.fetchall()
            
                if len(u_data) > 0:

                    msg = "Already exists this RFID Card..!"
                    
                    u_id = request.GET.get("u_id")

                    sel = "select * from user_tb where u_id='"+str(u_id)+"'"
                    mydb = getdb()
                    mycursor = mydb.cursor(dictionary=True)
                    mycursor.execute(sel)
                    u_data = mycursor.fetchall()

                    alldata = {

                        'u_data':u_data,
                        'msg' : msg

                    }
                
                    return render(request,'userdetails.html',alldata)

                else:
                    u_id = request.GET.get("u_id")
                    u_status = request.POST.get("u_status")
                    u_discount = request.POST.get("u_discount")
                    cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    update = "update user_tb set u_status = '"+str(u_status)+"',u_discount = '"+str(u_discount)+"',u_smartcard = '"+str(u_smartcard)+"' , u_udate = '"+cdate+"' where u_id='"+str(u_id)+"'" 
                    mydb = getdb()
                    mycursor = mydb.cursor(dictionary=True)
                    mycursor.execute(update)
                    mydb.commit()
                    return redirect("user")

            else:
                
                u_id = request.GET.get("u_id")
                u_status = request.POST.get("u_status")
                u_discount = request.POST.get("u_discount")
                cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                update = "update user_tb set u_status = '"+str(u_status)+"',u_discount = '"+str(u_discount)+"',u_smartcard = '"+str(u_smartcard)+"' , u_udate = '"+cdate+"' where u_id='"+str(u_id)+"'" 
                mydb = getdb()
                mycursor = mydb.cursor(dictionary=True)
                mycursor.execute(update)
                mydb.commit()
                return redirect("user")


                    
        else:
            
            u_id = request.GET.get("u_id")
           
            sel = "select * from user_tb where u_id='"+str(u_id)+"'"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            u_data = mycursor.fetchall()

            alldata = {

                'u_data':u_data,
                'msg' : msg

            }
            
            return render(request,'userdetails.html',alldata)
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def doctor(request):
    try:

        if request.GET.get("d_id") !=None:
            d_id = request.GET.get("d_id")

            deld = "delete from doctor_tb where d_id='"+str(d_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(deld)
            mydb.commit()
            return redirect("doctor")

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
            return redirect("doctor")
        
        else:

            sel = "select * from doctor_tb d, specialization_tb s where d.s_id=s.s_id order by d.d_id desc " 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            d_data = mycursor.fetchall()

            return render(request,'doctor.html',{'d_data':d_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def pendingappointment(request):
    try:

        if request.GET.get("a_id") !=None:
            a_id = request.GET.get("a_id")

            delp = "delete from appointment_tb where a_id='"+str(a_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(delp)
            mydb.commit()
            return redirect("pendingappointment")

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
            return redirect("pendingappointment")
        
        else:

            sel = "select * from appointment_tb a,user_tb u,doctor_tb d,specialization_tb s where a.u_id = u.u_id and a.d_id = d.d_id and a.s_id = s.s_id and a.a_status = 'Pending' order by a.a_id desc" 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            p_data = mycursor.fetchall()

            return render(request,'pendingappointment.html',{'p_data':p_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def approvedappointment(request):
    try:

        if request.GET.get("a_id") !=None:
            a_id = request.GET.get("a_id")

            dele = "delete from appointment_tb where a_id='"+str(a_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(dele)
            mydb.commit()
            return redirect("approvedappointment")

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
            print(upd)
           
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(upd)
            mydb.commit()
            return redirect("approvedappointment")
        
        else:

            sel = "select * from appointment_tb a,user_tb u,doctor_tb d,specialization_tb s where a.u_id = u.u_id and a.d_id = d.d_id and a.s_id = s.s_id and a.a_status = 'Approved' order by a.a_id desc" 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            a_data = mycursor.fetchall()

            return render(request,'approvedappointment.html',{'a_data':a_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def cancelappointment(request):
    try:

        if request.GET.get("a_id") !=None:
            a_id = request.GET.get("a_id")

            dele = "delete from appointment_tb where a_id='"+str(a_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(dele)
            mydb.commit()
            return redirect("cancelappointment")

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
            return redirect("cancelappointment")
        
        else:

            sel = "select * from appointment_tb a,user_tb u,doctor_tb d,specialization_tb s where a.u_id = u.u_id and a.d_id = d.d_id and a.s_id = s.s_id and a.a_status = 'Cancel' order by a.a_id desc" 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            c_data = mycursor.fetchall()

            return render(request,'cancelappointment.html',{'c_data':c_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def treatment(request):
    try:

        if request.GET.get("t_id") !=None:
            t_id = request.GET.get("t_id")

            dele = "delete from treatment_tb where t_id='"+str(t_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(dele)
            mydb.commit()
            return redirect("treatment")
        
        else:

            sel = "select * from treatment_tb t, appointment_tb a,user_tb u,doctor_tb d where t.a_id=a.a_id and t.u_id=u.u_id and t.d_id=d.d_id order by t.t_id desc " 
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            t_data = mycursor.fetchall()

            return render(request,'treatment.html',{'t_data':t_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def treatmentbill(request):
    try:

        if request.GET.get("b_id") !=None:
            b_id = request.GET.get("b_id")

            dele = "delete from bill_tb where b_id='"+str(b_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(dele)
            mydb.commit()
            return redirect("treatmentbill")

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
            return redirect("treatmentbill")
        
        else:

            sel="select * from bill_tb b, user_tb u,doctor_tb d,treatment_tb t where b.u_id=u.u_id and b.d_id=d.d_id and b.b_bill_id=t.t_id and b.b_type='Treatment' order by b.b_id desc"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            t_data = mycursor.fetchall()

            return render(request,'treatmentbill.html',{'t_data':t_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def appointmentbill(request):
    try:

        if request.GET.get("b_id") !=None:
            b_id = request.GET.get("b_id")

            dele = "delete from bill_tb where b_id='"+str(b_id)+"'" 
            mydb = getdb()
            mycursor = mydb.cursor()
            mycursor.execute(dele)
            mydb.commit()
            return redirect("appointmentbill")

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
            return redirect("appointmentbill")
        
        else:

            sel="select * from bill_tb b, user_tb u,doctor_tb d,appointment_tb a where b.u_id=u.u_id and b.d_id=d.d_id and b.b_bill_id=a.a_id and b.b_type='Appointment' order by b.b_id desc"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            a_data = mycursor.fetchall()

            return render(request,'appointmentbill.html',{'a_data':a_data})
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def login(request):
    try:
        msg=""
        if request.POST:
            l_username = request.POST.get("l_username")
            l_password = request.POST.get("l_password")
            
            sel="select * from login_tb where l_username='"+str(l_username)+"' and l_password= '"+str(l_password)+"'"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            l_data = mycursor.fetchall()
            if len(l_data)>0:

                request.session["id"] = l_data[0]["l_id"]
                request.session["username"] = l_username
                request.session["img"] = l_data[0]["l_image"]
                print(l_data[0]["l_image"])
                request.session["time"] = str(l_data[0]["l_lastseen"])

                return redirect("index")
            else:
                msg="Invalid Username Or Password.!"
                return render(request,'login.html',{'msg':msg})
        else:
            return render(request,'login.html',{'msg':msg})

    except NameError:
        print("internal error")
    except:
        print('Error returned')

def logout(request):

    try:
        
        l_id = request.session["id"]
        cdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        update = "update login_tb set l_lastseen = '"+cdate+"' where l_id='"+str(l_id)+"'" 
        print(update)
        mydb = getdb()
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute(update)
        mydb.commit()

        request.session["id"] = None
        request.session["username"] = None
        request.session["img"] = None
        request.session["time"] = None

        return redirect("login")
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def appointmentreport(request):
    try:
        if request.POST:
            start = request.POST.get("start")
            end = request.POST.get("end")
            a_status = request.POST.get("a_status")

            sel="select * from appointment_tb a,user_tb u,doctor_tb d,specialization_tb s where a.u_id = u.u_id and a.d_id = d.d_id and a.s_id = s.s_id and a.a_status='"+str(a_status)+"' and date(a.a_cdate) between '"+str(start)+"' and '"+str(end)+"' "
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            a_data = mycursor.fetchall()
            
            return render(request,'appointmentreport.html',{'a_data':a_data})
        else:
             return render(request,'appointmentreport.html',{})
        
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def treatmentreport(request):
    try:
        if request.POST:
            start = request.POST.get("start")
            end = request.POST.get("end")
            

            sel="select * from treatment_tb t, appointment_tb a,user_tb u,doctor_tb d where t.a_id=a.a_id and t.u_id=u.u_id and t.d_id=d.d_id and date(t.t_cdate) between '"+str(start)+"' and '"+str(end)+"' "
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            t_data = mycursor.fetchall()
            
            return render(request,'treatmentreport.html',{'t_data':t_data})
        else:
             return render(request,'treatmentreport.html',{})
        
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def appointmentbillreport(request):
    try:
        if request.POST:
            start = request.POST.get("start")
            end = request.POST.get("end")
            b_status = request.POST.get("b_status")
            
            sel="select * from bill_tb b, user_tb u,doctor_tb d,appointment_tb a where b.u_id=u.u_id and b.d_id=d.d_id and b.b_bill_id=a.a_id and b.b_type='Appointment' and b.b_status='"+str(b_status)+"' and date(b.b_cdate) between '"+str(start)+"' and '"+str(end)+"' order by b.b_id desc"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            a_data = mycursor.fetchall()
            
            return render(request,'appointmentbillreport.html',{'a_data':a_data})
        else:
                return render(request,'appointmentbillreport.html',{})
        
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def treatmentbillreport(request):
    try:
        if request.POST:
            start = request.POST.get("start")
            end = request.POST.get("end")
            b_status = request.POST.get("b_status")
            
            sel="select * from bill_tb b, user_tb u,doctor_tb d,treatment_tb t where b.u_id=u.u_id and b.d_id=d.d_id and b.b_bill_id=t.t_id and b.b_type='Treatment' and b.b_status='"+str(b_status)+"' and date(b.b_cdate) between '"+str(start)+"' and '"+str(end)+"' order by b.b_id desc"
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(sel)
            t_data = mycursor.fetchall()

            return render(request,'treatmentbillreport.html',{'t_data':t_data})
        else:
            return render(request,'treatmentbillreport.html',{})
        
    except NameError:
        print("internal error")
    except:
        print('Error returned')

def changepassword(request):
    try:
        msg = ""
        if request.POST:

            l_id = request.session["id"]
            currentpassword = request.POST.get("currentpassword")
            newpassword = request.POST.get("newpassword")
            confirmpassword = request.POST.get("confirmpassword")
            
            selchangepassword = "select * from login_tb  where l_id = '"+str(l_id)+"'"
            # connection create object
            mydb = getdb()
            mycursor = mydb.cursor(dictionary=True)
            #query execute
            mycursor.execute(selchangepassword)
            l_data = mycursor.fetchall()

            cpassword = l_data[0]["l_password"]

            if cpassword == currentpassword:

                if newpassword == confirmpassword : 

                    update = "update login_tb set l_password = '"+str(confirmpassword)+"'  where l_id='"+str(l_id)+"'" 
                    mydb = getdb()
                    mycursor = mydb.cursor(dictionary=True)
                    mycursor.execute(update)
                    mydb.commit()

                    return redirect("index")

                else:
                    msg = "New And Confirm Password Doesn't Match.!"
                    return render(request,'changepassword.html',{'msg': msg})
        
            else:
                msg = "Invalid Current Password.!"
                return render(request,'changepassword.html',{'msg': msg})

        else:
            return render(request,'changepassword.html',{'msg': msg})

    except NameError:
        print("internal error")
    except:
        print('Error returned')


