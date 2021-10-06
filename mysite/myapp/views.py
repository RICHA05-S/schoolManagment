from django.shortcuts import render,redirect
from django.views.generic.edit import View
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Profile
from django.contrib.auth.models import auth,User
from .forms import UpdateForm,SubjectUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import  *
from django.db.models import Avg,Min,Max
from django.db.models import Q
from django.template.loader import get_template
from xhtml2pdf import pisa
import pdfkit
import os
from django.template.loader import render_to_string
import mimetypes
from django.conf import settings
import uuid

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# Create your views here.

class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, 'home.html')
    def post(self, request):
        return render(request, 'home.html')


class AboutUsView(View):
    template_name = 'aboutus.html'

    def get(self, request):
        return render(request, 'aboutus.html')
    def post(self, request):
        return render(request, 'aboutus.html')

class SignupView(View):
    template_name = 'signup.html'

    def get(self,request):
        return render(request,'registeration/signup.html')

    def post(self, request):
        data = request.POST
        if User.objects.filter(username=data['username']).exists():
            return render(request, 'signup.html')
        if User.objects.filter(email=data['email']).exists():
            msg = 'email already exist'
            return render(request, 'signup.html', {'msg': msg})
        user_obj = User(username=data['username'], email=data['email'],
                            first_name=data['first_name'], last_name=data['last_name'])
        user_obj.set_password(data['password'])
        user_obj.save()
        profile_obj = Profile(user=user_obj, phone_number=data['phone_number'], user_type=data['usertype'])
        profile_obj.save()
        return redirect('myapp:login')


class LoginView(View):
    template_name = 'registeration/login.html'

    def get(self,request):
        return render(request,'registeration/login.html')

    def post(self, request):
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        try:
            user_obj = User.objects.get(username = username)
        except ObjectDoesNotExist :
            messages.info(request, 'account not exit plz sign in')
            redirect('myapp:login')

        if user is not None:
            auth.login(request, user)
            type_obj =Profile.objects.get(user=user_obj).user_type
            if user.is_authenticated and type_obj=="Admin" :
                return redirect('myapp:user_profile')
            elif user.is_authenticated and type_obj=="Teacher":
                return redirect('myapp:teacher_profile')
            if user.is_authenticated and type_obj=="Student":
                return HttpResponseRedirect(f'/student_report_cart/{user.id}')
        else:
            messages.info(request, 'account not exit plz sign in')

        form = AuthenticationForm()
        return render(request, 'registeration/login.html', {'form': form})


class PasswordResetView(View):

    def get(self, request):
        return render(request, 'registeration/password_reset.html')

    def post(self, request):
        data = request.POST
        if User.objects.filter(email=data['email']).exists():
            auth_token = str(uuid.uuid4())
            try:
                reset_password_obj =  Resetpassword(user = User.objects.get(email=data['email']),token=auth_token ,)
                reset_password_obj.save()
            except:
                msg = "Email already sent.Please try again."
                res = Resetpassword.objects.get(user__email=data['email'] )
                res.delete()
                print(msg)
                return redirect('myapp:password_reset_done')
            link = f"http://127.0.0.1:8000/password_reset_confirm/{auth_token}"
            subject = 'Reset Password'
            html_message = render_to_string('registeration/password_reset_email.html',
                                            {"user": User.objects.get(email=data['email']).username,"link":link})
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to = data['email']

            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
            print("New email sent")
            return redirect('myapp:password_reset_done')
        print("email not found")
        return render(request,'registeration/password_reset.html')

class PasswordResetDoneView(View):
    def get(self, request):
        return render(request, 'registeration/password_reset_done.html')

    def post(self, request):

        return render(request, 'registeration/password_reset_done.html')


