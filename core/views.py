# core/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import extract_text
import os
import json
import traceback
from markdown2 import markdown
from django.http import StreamingHttpResponse
from .llama import stream_llama_response
UPLOAD_DIR = "media"

# Ensure media directory exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def chat_view(request):
    return render(request, "chat.html")


@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_path = os.path.join(UPLOAD_DIR, file.name)

        try:
            # Save uploaded file
            with open(file_path, 'wb+') as dest:
                for chunk in file.chunks():
                    dest.write(chunk)

            # Extract text
            extracted_text = extract_text(file_path)

            return JsonResponse({"text": extracted_text})

        except Exception as e:
            return JsonResponse({
                "error": f"File upload or text extraction failed: {str(e)}"
            }, status=500)

    return JsonResponse({"error": "No file provided."}, status=400)


# @csrf_exempt
# def ask_question(request):
#     if request.method != 'POST':
#         return JsonResponse({"error": "Invalid request method. Use POST."}, status=405)

#     try:
#         data = json.loads(request.body)
#         question = data.get("question", "").strip()
#         context = data.get("context", "").strip()  # May be empty if no document uploaded

#         if not question:
#             return JsonResponse({"error": "Question is required."}, status=400)

#         # Ask LLaMA with or without context
#         answer = ask_llama(context, question)
#         html_response = markdown(answer)


#         if not answer or not answer.strip():
#             return JsonResponse({"error": "AI model did not return a valid response."}, status=500)

#         return JsonResponse({"answer": html_response})

#     except json.JSONDecodeError:
#         return JsonResponse({"error": "Invalid JSON input."}, status=400)

#     except Exception as e:
#         traceback.print_exc()
#         return JsonResponse({"error": f"Internal Server Error: {str(e)}"}, status=500)

@csrf_exempt
def stream_question(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST allowed."}, status=405)

    try:
        data = json.loads(request.body)
        question = data.get("question", "").strip()
        context = data.get("context", "").strip()

        if not question:
            return JsonResponse({"error": "Question is required."}, status=400)

        # Return stream using Server-Sent Events
        return StreamingHttpResponse(
            stream_llama_response(context, question),
            content_type='text/event-stream'
        )

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON input."}, status=400)

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": f"Internal Server Error: {str(e)}"}, status=500)

def test_view(request):

    return render(request,'test.html')