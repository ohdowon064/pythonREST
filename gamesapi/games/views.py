from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer # 직렬화 : 파이썬 모델 인스턴스 -> JSON 문자열
from rest_framework.parsers import JSONParser # 역직렬화 : JSON 문자열 -> 파이썬 모델 인스턴스
from rest_framework import status
from games.models import Game
from games.serializers import GameSerializer

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def game_list(request):
    if request.method == 'GET':
        games = Game.objects.all()
        games_serializer = GameSerializer(games, many=True)
        return JSONResponse(games_serializer.data)

    elif request.method == 'POST':
        game_data = JSONParser().parse(request)
        game_serializer = GameSerializer(data=game_data)
        
        # 직렬화된 데이터 접근시 유효성 검사
        # 유효할 경우
        if game_serializer.is_valid():
            game_serializer.save()
            return JSONResponse(game_serializer.data, status=status.HTTP_201_CREATED)
        
        # 유효하지 않은 경우
        return JSONResponse(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def game_detail(request, pk):
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