class PasswordResetConfirmView(View):


    def get(self, request,token):
        try:
            reset_password_obj = Resetpassword.objects.get(token=token)
        except:
            msg = "Token  not found "
            return redirect('myapp:password_reset')


        return render(request, 'registeration/password_reset_confirm.html',{'token':token})

    def post(self, request,token):
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            res = Resetpassword.objects.get(token = token)
            print(res)
            user_obj = User.objects.get(email=res.user.email)
            user_obj.set_password(password)
            user_obj.save()
            res.delete()
        else:
            return render(request, 'registeration/password_reset_confirm.html')

        return redirect('myapp:login')


class AdminProfileView(View):
    template_name = 'admin_profile.html'

    def get(self, request):
        user = Profile.objects.get(user=request.user)
        context = {
            'user_type': user.user_type,
            'teacher_profile': User.objects.filter(Q(profile__user_type='Teacher')
                                                   )}
        return render(request, 'teacherprofile.html', {'context': context})

    def post(self,request):
        return render(request, 'teacherprofile.html')

class AdminProfileUpdateView(View):
    def get(self, request, id):
        update = User.objects.get(pk=id)
        return render(request, 'admin_profile_update.html', {'user': update})

    def post(self, request, id):
        update = User.objects.get(pk=id)
        upt_form = UpdateForm(request.POST or None, instance=update)
        if upt_form.is_valid():
            upt_form.save()
            return redirect('myapp:admin_profile')
        return render(request, 'admin_profile_update.html', {'upt_form': upt_form, 'user': update})


class ProfileView(View):
    template_name = 'user_profile.html'

    def get(self,request):
        try:
            user = Profile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            print('user does not exist')
        print(user.user_type)
        context = {
            'user_type': user.user_type ,
            'user_profile':User.objects.all()
         }
        # create an paginator object from the same
        # per page two records will be displayed and last page may have 3 entries to avoid additional page
        emp_page_wise = Paginator(context['user_profile'],per_page=3, orphans=1)
        # get the current page number
        current = request.GET.get('page')
        emp_list = emp_page_wise.get_page(current)
        # emp_list is an object of Page class
        return render(request,'user_profile.html',{'page_obj': emp_list,'user_type':context['user_type']})

    def post(self,request):
        return render(request,'user_profile.html')


class ProfileUpdateView(View):

    def get(self,request,id):
        update = User.objects.get(pk=id)
        return render(request,'user_update.html',{'user':update})

    def post(self,request,id):
        update=User.objects.get(pk=id)
        upt_form=UpdateForm(request.POST or None,instance=update)
        if upt_form.is_valid():
            upt_form.save()
            return redirect('myapp:user_profile')
        return render(request, 'user_update.html', {'upt_form': upt_form,'user':update})



class ProfileAddView(View):


    def get(self, request):
        ctx = {'user_type':request.user.profile.user_type}
        print(ctx)
        return render(request,'user_add.html',ctx)


    def post(self, request):
        data = request.POST
        if User.objects.filter(username=data['username'],email=data['email']).exists():
            messages = 'email already exist'
            print(messages)
            return render(request, 'user_add.html', {'messages': messages})
        user_obj = User(username=data['username'], email=data['email'],
                        first_name=data['first_name'], last_name=data['last_name'])
        user_obj.set_password(data['password'])
        user_obj.save()
        profile_obj = Profile(user=user_obj, phone_number=data['phone_number'], user_type=data['usertype'])
        profile_obj.save()
        return redirect( 'myapp:user_profile')

class ProfileDeleteView(View):

    def get(self,request,id):
         user=User.objects.get(pk=id)
         user.delete()
         return redirect('myapp:user_profile')


class TeacherprofileView(View):

    def get(self,request):
        user = Profile.objects.get(user=request.user)
        context = {
            'user_type': user.user_type,
            'teacher_profile': User.objects.filter(Q(profile__user_type='Teacher')
                                                )}
        return render(request, 'teacherprofile.html', {'context': context})


class TeacherProfileUpdateView(View):
    def get(self, request, id):
        update = User.objects.get(pk=id)
        return render(request, 'teacher_profile_update.html', {'user': update})

    def post(self, request, id):
        update = User.objects.get(pk=id)
        upt_form = UpdateForm(request.POST or None, instance=update)
        if upt_form.is_valid():
            upt_form.save()
            return redirect('myapp:teacherprofile')
        return render(request, 'teacher_profile_update.html', {'upt_form': upt_form, 'user': update})


