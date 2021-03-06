from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import re
from django.db.models import F
from classroom_app import models
from classroom_app.utils import *
import razorpay
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv

load_dotenv()


# Create your views here.
def loginHtml(request):
    return render(request, 'login.html', {'google_secret_key': os.getenv('google_secret')})


@csrf_exempt
def login_operation(request):
    try:
        useremail = request.POST.get('useremail')
        password = request.POST.get('password')
        u_name = re.search(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', useremail, re.I)
        if u_name:
            try:
                validate_user = models.Users.objects.get(useremail=useremail,
                                                         password=encrypt_password(password),
                                                         status__iexact='active')
                if validate_user is not None:
                    request.session['usercode'] = validate_user.user_code
                    response_msg = {"result": "success", 'u_type': validate_user.role_id.role_name,
                                    'u_code': validate_user.user_code}
                else:
                    response_msg = {"result": "failed", "msg": "Invalid User credentials"}
            except models.Users.DoesNotExist:
                response_msg = {"result": "failed", "msg": "Invalid User credentials"}
            return JsonResponse(response_msg)
        else:
            return JsonResponse({"result": "Invalid", "msg": "Invalid Username."})
    except Exception as e:
        print("Exception in login_operation views.py-->", e)
        return JsonResponse({"result": "error", "msg": "Opps!, Server error while login"})


@csrf_exempt
def google_user_login(request):
    try:
        if request.method == 'POST':
            id = request.POST['id']
            fullName = request.POST['fullName']
            givenName = request.POST['givenName']
            imgUrl = request.POST['imgUrl']
            email = request.POST['email']
            token = request.POST['id_token']
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), os.getenv('google_secret'))
            print('idinfo -->', idinfo)
            check_email_exist = models.Users.objects.filter(useremail=email).exists()
            if check_email_exist is False:
                u_code = getUniqueUserCode()
                models.Student.objects.create(usercode=u_code, student_name=fullName,
                                              student_email=email)

                models.Users.objects.create(user_code=u_code, name=fullName, useremail=email,
                                            role_id=models.Role.objects.get(role_name='Student'))
                validate_user = models.Users.objects.get(useremail=email,
                                                         status__iexact='active')
                request.session['usercode'] = validate_user.user_code
                response_msg = {"result": "success", 'u_type': validate_user.role_id.role_name,
                                'u_code': validate_user.user_code}
                return JsonResponse(response_msg)

            else:
                validate_user = models.Users.objects.get(useremail=email,
                                                         status__iexact='active')
                request.session['usercode'] = validate_user.user_code
                response_msg = {"result": "success", 'u_type': validate_user.role_id.role_name,
                                'u_code': validate_user.user_code}
                return JsonResponse(response_msg)
    except Exception as e:
        print('Exception in google_login function -->', e)


def logout(request):
    try:
        # Remove the authenticated user's ID from the request and flush their session data.Add details to UserLogs table.
        if 'usercode' in request.session:
            user_code = request.session['usercode']
            print('LOGOUT - ---- > ', user_code)
            request.session.flush()
        return HttpResponseRedirect('/')
    except Exception as e:
        print('Exception in logout --> ', e)
        request.session.flush()
        return HttpResponseRedirect('/')


def admin_dashboard(request):
    try:
        if 'usercode' in request.session:
            user_code = request.session['usercode']
            user_details = list(
                models.Users.objects.filter(user_code=user_code).values('name', 'useremail'))
            return render(request, 'admin_dashboard.html',
                          {'user_code': user_code, 'details': user_details, 'type': 'ADMIN'})
    except Exception as e:
        print('Exception in rendering admin_dashboard --> ', e)
        request.session.flush()
        return HttpResponseRedirect('/')


def teacher_dashboard(request):
    try:
        if 'usercode' in request.session:
            user_code = request.session['usercode']
            user_details = list(
                models.Users.objects.filter(user_code=user_code).values('name', 'useremail'))
            return render(request, 'teacher_dashboard.html',
                          {'user_code': user_code, 'details': user_details, 'type': 'TEACHER'})
    except Exception as e:
        print('Exception in rendering teacher_dashboard --> ', e)
        request.session.flush()
        return HttpResponseRedirect('/')


