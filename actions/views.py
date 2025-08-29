from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ActionManager
from .serializers import ActionSerializer

action_manager = ActionManager()

@api_view(['GET', 'POST'])
def action_list(request):
    if request.method == 'GET':
        actions = action_manager.get_all()
        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = ActionSerializer(data=request.data)
        if serializer.is_valid():
            action_data = serializer.validated_data
            created_action = action_manager.create(action_data)
            response_serializer = ActionSerializer(created_action)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def action_detail(request, pk):
    action = action_manager.get_by_id(pk)
    
    if not action:
        return Response({'detail': 'Action not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ActionSerializer(action)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = ActionSerializer(data=request.data)
        if serializer.is_valid():
            action_data = serializer.validated_data
            updated_action = action_manager.update(pk, action_data)
            if updated_action:
                response_serializer = ActionSerializer(updated_action)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            return Response({'detail': 'Failed to update action'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        # For PATCH, allow partial updates
        serializer = ActionSerializer(action, data=request.data, partial=True)
        if serializer.is_valid():
            action_data = serializer.validated_data
            # Merge with existing action data
            updated_data = {**action, **action_data}
            updated_action = action_manager.update(pk, updated_data)
            if updated_action:
                response_serializer = ActionSerializer(updated_action)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            return Response({'detail': 'Failed to update action'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        action_manager.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
