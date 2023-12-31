from django.shortcuts import redirect, render
from portfolio_app.models import *
from django.views.generic import TemplateView
from django.contrib import messages
from sendgrid.helpers.mail import Mail
from django.template.loader import render_to_string
import os, re
from email.mime.text import MIMEText
import smtplib


# Create your views here.
# def index_page(request):
#       return render(request, "index.html")

class home_view(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        
        if request.method == 'POST':
            form_error = False
            FullName = request.POST.get('name', None)
            Email_ID = request.POST.get('email', None)
            Subject = request.POST.get('subject', None)
            Message = request.POST.get('message', None)

            if FullName and Email_ID and Subject and Message:
        
                regex = '^\w+([\.-]?\w+)@\w+([\.-]?\w+)(\.\w{2,3})+$'
                

                if FullName in ['', None] or Subject in ['', None] or Message in ['', None]:
                    messages.error(request, "All fields are  required..")
                    form_error = True
                    

                else:

                    if not(re.search(regex,Email_ID)):
                        form_error = True
                        messages.error(request, "Please enter valid email address!")
                    
                    else:
                        if not(form_error):
                            visitor = visitorquery(name = FullName,email = Email_ID, subject = Subject, message = Message)
                            visitor.save()                       
                            

                            email_text = '<p>Name : {}</p>'.format(FullName)
                            email_text += '<p>Email : {}</p>'.format(Email_ID)
                            email_text += '<p>Subject : {}</p>'.format(Subject)
                            email_text += '<p>Message : {}</p>'.format(Message)
                            
                            email_textc ='<p>Thank You {}</p>'.format(FullName)
                            email_textc += '<p>I will contacy shortly<br/><br/>Regards,<br/>Jay Makavana</p>'

                            recipientsc = [visitor.email]
                            recipients = ["jay95makavana@gmail.com"]
                            msg = MIMEText(email_text, 'html')
                            msgc = MIMEText(email_textc, 'html')
                            msg["Subject"] = "Jay Portfolio"
                            msgc["Subject"] = "Jay Makavana"
                            msg["From"] = visitor.email

                            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                            smtp_server.login("jay95makavana@gmail.com", "cnbzijigbaoydzsi")
                            smtp_server.sendmail("jay95makavana@gmail.com", recipients, msg.as_string())
                            smtp_server.sendmail(visitor.email, recipientsc, msgc.as_string())
                            smtp_server.quit()
                            return redirect('portfolio_app:home_view')
            else:
                a = "enter value"
                return render(request, "index.html", {'a': a})