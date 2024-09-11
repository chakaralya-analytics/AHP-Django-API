# ahp_api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import AHPInputSerializer, AHPProjectSerializer
from .models import AHPProject
from AHP import AHP

class AHPCalculationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AHPInputSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            ahp = AHP(data['criteria'], data['alternatives'], data['project_name'])
            ahp.set_pairwise_matrix(data['pairwise_matrix'])
            for i, matrix in enumerate(data['alternative_matrices']):
                ahp.set_alternative_matrix(i, matrix)
            result = ahp.run()
            
            # Save the project
            project = AHPProject(
                user=request.user,
                project_name=data['project_name'],
                criteria=data['criteria'],
                alternatives=data['alternatives'],
                pairwise_matrix=data['pairwise_matrix'],
                alternative_matrices=data['alternative_matrices'],
                ranking_data=result['Ranking data'],
                ranking_list=result['Ranking list'],
                alternative_scores=result['Alternative scores'],
                weights=result['weights'],
                consistency_ratio=result['consistency_ratio']
            )
            project.save()
            
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProjectsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = AHPProject.objects.filter(user=request.user)
        serializer = AHPProjectSerializer(projects, many=True)
        return Response(serializer.data)