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


