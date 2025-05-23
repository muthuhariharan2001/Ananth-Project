
# import os
# import re
# import pytesseract
# from rapidfuzz import fuzz
# from PIL import Image
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.core.files.storage import default_storage
# from django.conf import settings
# from rest_framework.decorators import api_view, parser_classes
# from rest_framework.parsers import MultiPartParser
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .utils import generate_image_hash
# from django.core.files.storage import default_storage
# # import imagehash
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# # from .models import ImageHash

# import os
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR'
# print(os.environ.get("TESSDATA_PREFIX"))



# # Ensure Upload Directory Exists
# UPLOAD_DIR = os.path.join(settings.MEDIA_ROOT, "uploads")
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# # Configure Tesseract OCR (Update path if needed)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# @csrf_exempt
# @api_view(["POST"])
# @parser_classes([MultiPartParser])
# def upload_files(request):
#     # Ensure both files are received
#     if 'aadhar' not in request.FILES or 'smart_card' not in request.FILES:
#         return JsonResponse({"error": "Both Aadhar and Smart Card images are required"}, status=400)

#     # Save Uploaded Files
#     aadhar_path = save_uploaded_file(request.FILES["aadhar"], "aadhar.png")
#     smart_card_path = save_uploaded_file(request.FILES["smart_card"], "smart_card.png")

#     # Extract Text from Images
#     aadhar_text = extract_text_from_image(aadhar_path)
#     smart_card_text = extract_text_from_image(smart_card_path)

#     # Extract Aadhar Number
#     aadhar_number = extract_aadhar_number(aadhar_text)

#     aadhar_address = extract_address_from_text(aadhar_text)
#     smart_card_address = extract_address_from_text(smart_card_text)

#     # Compare Aadhar & Smart Card Text
#     match_percentage = compare_text(aadhar_text, smart_card_text)
#     address_match_percentage = compare_text(aadhar_address, smart_card_address)

#     # Return Full Response
#     return JsonResponse({
#         "message": "Files uploaded successfully",
#         "aadhar_image_url": "/media/uploads/aadhar.png",
#         "smart_card_image_url": "/media/uploads/smart_card.png",
#         "uploaded_aadhar": "Aadhar Uploaded",
#         "uploaded_smart_card": "Smart Card Uploaded",
#         "aadhar_number": aadhar_number,
#         "match_percentage": match_percentage,
#         "aadhar_text": aadhar_text,
#         "smart_card_text": smart_card_text,
#         "aadhar_address": aadhar_address,
#         "smart_card_address": smart_card_address,
#         "address_match":address_match_percentage
#     }, status=200)

# def save_uploaded_file(uploaded_file, filename):
#     file_path = os.path.join(UPLOAD_DIR, filename)
#     with default_storage.open(file_path, 'wb+') as destination:
#         for chunk in uploaded_file.chunks():
#             destination.write(chunk)
#     return file_path

# def identify_card_type(request, text):
#     text = text.lower()
#     if any(keyword in text for keyword in ["தனிப்பட அடையாள", "ஆதார்", "uidai"]):
#         return "aadhaar"
#     elif any(keyword in text for keyword in ["உணவுப்பொருள்", "smart card", "பதிவு"]):
#         return "smart_card"
#     else:
#         return "unknown"


# def extract_text_from_image(image_path):
#     try:
#         img = Image.open(image_path)
#         text = pytesseract.image_to_string(img, lang='tam+eng')  # Ensure English is used
#         return text.strip()
#     except Exception as e:
#         return f"Error extracting text: {str(e)}"

# def extract_aadhar_number(text):
#     """ Extract Aadhar number from the OCR text """
#     match = re.search(r'\b\d{4}\s?\d{4}\s?\d{4}\b', text)  # Match 12-digit Aadhar number
#     return match.group(0) if match else "Not Found"

# # def compare_text(text1, text2):
# #     """ Calculate match percentage between two texts """
# #     words1 = set(text1.lower().split())
# #     words2 = set(text2.lower().split())
# #     common_words = words1.intersection(words2)
# #     match_percentage = (len(common_words) / max(len(words1), len(words2))) * 100 if max(len(words1), len(words2)) > 0 else 0
# #     return round(match_percentage, 2)

# from rapidfuzz import fuzz

# def clean_tamil_text(text):
#     # Remove non-Tamil Unicode
#     text = re.sub(r'[^\u0B80-\u0BFF\s]', '', text)
#     text = re.sub(r'\s+', ' ', text).strip()
#     return text

# def extract_address_from_text(text):
#     # Look for lines that contain address-related keywords
#     keywords = ['தெரு', 'புரம்', 'நகர்', 'தூத்துக்குடி', 'மாவட்டம்', 'தமிழ்நாடு']
#     lines = text.split('\n')
#     address_lines = [line.strip() for line in lines if any(k in line for k in keywords)]
#     return clean_tamil_text(' '.join(address_lines))


