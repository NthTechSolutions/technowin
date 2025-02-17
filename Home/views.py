from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
from django.db.models import Q
from .models import chatbot

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


def get_botans(request):
    try:
        if request.method == "GET":
            q = str(request.GET.get('q', '')).strip()

            # Check if the question exists in the database (fuzzy search)
            chatbot_entry = chatbot.objects.filter(Q(question__icontains=q)).first()
            if chatbot_entry:
                response_data = {'result': 'success', 'data': chatbot_entry.link if chatbot_entry.link else chatbot_entry.answer}
            else:
                # Configure Gemini API
                genai.configure(api_key='AIzaSyDY58C2WPnq6qRLMauptJJ6urnzHRtNg6Q')
                model = genai.GenerativeModel('gemini-pro')

                # Refined prompt for company-specific responses
                prompt = (
                    f"\r\n\r\n\r\nThis is a customer question: '{q}'\r\n\r\n\r\n"
                    "You are an AI chatbot for Technowin IT Infra Pvt Ltd, a leading software development company. "
                    "Answer only based on the company's services, expertise, and work domain. "
                    "Do not provide general AI responses, additional explanations, or unrelated details. "
                    "Strictly follow the question context and keep the response very short, direct, and relevant. "
                    "Focus only on software development, IT solutions, and technologies that we specialize in.\n\n"
                    "Limit your response to one or two sentences only. Avoid adding unnecessary information or assumptions.\n\n"
                )


                # Get response from Gemini
                data = model.generate_content(prompt)
                response_data = {'result': 'success', 'data': data.text}

    except Exception as e:
        print("Error:", e)
        response_data = {'result': 'fail', 'error': str(e)}

    return JsonResponse(response_data, safe=False)