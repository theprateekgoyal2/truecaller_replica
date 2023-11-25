from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Contact, UserMapContact, Profile, spamPhoneNumber
from .serializers import ContactSerializer

class ContactListAV(APIView):
	def get(self, request):

		usermap_contacts = UserMapContact.objects.filter(user=request.user)
		contacts = []
		for entry in usermap_contacts:
			contacts.append(entry.contact)
		serializer = ContactSerializer(contacts, many=True)
		
		return Response(serializer.data)
	
	def post(self,request):
		name = request.data["name"]
		phone_number = request.data["phone_number"]
		email = request.data.get("email", "NONE")
		if name is None or phone_number is None:
			return Response(
				{
					"Error": "name or phone_number cant be empty"
				},
				status = status.HTTP_400_BAD_REQUEST
			)
		
		if spamPhoneNumber.objects.filter(phone_number=phone_number).exists():	
			contact=Contact.objects.create(
				name=request.data["name"],
				phone_number=request.data["phone_number"],
				email=email,
				spam=True
			)
			mapping=UserMapContact.objects.create(
					user=request.user,
					contact=contact,
				)
			return Response(
					{
						"Message":"Contact saved successfully and marked as spam"
					},
					status = status.HTTP_201_CREATED
			)
		else:
			contact=Contact.objects.create(
                name=request.data["name"],
                phone_number=request.data["phone_number"],
                email=email,
            )
			mapping=UserMapContact.objects.create(
                    user=request.user,
                    contact=contact,
            )
			return Response(
                    {
                        "Message":"Contact saved successfully"
                    },
                    status = status.HTTP_201_CREATED
            )

@permission_classes((AllowAny,))
class Register(APIView):
    def post(self, request):
        name = request.data.get("name")
        phone_number = request.data.get("phone_number")
        email = request.data.get("email", "NONE")
        password = request.data.get("password")

        if name is None or phone_number is None or password is None:
            return Response(
                {
                    "Error": "name and phone_number cant be empty"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the provided phone number exists in the SpamPhoneNumber model
        if spamPhoneNumber.objects.filter(phone_number=phone_number).exists():
			
            # If it exists, create a new user and profile with spam status set to True
            user = User(username=name, email=email)
            if user:
                user.set_password(password)
                user.save()
				
            profile = Profile.objects.create(
				user=user, 
				phone_number=phone_number, 
				email=email,
				spam=True
			)
            return Response(
                {
                    "Message": "Registered successfully, and the phone number is marked as spam."
                },
                status=status.HTTP_200_OK
            )
        else:
            # If the phone number is not in the spam list, proceed with the regular registration process
            user = User(username=name, email=email)
            if user:
                user.set_password(password)
                user.save()
				
            profile = Profile.objects.create(
				user=user, 
				phone_number=phone_number, 
				email=email, 
				spam=True
			)

            return Response(
                {
                    "Message": "Registered successfully"
                },
                status=status.HTTP_200_OK
            )

@permission_classes((AllowAny,))
class Login(APIView):
	def post(self,request):
		if not request.data:
			return Response(
				{
					"Error":"Please provide username and password"
				},
				status=status.HTTP_400_BAD_REQUEST
			)
		username=request.data.get("username")
		password=request.data.get("password")
		if username is None or password is None:
			return Response(
				{
					"Error":"Invalid Credentials"
				},
				status=status.HTTP_404_NOT_FOUND
			)
		user = authenticate(username = username, password = password)
		token, _ =Token.objects.get_or_create(user = user)
		return Response(
			{
				"Token":token.key
			},
			status=status.HTTP_200_OK
		)

class MarkAsSpam(APIView):
	def post(self,request):
		phone_number=request.data.get("phone_number")
		if not phone_number:
			return Response(
				{
					"Error":"Phone number required"
				},
				status = status.HTTP_400_BAD_REQUEST
			)
		contact=Contact.objects.filter(phone_number=phone_number).update(spam=True)
		profile=Profile.objects.filter(phone_number=phone_number).update(spam=True)
		if (contact+profile):
			return Response(
				{
					"Message":"Contact marked as spam successfully"
				},
				status = status.HTTP_200_OK
			)
		else:
			spam = spamPhoneNumber(
				phone_number=phone_number, 
				spam=True
			)
			spam.save()
			return Response(
				{
					"message":"New Phone number marked as spam"
				},
				status = status.HTTP_200_OK
			)


class SearchName(APIView):
	def get(self,request):
		name=request.data.get("name")
		if request.data["name"] is None:
			return Response(
				{
					"Error":"Name is required!!"
				},
				status = status.HTTP_400_BAD_REQUEST
			)
		profile_start=Profile.objects.filter(user__username__startswith=name)
		profile_contain=Profile.objects.filter(user__username__contains=name).exclude(user__username__startswith=name)
		contact_start=Contact.objects.filter(name__startswith=name)
		contact_contain=Contact.objects.filter(name__contains=name).exclude(name__startswith=name)
		response=[]
		for contact in profile_start:
			user = contact.user
			response.append(
					{
						"name":user.username,
						"phone_number":contact.phone_number,
						"email": contact.email,
						"spam":contact.spam,
					}
				)
		
		for contact in profile_contain:
			user = contact.user
			response.append(
					{
						"name":user.username,
						"phone_number":contact.phone_number,
						"email": contact.email,
						"spam":contact.spam,
					}
				)
		
		for contact in contact_start:
			response.append(
					{
						"name":contact.name,
						"phone_number":contact.phone_number,
						"email": contact.email,
						"spam":contact.spam,
					}
				)
		
		for contact in contact_contain:
			response.append(
					{
						"name":contact.name,
						"phone_number":contact.phone_number,
						"email": contact.email,
						"spam":contact.spam,
					}
				)
	
		serializer = ContactSerializer(response, many=True)
		return Response(serializer.data)

class SearchPhoneNumber(APIView):
	def get(self,request):
		phone_number=request.data.get("phone_number")
		if request.data["phone_number"] is None:
			return Response(
				{
					"Error":"Phone number required!!"
				},
				status = status.HTTP_400_BAD_REQUEST
			)
		# Using .first() to get the first (and only) instance from the queryset
		profile=Profile.objects.filter(phone_number=phone_number).first()
		if profile:
			user = profile.user
			return Response(
					{
						"name":user.username,
						"phone_number":profile.phone_number,
						"spam":profile.spam,
						"email":profile.email
					}
				)
		else:
			contact=Contact.objects.filter(phone_number=phone_number)
			serializer=ContactSerializer(contact,many=True)
			return Response(
					serializer.data
				)