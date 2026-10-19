# from .models import User
#
# class CurrentUserMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         request.user = None
#         user_id = request.session.get("user_id")
#         print(user_id)
#         if user_id:
#             request.user = User.objects.filter(id=user_id).first()
#         print("fin", user_id, request.user)
#         response = self.get_response(request)
#         return response