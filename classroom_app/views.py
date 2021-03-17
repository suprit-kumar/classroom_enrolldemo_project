from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import re

from classroom_app import models
from classroom_app.utils import *


# Create your views here.
def loginHtml(request):
    return render(request, 'login.html')


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
        print('Exception in rendering admin_dashboard --> ', e)
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
