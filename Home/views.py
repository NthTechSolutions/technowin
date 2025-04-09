from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
from django.db.models import Q
from Home.models import *
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from django.contrib import messages
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import about_us
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseBadRequest
from .models import contact_us  # Adjust the import as per your project structure
from django.core.validators import EmailValidator
import traceback
from django.utils.timezone import now
from datetime import datetime


# Create your views here.
def Home(request):
    today = datetime.today().strftime('%d-%m-%Y')  # Get today's date in DD-MM-YYYY format
    event = events_notification.objects.filter(event_date=today).first()
    return render(request,'Home/index.html', {'event': event}) 

# Create your views here.
def AboutUs(request):
    return render(request,'Home/about_us.html') 

# Create your views here.
def Services(request):
    return render(request,'Home/service.html') 

# Create your views here.
def ContactUs(request):
    return render(request,'Home/contact_us.html') 

def Software(request):
    return render(request,'Home/software.html') 

def siteMap(request):
    return render(request,'Home/siteMap.html') 

def Blogs(request):
    return render(request,'Home/blogs_index.html') 

def Product(request):
    return render(request,'Home/product.html') 

def get_botans(request):
    try:
        if request.method == "GET":
            q = str(request.GET.get('q', '')).strip()
            all_questions = list(chatbot.objects.values_list("question", flat=True))
            if all_questions:
                # Construct a prompt for Gemini to match the most relevant question
                prompt = (
                    "Here is a list of company-related questions:\n\n"
                    f"{all_questions}\n\n"
                    f"Find the question from the list that best matches the user's query: '{q}'.\n"
                    "Use semantic similarity to determine the closest match. \n"
                    "Respond only with the exact matching question from the list, without modifications or extra spaces. \n"
                    "If no close match is found, respond with 'No match'."
                )

                genai.configure(api_key='AIzaSyAPvmuqD0zQb5qZWL_NdUu29QMKOXoeRnY')
                model = genai.GenerativeModel('gemini-2.0-flash')
                response = model.generate_content(prompt)
                matched_question = response.text.strip()

                # If Gemini found a close match, retrieve the answer from the database
                if matched_question and matched_question != "No match":
                    chatbot_entry = chatbot.objects.filter(question=matched_question).first()
                    if chatbot_entry:
                        return JsonResponse({"result": "success", "data": chatbot_entry.answer}, safe=False)

            # If no match, generate a response using Gemini AI
            ai_prompt = (
                f"\r\n\r\n\r\nThis is a customer question: '{q}'\r\n\r\n\r\n"
                    "You are an AI chatbot for Technowin IT Infra Pvt Ltd, a leading software development company. "
                    "Answer only based on the company's services, expertise, and work domain. "
                    "Do not provide general AI responses, additional explanations, or unrelated details. "
                    "Strictly follow the question context and keep the response very short, direct, and relevant. "
                    "Focus only on software development, IT solutions, and technologies that we specialize in.\n\n"
                    "Limit your response to one or two sentences only. Avoid adding unnecessary information or assumptions.\n\n"
                )
            genai.configure(api_key='AIzaSyAPvmuqD0zQb5qZWL_NdUu29QMKOXoeRnY')
            model = genai.GenerativeModel('gemini-2.0-flash')
            ai_response = model.generate_content(ai_prompt)
            bot_reply = ai_response.text.strip().split("\n")[0]
           
            response_data = {'result': 'success', 'data':bot_reply}

    except Exception as e:
        print("Error:", e)
        response_data = {'result': 'fail', 'error': str(e)}

    return JsonResponse(response_data, safe=False)

def website_counter(request):
    try:
        if not request.COOKIES.get('visitor_counted'):
            counter_obj, created = webiste_counter.objects.get_or_create(id=1)
            counter_obj.counter += 1
            counter_obj.save()

            response = JsonResponse({"total_visits": counter_obj.counter})
            response.set_cookie('visitor_counted', 'true', max_age=86400)  # Cookie expires in 1 day
            return response
        else:
            return JsonResponse({"total_visits": webiste_counter.objects.get(id=1).counter})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# Function to validate name (only alphabets and spaces, no longer than 30 characters)
def validate_name(name):
    if not re.match(r'^[A-Za-z\s]+$', name):  # Allow alphabets and spaces only
        raise ValidationError("Name must contain only alphabets and spaces.")
    if len(name) > 30:
        raise ValidationError("Name must be less than or equal to 30 characters.")

