from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
app_name="myapp"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(),{'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('user_profile/', ProfileView.as_view(), name='user_profile'),
    path('student_profile/', StudentProfileView.as_view(), name='student_profile'),
    path('teacher_profile/', TeacherProfileView.as_view(), name='teacher_profile'),
    path('teacherprofile/', TeacherprofileView.as_view(), name='teacherprofile'),
    path('teacher_profile_update/<int:id>', TeacherProfileUpdateView.as_view(), name='teacher_profile_update'),
    path('user_update/<int:id>', ProfileUpdateView.as_view(), name='user_update'),
    path('user_delete/<int:id>', ProfileDeleteView.as_view(), name='user_delete'),
    path('user_add/', ProfileAddView.as_view(), name='user_add'),
    path('signup/validations/',signup_validation, name='signup/validations'),
    path('login/validations/', signup_validation, name='login/validations'),
    path('add_subj/', TeacherAddSubjView.as_view(), name='add_subj'),
    path('subject_profile/', TeacherSubjectProfileView.as_view(), name='subject_profile'),
    path('subject_delete/<int:id>', SubjectsDeleteView.as_view(), name='subject_delete'),
    path('subject_update/<int:id>', SubjectUpdateView.as_view(), name='subject_update'),
    path('add_marks/<int:id>', AddMarksView.as_view(), name='add_marks'),
    path('student_report_cart/<int:id>', StudentReportView.as_view(), name='student_report_cart'),
    path('pdf_report/<int:id>',pdf_report,name='pdf_report'),
    path('aboutus/', AboutUsView.as_view(), name='aboutus'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<str:token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    ]