# def compare_text(text1, text2):
#     addr1 = extract_address_from_text(text1)
#     addr2 = extract_address_from_text(text2)
#     match_score = fuzz.token_sort_ratio(addr1, addr2)
#     return round(match_score, 2)

import os
import re
import pytesseract
from rapidfuzz import fuzz
from PIL import Image
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser

# Configure Tesseract paths for Windows environment
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR'

# Ensure upload directory exists
UPLOAD_DIR = os.path.join(settings.MEDIA_ROOT, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@csrf_exempt
@api_view(["POST"])
@parser_classes([MultiPartParser])
def upload_files(request):
    # Validate files presence
    if 'aadhar' not in request.FILES or 'smart_card' not in request.FILES:
        return JsonResponse({"error": "Both Aadhar and Smart Card images are required"}, status=400)

    # Save uploaded files
    aadhar_path = save_uploaded_file(request.FILES["aadhar"], "aadhar.png")
    smart_card_path = save_uploaded_file(request.FILES["smart_card"], "smart_card.png")

    # OCR extraction (Tamil + English)
    aadhar_text = extract_text_from_image(aadhar_path)
    smart_card_text = extract_text_from_image(smart_card_path)

    # Card type validation
    aadhar_type = identify_card_type(aadhar_text)
    smart_card_type = identify_card_type(smart_card_text)

    if aadhar_type != "aadhaar" or smart_card_type != "smart_card":
        return JsonResponse({"error": "Uploaded files are not valid Aadhar and Smart Card images"}, status=400)

    # Extract Aadhaar number
    aadhar_number = extract_aadhar_number(aadhar_text)

    # Extract addresses
    aadhar_address = extract_address_from_text(aadhar_text)
    smart_card_address = extract_address_from_text(smart_card_text)

    # Fuzzy match address similarity
    match_percentage = fuzz.token_sort_ratio(aadhar_address, smart_card_address)

    # Return response
    return JsonResponse({
        "message": "Files uploaded successfully",
        "aadhar_image_url": "/media/uploads/aadhar.png",
        "smart_card_image_url": "/media/uploads/smart_card.png",
        "aadhar_number": aadhar_number,
        "match_percentage": match_percentage,
        "aadhar_text": aadhar_text,
        "smart_card_text": smart_card_text,
        "aadhar_address": aadhar_address,
        "smart_card_address": smart_card_address,

    }, status=200)

from .models import ImageHashDBA, ImageHashDBB, HashPair

def create_hash_pair(dba_hash_str, dbb_hash_str):
    try:
        dba_obj, _ = ImageHashDBA.objects.get_or_create(hash=dba_hash_str)
        dbb_obj, _ = ImageHashDBB.objects.get_or_create(hash=dbb_hash_str)

        # Check if already paired
        if HashPair.objects.filter(dba_hash=dba_obj, dbb_hash=dbb_obj).exists():
            return "Already paired"

        # Create the pair
        HashPair.objects.create(dba_hash=dba_obj, dbb_hash=dbb_obj)
        return "Pair created"

    except Exception as e:
        return f"Error: {str(e)}"

def check_hash_pair(dba_hash_str, dbb_hash_str):
    try:
        dba_obj = ImageHashDBA.objects.get(hash=dba_hash_str)
        dbb_obj = ImageHashDBB.objects.get(hash=dbb_hash_str)
        return HashPair.objects.filter(dba_hash=dba_obj, dbb_hash=dbb_obj).exists()
    except ImageHashDBA.DoesNotExist:
        return False
    except ImageHashDBB.DoesNotExist:
        return False


def save_uploaded_file(uploaded_file, filename):
    file_path = os.path.join(UPLOAD_DIR, filename)
    with default_storage.open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return file_path


def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        # Tamil + English OCR for better accuracy
        text = pytesseract.image_to_string(img, lang='tam+eng')
        return text.strip()
    except Exception as e:
        return f"Error extracting text: {str(e)}"


def identify_card_type(text):
    text_lower = text.lower()
    print(text_lower)
    # mugavari in tamil text
    # Check for keywords to identify card type

    if any(keyword in text_lower for keyword in ["தனிப்பட அடையாள","government", "ஆதார்", "uidai", "unique",  "uid", "aadhaar", "aadhaar number", "aadhaar card", "aadhaar uid", "aadhaar uid number", "aadhaar uidai", "unique identification authority of india", "unique identification authority", "uidai aadhaar", "uidai number", "uidai card", "uidai uid", "uidai uid number", "uidai uidai", "uidai unique identification authority of india", "uidai unique identification authority", "uidai unique identification authority", "uidai unique identification authority of india", "uidai unique identification authority of india aadhaar", "uidai unique identification authority of india aadhaar number", "uidai unique identification authority of india aadhaar card", "uidai unique identification authority of india aadhaar uid", "uidai unique identification authority of india aadhaar uid number", "uidai unique identification authority of india aadhaar uidai", "uidai unique identification authority of india aadhaar uidai number"]):
        return "aadhaar"
    elif any(keyword in text_lower for keyword in ["உணவுப்பொருள்", "spouse","2067071206926", "name","bank", "IFSC", "MICR", "Name" , "Muthu", "Personal","Account", "பதிவு","electoral", "registration", "officer", "Date", "of", "birth"]):
        return "smart_card"
    else:
        return "unknown"


def extract_aadhar_number(text):
    match = re.search(r'\b\d{4}\s?\d{4}\s?\d{4}\b', text)
    return match.group(0) if match else "Not Found"


def clean_tamil_text(text):
    # Remove non-Tamil characters and digits
    return re.sub(r'[^அ-ஹஂ-௺\s]', '', text)

def extract_address_from_text(text):
    noise_keywords = [
        'அரசு', 'உணவுப்பொருள்', 'வழங்கல்', 'நுகர்', 'பாதுகாப்பு', 'துறை',
        'SUPPLIES', 'CONSUMER', 'PROTECTION', 'DEPARTMENT', 'GOVERNMENT', 
        'VID', 'vid', 'UIDAI', 'help', 'www.uidai.gov.in', 'C4', 'VID', '@', '+', '-', '|', '%'
    ]

    # Remove noise keywords
    for word in noise_keywords:
        text = text.replace(word, '')

    # Extract lines with known location keywords
    keywords = ['தெரு', 'புரம்', 'நகர்', 'மாவட்டம்', 'தமிழ்நாடு', 'தூத்துக்குடி']
    lines = text.splitlines()
    address_lines = [line for line in lines if any(k in line for k in keywords)]

    # Clean Tamil text only
    cleaned_address = clean_tamil_text(' '.join(address_lines))

    # Deduplicate words
    cleaned_unique = ' '.join(sorted(set(cleaned_address.split()), key=cleaned_address.split().index))
    return cleaned_unique



def compare_text(text1, text2):
    addr1 = extract_address_from_text(text1)
    addr2 = extract_address_from_text(text2)
    match_score = fuzz.partial_token_sort_ratio(addr1, addr2)
    return round(match_score, 2)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ImageHashDBA, ImageHashDBB, HashPair

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ImageHashDBA, ImageHashDBB, HashPair

class CheckImageHashView(APIView):
    def post(self, request):
        hash1 = request.data.get('hash1')
        hash2 = request.data.get('hash2')

        if not hash1 or not hash2:
            return Response({'error': 'Both hash1 and hash2 are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            hash_a_obj = ImageHashDBA.objects.filter(hash=hash1).first()
            hash_b_obj = ImageHashDBB.objects.filter(hash=hash2).first()

            if not hash_a_obj or not hash_b_obj:
                return Response({
                    'match': False,
                    'message': 'One or both hashes not found in the database.'
                }, status=status.HTTP_404_NOT_FOUND)

            is_pair = HashPair.objects.filter(dba_hash=hash_a_obj, dbb_hash=hash_b_obj).exists()

            if is_pair:
                return Response({
                    'match': True,
                    'message': 'Both cards belong to the same person.'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'match': False,
                    'message': 'The cards do not belong to the same person.'
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f'Internal Server Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SaveImageHashView(APIView):
    def post(self, request):
        hash_value = request.data.get('hash')
        db = request.data.get('db')

        if not hash_value or not db:
            return Response({'error': 'Hash or DB not provided'}, status=400)

        Model = ImageHashDBA if db == 'A' else ImageHashDBB

        obj, created = Model.objects.get_or_create(hash=hash_value)

        if created:
            return Response({'status': 'saved'}, status=201)
        else:
            return Response({'status': 'exists'}, status=200)

class SaveHashPairView(APIView):
    def post(self, request):
        hash1 = request.data.get('hash1')
        hash2 = request.data.get('hash2')

        if not hash1 or not hash2:
            return Response({'error': 'Both hash1 and hash2 are required'}, status=400)

        try:
            dba_obj, _ = ImageHashDBA.objects.get_or_create(hash=hash1)
            dbb_obj, _ = ImageHashDBB.objects.get_or_create(hash=hash2)

            pair_exists = HashPair.objects.filter(dba_hash=dba_obj, dbb_hash=dbb_obj).exists()
            if pair_exists:
                return Response({'status': 'already exists'}, status=200)

            HashPair.objects.create(dba_hash=dba_obj, dbb_hash=dbb_obj)
            return Response({'status': 'pair created'}, status=201)

        except Exception as e:
            return Response({'error': str(e)}, status=500)