class TeacherProfileView(View):

    def get(self, request):
        user = Profile.objects.get(user=request.user)
        print(user.user_type)
        context = {
            'user_type': user.user_type,
            'user_profile': User.objects.filter(Q(profile__user_type = 'Student')
                                                )

        }
        # create an paginator object from the same
        # per page two records will be displayed and last page may have 3 entries to avoid additional page
        emp_page_wise = Paginator(context['user_profile'], per_page=3, orphans=1)
        print(emp_page_wise)
        # get the current page number
        current = request.GET.get('page')
        print(current)
        emp_list = emp_page_wise.get_page(current)
        print(emp_list)
        # emp_list is an object of Page class
        return render(request, 'teacher_profile.html', {'page_obj': emp_list, 'user_type': context['user_type']})

    def post(self, request):
        return render(request, 'teacher_profile.html')

class StudentprofileView(View):
    def get(self, request):
        user = Profile.objects.get(user=request.user)
        context = {
            'user_type': user.user_type,
            'teacher_profile': User.objects.filter(Q(profile__user_type='Teacher')
                                                   )}
        return render(request, 'teacherprofile.html', {'context': context})

class StudentProfileUpdateView(View):
    def get(self, request, id):
        update = User.objects.get(pk=id)
        return render(request, 'teacher_profile_update.html', {'user': update})

    def post(self, request, id):
        update = User.objects.get(pk=id)
        upt_form = UpdateForm(request.POST or None, instance=update)
        if upt_form.is_valid():
            upt_form.save()
            return redirect('myapp:studentprofile')
        return render(request, 'student_profile_update.html', {'upt_form': upt_form, 'user': update})

class StudentProfileView(View):

    def get(self, request):
        try:
            user = Profile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            print('user does not exist')
        print(user.user_type)
        context = {
            'user_type': user.user_type,
            'user_profile': User.objects.all()
        }
        # create an paginator object from the same
        # per page two records will be displayed and last page may have 3 entries to avoid additional page
        emp_page_wise = Paginator(context['user_profile'], per_page=3, orphans=1)
        print(emp_page_wise)
        # get the current page number
        current = request.GET.get('page')
        print(current)
        emp_list = emp_page_wise.get_page(current)
        print(emp_list)
        # emp_list is an object of Page class
        return render(request, 'student_profile.html', {'page_obj': emp_list, 'user_type': context['user_type']})

    def post(self, request):
        return render(request, 'student_profile.html')

def signup_validation(request):

    try:
        data=request.POST
        if User.objects.filter(username = data['user']).exists():
            return HttpResponse('exist')
    except Exception as e:
        print(e)


    return HttpResponse('success')


def login_validation(request):
    try:
        data=request.POST
        print(data)
        if User.objects.filter(username = data['user'],password=data['user']).exists():
            return HttpResponse('both user and password are correct')
        else:
            return HttpResponse(' both user and password are incorrect')
    except Exception as e:
        print(e)


    return HttpResponse('successfully login ')


class TeacherAddSubjView(View):
    template_name = 'add_subj.html'

    def get(self,request):
        subjects_obj  = Subject.objects.all()
        return render(request,'add_subj.html',{"subjects":subjects_obj})

    def post(self,request):
        data = request.POST
        subjects_obj =Subject(sub_name = data['subject'],description = data['description'])
        subjects_obj.save()
        return redirect('myapp:add_subj')

class TeacherSubjectProfileView(View):

    def get(self, request):
        subjects_obj = Subject.objects.all()
        return render(request, 'subject_profile.html', {"subjects": subjects_obj})

    def post(self,request):
        return render(request, 'subject_profile.html' )

class SubjectsDeleteView(View):

    def get(self,request,id):
         user=Subject.objects.get(pk=id)
         user.delete()
         return redirect('myapp:subject_profile')

    def post(self,request):
        return render(request,'subject_profile.html')