# Function to validate subject and message (only alphabets and spaces, no longer than 50 characters)
def validate_subject_or_message(subject, message):
    # Validate subject
    if not re.match(r'^[A-Za-z\s]+$', subject):  # Allow alphabets and spaces only
        raise ValidationError("Subject must contain only alphabets and spaces.")
    if len(subject) > 50:
        raise ValidationError("Subject must be less than or equal to 50 characters.")
    
    # Validate message
    if not re.match(r'^[A-Za-z\s]+$', message):  # Allow alphabets and spaces only
        raise ValidationError("Message must contain only alphabets and spaces.")
    if len(message) > 50:
        raise ValidationError("Message must be less than or equal to 50 characters.")

# Define the custom email validation function
def validate_email(email):
    """ Validate email with custom logic: 1 '@' and max 2 dots '.' """
    at_count = email.count('@')
    dot_count = email.count('.')
    
    # Check if there's exactly one '@'
    if at_count != 1:
        raise ValidationError("Email must contain exactly one '@'.")
    
    # Check if there are no more than two dots ('.')
    if dot_count > 2:
        raise ValidationError("Email must contain no more than two '.' characters.")
    
    # Use Django's built-in EmailValidator to check the general validity of the email
    try:
        EmailValidator()(email)
    except ValidationError:
        raise ValidationError("Please enter a valid email address.")


def contactUsFormPost(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            email = request.POST.get("email")
            subject = request.POST.get("subject")
            message = request.POST.get("message")


            # Save the contact form data to the database
            new_contact = contact_us(
                name=name,
                email_id=email,
                subject=subject,
                message=message
            )
            new_contact.save()

            # Add a success message
            messages.success(request, "Thank you for contacting Technowin !")
            return redirect('ContactUs')  # Replace 'ContactUs' with your actual URL name for the contact page
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            fun = tb[0].name
            # error_log.objects.create(method=fun,error=str(e),error_date=now(),user='')
            # Add an error message if something else goes wrong
            messages.error(request, "An error occurred while processing your request.")
            return render(request, 'Home/contact_us.html')  # Replace with your actual template name
    else:
        return HttpResponseBadRequest("Invalid request method.")

    

# Function to validate full name (only alphabets, spaces, and a character limit)
def validate_full_name(name):
    # Check if the name contains only alphabets and spaces
    if not re.match(r'^[A-Za-z\s]+$', name):
        raise ValidationError("Full name must contain only alphabets and spaces.")
    
    # Check if the name length is less than or equal to 30 characters
    if len(name) > 30:
        raise ValidationError("Full name must not exceed 30 characters.")


# Function to validate the requirement field
def validate_requirement(requirement):
    # Validate that the requirement contains only alphabets and spaces, and is no longer than 50 characters
    if not re.match(r'^[A-Za-z\s]+$', requirement):  # Allow alphabets and spaces only
        raise ValidationError("Requirement must contain only alphabets and spaces.")
    if len(requirement) > 50:
        raise ValidationError("Requirement must be less than or equal to 50 characters.")

# Define the custom email validation function
def validate_email(email):
    """ Validate email with custom logic: 1 '@' and max 2 dots '.' """
    at_count = email.count('@')
    dot_count = email.count('.')
    
    # Check if there's exactly one '@'
    if at_count != 1:
        raise ValidationError("Email must contain exactly one '@'.")
    
    # Check if there are no more than two dots ('.')
    if dot_count > 2:
        raise ValidationError("Email must contain no more than two '.' characters.")
    
    # Use Django's built-in EmailValidator to check the general validity of the email
    try:
        EmailValidator()(email)
    except ValidationError:
        raise ValidationError("Please enter a valid email address.")

def aboutUsFormPost(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            email = request.POST.get("email")
            requirement = request.POST.get("requirement")

            # Check if a submission already exists for the given email
            if about_us.objects.filter(about_email_id=email).exists():
                messages.warning(request, "You have already filled the form with this email.")
                return redirect('Home')  # Redirect to home or another page

            # Validate full name (only alphabets)
            validate_full_name(name)

            # Validate email (Django provides a built-in email validator)
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, "Please provide a valid email address.")
                return redirect('Home')

            # Validate requirement (only alphabets and spaces, max length 50)
            validate_requirement(requirement)

            # Save the contact form data to the database
            new_enquiry = about_us(
                about_full_name=name,
                about_email_id=email,
                about_requirement=requirement
            )
            new_enquiry.save()

            # Add a success message
            messages.success(request, "Thank you for Booking a Demo!")
            return redirect('Home')  # Replace 'Home' with the actual URL name of your home page
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            fun = tb[0].name
            # error_log.objects.create(method=fun,error=str(e),error_date=now(),user='')
            # Add an error message if something else goes wrong
            messages.error(request, "An error occurred while processing your request.")
            return redirect('Home')
    else:
        return HttpResponseBadRequest("Invalid request method.")
