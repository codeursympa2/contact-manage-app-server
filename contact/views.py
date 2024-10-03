from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Contact
from .serializers import ContactSerializer

# Create your views here.

contactNotFound="Ce contact n'existe pas."

@api_view(['GET'])
def getContacts(request):
    contacts = Contact.objects.all() #On recupere toutes les données
    
    serializer = ContactSerializer(contacts,many=True) # on serialize
    
    return Response(serializer.data) #on renvoie les données

@api_view(['POST'])
def addContact(request):
    serializer=ContactSerializer(data=request.data) #deserialisation
    
    if serializer.is_valid():
        #Sauvegarde
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
        
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

@api_view(['DELETE'])
def deleteContact(request,pk): 
    try:
        #on verifie s'il existe
        contact=getById(pk)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Contact.DoesNotExist:
        return response404(contactNotFound)
    return response404(contactNotFound)
    
    

@api_view(['GET'])
def getContactById(request,pk):
    try:
        contact=getById(pk)
        return Response(ContactSerializer(contact).data)
    except:
        return response404(contactNotFound)
    return response404("Echec de la recupération du contact")
    
@api_view(['PUT'])    
def updateContact(request,pk):
    #check si le contact existe
    try:
        contact=getById(pk)
    except Contact.DoesNotExist:
        return response404(contactNotFound)
    
     # On désérialise les données en passant l'instance existante pour la mise à jour
    serializer= ContactSerializer(instance= contact,data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    # Retourne les erreurs du serializer si les données ne sont pas valides
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def search_contact(request):
    search_query = request.query_params.get('q', None)

    if not search_query:
        return Response([], status=400)

    try:
        # Recherche partielle dans les prénoms (firstname)
        contact = Contact.objects.filter(firstname__icontains=search_query)

        if contact:
            serializer = ContactSerializer(contact,many=True)
            return Response(serializer.data)
        
        # Recherche partielle dans les noms de famille (lastname)
        contact = Contact.objects.filter(lastname__icontains=search_query)

        if contact:
            serializer = ContactSerializer(contact,many=True)
            return Response(serializer.data)
        
        # Recherche partielle de l'email (email)
        contact = Contact.objects.filter(email__icontains=search_query)

        if contact:
            serializer = ContactSerializer(contact,many=True)
            return Response(serializer.data)

        # Recherche partielle dans les adresses
        contact = Contact.objects.filter(address__icontains=search_query)

        if contact:
            serializer = ContactSerializer(contact,many=True)
            return Response(serializer.data)

        # Recherche dans le champ tel (cas où le paramètre est numérique)
        if search_query.isdigit():
            contact = Contact.objects.filter(tel__icontains=search_query)

            if contact:
                serializer = ContactSerializer(contact,many=True)
                return Response(serializer.data)

        return Response([], status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


def getById(pk):
    return Contact.objects.get(pk=pk) 

def response404(message):
    return Response( {"error": message},status=status.HTTP_404_NOT_FOUND)     