def payment_page(request):
    try:
        if 'usercode' in request.session:
            user_code = request.session['usercode']
            user_details = list(
                models.Users.objects.filter(user_code=user_code).values('name', 'useremail'))
            return render(request, 'payment.html',
                          {'user_code': user_code, 'details': user_details, 'type': 'TEACHER'})
    except Exception as e:
        print('Exception in rendering payment page --> ', e)
        request.session.flush()
        return HttpResponseRedirect('/')


def student_dashboard(request):
    try:
        if 'usercode' in request.session:
            user_code = request.session['usercode']
            user_details = list(
                models.Users.objects.filter(user_code=user_code).values('name', 'useremail'))
            return render(request, 'student_dashboard.html',
                          {'user_code': user_code, 'details': user_details, 'type': 'STUDENT'})
    except Exception as e:
        print('Exception in rendering admin_dashboard --> ', e)
        request.session.flush()
        return HttpResponseRedirect('/')


@csrf_exempt
def register_new_user(request):
    try:
        if request.method == 'POST':
            user_type = request.POST['type']
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']

            if user_type != '' and name != '' and email != '' and password != '':
                check_email_exist = models.Users.objects.filter(useremail=email).exists()
                if check_email_exist is False:
                    u_code = getUniqueUserCode()
                    if user_type == 'Teacher':
                        save_details = models.Teacher.objects.create(usercode=u_code, teacher_name=name,
                                                                     teacher_email=email)
                    else:
                        save_details = models.Student.objects.create(usercode=u_code, student_name=name,
                                                                     student_email=email)
                    if save_details is not None:
                        try:
                            models.Users.objects.create(user_code=u_code, name=name, useremail=email,
                                                        password=encrypt_password(password),
                                                        role_id=models.Role.objects.get(role_name=user_type))
                            try:
                                send_manually_email(subject='Registration Successfull',
                                                    message="Dear User,\n\n"
                                                            "Please note your email id and password to access your account.\n"
                                                            "Email-id: " + email + "\n"
                                                                                   "Password: " + password + ""
                                                    , to=email)
                            except Exception as e:
                                print('Exception in send email', e)
                                pass
                            return JsonResponse({'result': 'success', 'msg': 'Registered Successfully'})
                        except Exception as e:
                            models.Teacher.objects.filter(usercode=u_code).delete()
                            models.Student.objects.filter(usercode=u_code).delete()
                            print("Exception in user creation -->", e)
                else:
                    return JsonResponse(
                        {'result': 'email_exist', 'msg': 'This email id already registered! Try with another'})
            else:
                return JsonResponse({'result': 'invalid_request', 'msg': 'Invalid request! Try again'})

    except Exception as e:
        print("Exception in register_new_user views.py-->", e)
        return JsonResponse({'result': 'failed', 'msg': 'Failed to register! Try after sometimes'})


@csrf_exempt
def save_class_details(request):
    try:
        if 'usercode' in request.session:
            usercode = request.session['usercode']
            if request.method == 'POST':
                className = request.POST['className']
                classSubject = request.POST['classSubject']
                classDate = request.POST['classDate']
                classTime = request.POST['classTime']

                if className != '' and classSubject != '' and classDate != '' and classTime != '':
                    models.Classes.objects.create(class_name=className, class_subject=classSubject,
                                                  class_date=classDate, class_time=classTime,
                                                  teacher_id=models.Teacher.objects.get(usercode=usercode))
                    return JsonResponse({'result': 'success', 'msg': 'Class Created Successfully'})
                else:
                    return JsonResponse({'result': 'invalid_request', 'msg': 'Invalid request! Try again'})
    except Exception as e:
        print("Exception in save_class_details views.py-->", e)
        return JsonResponse({'result': 'failed', 'msg': 'Failed to save class details! Try after sometimes'})


