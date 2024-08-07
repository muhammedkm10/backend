from django.http import HttpRequest
from ..utils import convertjwt
from ..models import CustomUser
from django.http import JsonResponse

class JwtCheckingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # Define the list of URLs to exclude from JWT checking
        excluded_urls = ['/authapp/userlogin', '/authapp/usersignup','/authapp/api/token','/authapp/api/token/refresh','/authapp/otpverification',]
        if request.method == "POST" and request.path in excluded_urls:
            response = self.get_response(request)
            return response
        if request.path.startswith('/media/user_gallary') or request.path.startswith('/adminapp/payment-success') or request.path.startswith('/ws/')  :
            response = self.get_response(request)
            return response
        else:
            response = self.get_response(request)
            auth_header = request.headers.get('Authorization')
            bearer_token = auth_header.split()
            if not auth_header or len(bearer_token)!= 2 or bearer_token[0].lower() != 'bearer':
                    print(auth_header)
                    request.custom_message = "Invalid Authorization header format."
                    return self.get_response(request)
            if auth_header:
                user_id ,email = convertjwt(auth_header)
                if not CustomUser.objects.get(id = user_id).is_blocked:
                       return response
                return JsonResponse({'message': 'User is blocked'}, status=403) 
            

            
            
            
                 














        