class SubjectUpdateView(View):

    def get(self, request, id):
        update = Subject.objects.get(pk=id)
        return render(request, 'subject_update.html',{'user':update})

    def post(self, request, id):
        update = Subject.objects.get(pk=id)
        upt_form = SubjectUpdateForm(request.POST or None, instance=update)
        if upt_form.is_valid():
            upt_form.save()
            return redirect('myapp:subject_profile')
        return render(request, 'subject_update.html', {'upt_form': upt_form, 'user': update})

class AddMarksView(View):
    template_name = 'add_marks.html'

    def get(self, request,id):

        marks_obj= Marks.objects.filter(user__id=id) # add id for foreign key
        subject_obj = Subject.objects.values('sub_name')
        assigned_obj = marks_obj.values('subject__sub_name')
        all_subject = []
        assigned_subject = []
        for i in subject_obj:
            all_subject.append( i["sub_name"])
        for i in assigned_obj:
            assigned_subject.append(i['subject__sub_name'])
        print(all_subject,assigned_subject)
        all_subject = list(set(all_subject)-set(assigned_subject))
        return render(request, 'add_marks.html', {"marks_obj": marks_obj,"subjects":all_subject,'id':id})

    def post(self, request,id):
        data = request.POST
        try:
            data['subject']
        except:
            messages.info(request, 'please select subject')
            return HttpResponseRedirect(f'/add_marks/{id}')
        marks_obj =Marks(total_marks=data['total_marks'], description=data['description'],
            subject = Subject.objects.get(sub_name = data['subject']),
           user = User.objects.get(id = id))
        marks_obj.save()
        return HttpResponseRedirect(f'/add_marks/{id}')

class StudentReportView(View):
    template_name = 'student_report_cart.html'

    def get(self, request,id):

        marks_obj = Marks.objects.filter(user__id=id).order_by('total_marks')  # add id for foreign key
        marks_orderded_obj = marks_obj
        average = marks_obj.aggregate( Avg('total_marks'))


        max_subject = marks_orderded_obj.first().subject.sub_name
        min_subject = marks_orderded_obj.last().subject.sub_name
        return render(request, 'student_report_cart.html', {"marks_obj": marks_obj, 'id': id,'average':average,"max_subject":max_subject,"min_subject":min_subject})


def pdf_report(request,id):
     marks_obj = Marks.objects.filter(user__id=id)

     average = marks_obj.aggregate(Avg('total_marks'), Max('total_marks'), Min('total_marks'))
     template_path='pdf_report.html'

     print(get_template('pdf_report.html'))
     html_string =  render_to_string(template_path,{"marks_obj": marks_obj, 'id': id,'average':average,'user':request.user})
    #converting html to pdf

     filename = f"{marks_obj.first().user.username}_{marks_obj.first().user.id}.pdf"
     filepath = os.path.join(settings.BASE_DIR,"myapp","media","pdf",filename)
     print(filepath)
     pdfkit.from_string(html_string, filepath)

    #Sending
     # Define the full file path


     # Open the file for reading content
     path = open(filepath, 'rb')
     # Set the mime type
     mime_type, _ = mimetypes.guess_type(filepath)
     # Set the return value of the HttpResponse
     response = HttpResponse(path, content_type=mime_type)
     # Set the HTTP header for sending to browser
     response['Content-Disposition'] = "attachment; filename=%s" % filename
     # Return the response value
     return response
     # return HttpResponse(html_string)
"""
code for convert html to pdf
     # context={'marks_obj':marks_obj}
     # response=HttpResponse(content_type='application/pdf')
     # response['Content-Disposition']='filename="student_report_card.pdf"'
     # template=get_template(template_path)
     # html=template.render(context)
     # pisa_status=pisa.CreatePDF(
     #     html,dest=response)
     # if pisa_status.err:
     #     return HttpResponse('we had some errors <pre>'+ html +'<pre>')
     # return response
"""