@csrf_exempt
def fetch_class_details(request):
    try:
        if 'usercode' in request.session:
            usercode = request.session['usercode']
            if request.method == 'POST':
                teacher_obj = models.Teacher.objects.get(usercode=usercode)
                cls_details = list(
                    models.Classes.objects.values('class_name', 'class_subject', 'class_date', 'class_time',
                                                  'number_of_students').filter(teacher_id=teacher_obj.teacher_id))
                return JsonResponse({'result': 'success', 'cls_details': cls_details})
    except Exception as e:
        print("Exception in fetch_class_details views.py-->", e)
        return JsonResponse({'result': 'failed', 'msg': 'Failed to load class details! Refresh the page'})


@csrf_exempt
def fetch_all_class_details(request):
    try:
        if 'usercode' in request.session:
            if request.method == 'POST':
                cls_details = list(
                    models.Classes.objects.values('class_name', 'class_subject', 'class_date', 'class_time', 'class_id',
                                                  'number_of_students').filter(class_subject='Mathematics'))
                return JsonResponse({'result': 'success', 'cls_details': cls_details})
    except Exception as e:
        print("Exception in fetch_all_class_details views.py-->", e)
        return JsonResponse({'result': 'failed', 'msg': 'Failed to load class details! Refresh the page'})


@csrf_exempt
def enroll_class(request):
    try:
        if 'usercode' in request.session:
            usercode = request.session['usercode']
            if request.method == 'POST':
                clsId = request.POST['clsId']
                models.ClassStudentMapping.objects.create(class_id=models.Classes.objects.get(class_id=clsId),
                                                          student_id=models.Student.objects.get(usercode=usercode))
                models.Classes.objects.filter(class_id=clsId).update(
                    number_of_students=F('number_of_students') + 1)
                return JsonResponse({'result': 'success'})
    except Exception as e:
        print("Exception in fetch_all_class_details views.py-->", e)
        return JsonResponse({'result': 'failed', 'msg': 'Failed to enroll for class! Refresh the page'})


@csrf_exempt
def fetch_my_enrolled_classes(request):
    try:
        if 'usercode' in request.session:
            usercode = request.session['usercode']
            if request.method == 'POST':
                student_obj = models.Student.objects.get(usercode=usercode)
                fetch_enrolled_cls_list = list(
                    models.ClassStudentMapping.objects.values_list('class_id', flat=True).filter(
                        student_id=student_obj.student_id))
                cls_details = list(
                    models.Classes.objects.values('class_name', 'class_subject', 'class_date', 'class_time', 'class_id',
                                                  'number_of_students').filter(class_id__in=fetch_enrolled_cls_list))
                return JsonResponse({'result': 'success', 'cls_details': cls_details})
    except Exception as e:
        print("Exception in fetch_all_class_details views.py-->", e)
        return JsonResponse({'result': 'failed', 'msg': 'Failed to load class details! Refresh the page'})


@csrf_exempt
def generate_payment_order(request):
    try:
        if request.method == 'POST':
            itemName = request.POST['itemName']
            itemPrice = request.POST['itemPrice']
            client = razorpay.Client(auth=(os.getenv('razorpay_publickey'), os.getenv('razorpay_secretkey')))
            myorder = client.order.create(
                {'amount': int(itemPrice) * 100, 'currency': 'INR', 'payment_capture': '1'})
            models.Transactions.objects.create(name=itemName, amount=itemPrice, order_id=myorder['id'])
            return JsonResponse({'my_payment': myorder, 'amount': itemPrice, 'itemName': itemName})
    except Exception as e:
        print("Exception in generate_payment_order views.py-->", e)
        return JsonResponse({'result': 'failed', 'msg': 'Internal server error'})


@csrf_exempt
def update_transaction_db(request):
    if request.method == 'POST':
        razorpay_payment_id = request.POST['razorpay_payment_id']
        razorpay_order_id = request.POST['razorpay_order_id']
        razorpay_signature = request.POST['razorpay_signature']

        models.Transactions.objects.filter(order_id=razorpay_order_id).update(order_id=razorpay_order_id,
                                                                              payment_id=razorpay_payment_id,
                                                                              signature=razorpay_signature, paid=True)

        return JsonResponse({'result': 'success'})
