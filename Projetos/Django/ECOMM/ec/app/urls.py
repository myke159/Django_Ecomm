from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('category/<slug:val>', views.CategoryView.as_view(), name="category"),
    path('category-title/<val>', views.CategoryTitle.as_view(), name="category-title"),
    path('category-detail/<int:pk>', views.ProductDetail.as_view(), name="productdetail"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('address/', views.Address, name="address"),
    path('updateaddress/<int:pk>', views.UpdateAddress.as_view(), name="updateaddress"),
    




    #Login Authentication
    # --Registrar Conta--
    path('registration/', views.CustomerRegistrationView.as_view(), name="customerregistrationview"),

    # --Logar uma conta existente--
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    
    # --Trocar senha da conta logada 1/2--
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'),name='passwordchange'),
    # --Encaminha para o resultado da troca de senha 2/2--
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),

    # --Desloga a conta--
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),

    # --Resetar a senha 1/4--
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),

    # --Resetar a senha 2/4--
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),

    # --Resetar a senha 3/4--
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),

    # --Resetar a senha 4/4--
    path('password-reset-complet/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
