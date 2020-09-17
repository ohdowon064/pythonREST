from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from games.models import Game
from games.serializers import GameSerializer

@api_view(['GET', 'POST'])
def game_list(request):
    if request.method == 'GET':
        games = Game.objects.all()
        games_serializer = GameSerializer(games, many=True) # many=True 옵션은 여러 인스턴스를 직렬화
        return Response(games_serializer.data)

    elif request.method == 'POST':
        game_serializer = GameSerializer(data=request.data)

        if game_serializer.is_valid():
            game_serializer.save()
            return Response(game_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'POST'])
def game_detail(request, pk):
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        games_serializer = GameSerializer(game)
        return Response(games_serializer.data)
    
    elif request.method == 'PUT':
        game_serializer = GameSerializer(game, data=request.data)
        if game_serializer.is_valid():
            game_serializer.save()
            return Response(game_serializer.data)
        return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
