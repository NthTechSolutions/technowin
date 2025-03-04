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


# Create your views here.
def Home(request):
    return render(request,'Home/index.html') 

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

# contactUs Form

# from django.http import HttpResponse, HttpResponseBadRequest

# def contactUsFormPost(request):
#     if request.method == "POST":
#         try:
#             name = request.POST.get("name")
#             email = request.POST.get("email")
#             subject = request.POST.get("subject")
#             message = request.POST.get("message")
#             new_contact = contact_us(
#                 name=name,
#                 email_id=email,
#                 subject=subject,
#                 message=message
#             )
#             new_contact.save()
#             return JsonResponse({"message": "Thank you for contacting us!"}, status=200)
#         except Exception as e:
#             return JsonResponse({"error": "An error occurred while processing your request."}, status=500)
#     else:
#         return HttpResponseBadRequest("Invalid request method.")



from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseBadRequest
from .models import contact_us  # Adjust the import as per your project structure

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
            messages.success(request, "Thank you for contacting us!")

            # Redirect to the same contact page or a confirmation page
            return redirect('ContactUs')  # Replace 'contact_us' with the actual URL name for the contact page
        except Exception as e:
            # Add an error message if something goes wrong
            messages.error(request, "An error occurred while processing your request.")
            return render(request, 'Home/contact_us.html')  # Replace with the actual template name
    else:
        return HttpResponseBadRequest("Invalid request method.")




# def aboutUsFormPost(request):
#     if request.method == "POST":
#         try:
#             name = request.POST.get("name")
#             email = request.POST.get("email")
#             budget = request.POST.get("budget")  # Changed 'subject' to 'budget' to match the form field name
#             requirement = request.POST.get("requirement")
            
#             # Save the contact form data to the database
#             new_enquiry = about_us(
#                 about_full_name=name,
#                 about_email_id=email,
#                 about_budget=budget,
#                 about_requirement=requirement
#             )
#             new_enquiry.save()

#             # Add a success message
#             messages.success(request, "Thank you for contacting us!")

#             # Redirect to the same page or another page to avoid form resubmission on refresh
#             return redirect('Home')  # Replace 'home' with the actual URL name of your home page

#         except Exception as e:
#             # Add an error message if something goes wrong
#             messages.error(request, "An error occurred while processing your request.")
#             return redirect('Home')  # Replace 'home' with the actual URL name of your home page
#     else:
#         return HttpResponseBadRequest("Invalid request method.")


# Function to validate full name (only alphabets and spaces)
def validate_full_name(name):
    if not re.match(r'^[A-Za-z\s]+$', name):
        raise ValidationError("Full name must contain only alphabets.")

# Function to validate budget (should be a valid number)
def validate_budget(budget):
    try:
        # Check if budget is a number (integer or float)
        float(budget)
    except ValueError:
        raise ValidationError("Budget must be a valid number.")

def aboutUsFormPost(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            email = request.POST.get("email")
            budget = request.POST.get("budget")
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

            # Validate budget (must be a number)
            validate_budget(budget)

            # Save the contact form data to the database
            new_enquiry = about_us(
                about_full_name=name,
                about_email_id=email,
                about_budget=budget,
                about_requirement=requirement
            )
            new_enquiry.save()

            # Add a success message
            messages.success(request, "Thank you for Booking  Demo!")

            # Redirect to the same page or another page to avoid form resubmission on refresh
            return redirect('Home')  # Replace 'home' with the actual URL name of your home page

        except ValidationError as e:
            # Handle validation errors
            messages.error(request, str(e))
            return redirect('Home')

        except Exception as e:
            # Add an error message if something goes wrong
            messages.error(request, "An error occurred while processing your request.")
            return redirect('Home')
    else:
        return HttpResponseBadRequest("Invalid request method.")