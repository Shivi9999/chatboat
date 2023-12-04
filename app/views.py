from django.shortcuts import render
# Create your views here.
from django.http import JsonResponse
from .models import QA
import spacy
from fuzzywuzzy import fuzz
from spellchecker import SpellChecker
from fuzzywuzzy import process
def chat(request):
    return render(request,'index.html')





def get_answer(request):
    try:
        if request.method == 'GET':
            user_input = request.GET.get('user_input', '').strip()
            if not user_input:
                return JsonResponse({'answer': 'Please provide a question.'})
            #Spell-check user input
            spell_checker = SpellChecker()
            corrected_input = ' '.join(spell_checker.correction(word) for word in user_input.split())
            nlp = spacy.load("en_core_web_sm")
            input_doc = nlp(corrected_input)
          
            matched_qa = QA.objects.filter(question__icontains=corrected_input).first()
            if not matched_qa:
                # If an exact match is not found, try fuzzy matching
                questions = QA.objects.values_list('question', flat=True)
                best_match, ratio = process.extractOne(corrected_input, questions)
                
                if ratio >= 80:
                    matched_qa = QA.objects.filter(question=best_match).first()
            if matched_qa:
                
                if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                    return JsonResponse({'answer': matched_qa.answer})
               
                return render(request, 'answer.html', {'user_input': user_input, 'answer': matched_qa.answer})
            else:
                if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                    return JsonResponse({'answer': 'Sorry, I don\'t have an answer for that question.'})
                return render(request, 'answer.html', {'user_input': user_input, 'answer': 'Sorry, I don\'t have an answer for that question.'})
        else:
            return JsonResponse({'error': 'Invalid request method.'})
    except Exception as e:
       
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'Sorry, I don\'t have an answer for that question.'})



# def get_answer(request):
#     user_input = request.GET.get('user_input', '').strip()

#     if not user_input:
#         return JsonResponse({'answer': 'Please provide a question.'})

#     # Spell-check user input
#     spell_checker = SpellChecker()
#     corrected_input = ' '.join(spell_checker.correction(word) for word in user_input.split())

#     # Use spaCy for basic NLP processing
#     nlp = spacy.load("en_core_web_sm")
#     input_doc = nlp(corrected_input)

#     # Query the database for any matching question
#     matched_qa = QA.objects.filter(question__icontains=corrected_input).first()
#     if matched_qa:
#         if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#                 return JsonResponse({'answer': matched_qa.answer})
#                 # If not an AJAX request, render the page with the answer
#         return render(request, 'answer.html', {'user_input':user_input,'answer': matched_qa.answer})
#     else:
#          if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#             print("Sorry, I don\'t have an answer for that question.'")
#          return render(request, 'answer.html', {'user_input':user_input,'answer': 'Sorry, I don\'t have an answer for that question.'})


# def get_answer(request):
#     try:
#         if request.method == 'GET':
#             user_input = request.GET.get('user_input', '').strip()
#             if not user_input:
#                 return JsonResponse({'answer': 'Please provide a question.'})
            
            
#             nlp = spacy.load("en_core_web_sm")
#             input_doc = nlp(user_input)
           
#             matched_qa = QA.objects.filter(question__icontains=user_input).first()

#             if matched_qa:
              
#                 if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#                     return JsonResponse({'answer': matched_qa.answer})
               
#                 return render(request, 'answer.html', {'user_input':user_input,'answer': matched_qa.answer})
#             else:
#                 if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#                     return JsonResponse({'answer': 'Sorry, I don\'t have an answer for that question.'})
#                 return render(request, 'answer.html', {'user_input':user_input,'answer': 'Sorry, I don\'t have an answer for that question.'})
#         else:
#             return JsonResponse({'error': 'Invalid request method.'})
#     except Exception as e:
        
#         print(f"An error occurred: {str(e)}")
#         return JsonResponse({'error': 'Internal Server Error'})


# def get_answer(request):
#     try:
#         if request.method == 'GET':
#             user_input = request.GET.get('user_input', '').strip()

#             if not user_input:
#                 return JsonResponse({'answer': 'Please provide a question.'})

#             # Use spaCy for basic NLP processing
#             nlp = spacy.load("en_core_web_sm")
#             input_doc = nlp(user_input)
#             print (input_doc)
#             # Query the database for any matching question
#             matched_qa = QA.objects.filter(question__icontains=user_input).first()
           
#             if matched_qa:
#               if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#                 return JsonResponse({'answer': matched_qa.answer})
#                 return render(request, 'index.html', {'answer': matched_qa.answer})

#             else:
#                 print("Sorry, I don\'t have an answer for that question.'")
#                 return render(request, 'index.html', {'answer': 'Sorry, I don\'t have an answer for that question.'})
#         else:
#             return JsonResponse({'error': 'Invalid request method.'})
#     except Exception as e:
#         # Log the exception for debugging
#         print(f"An error occurred: {str(e)}")
#         return JsonResponse({'error': 'Internal Server Error'})



# chatbot/views.py
# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import QA
# import spacy
# def chat(request):
#     if request.method == 'GET':
#         # If the user submits a question, process it
#         user_input = request.GET.get('user_input', '').strip()
#         if user_input:
#             try:
#                 # Use spaCy for basic NLP processing
#                 nlp = spacy.load("en_core_web_sm")
#                 input_doc = nlp(user_input)
#                 # Query the database for any matching question
#                 matched_qa = QA.objects.filter(question__icontains=user_input).first()
#                 if matched_qa:
#                     # Check the 'HTTP_X_REQUESTED_WITH' header for AJAX requests
#                     if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#                         return JsonResponse({'answer': matched_qa.answer})
#                     # If not an AJAX request, render the page with the answer
#                     return render(request, 'index.html', {'answer': matched_qa.answer})
#                 else:
#                     if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#                         return JsonResponse({'answer': 'Sorry, I don\'t have an answer for that question.'})
#                     return render(request, 'index.html', {'answer': 'Sorry, I don\'t have an answer for that question.'})
#             except Exception as e:
#                 # Log the exception for debugging
#                 print(f"An error occurred: {str(e)}")
#                 return JsonResponse({'error': 'Internal Server Error'})
#         # If the user is just loading the page, render the initial page
#         return render(request, 'index.html', {'answer': ''})
#     # Handle other request methods (e.g., POST) if necessary
#     return JsonResponse({'error': 'Invalid request method.'})


