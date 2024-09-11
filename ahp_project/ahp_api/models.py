# ahp_api/models.py

from django.db import models
from django.contrib.auth.models import User

class AHPProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    criteria = models.JSONField()
    alternatives = models.JSONField()
    pairwise_matrix = models.JSONField()
    alternative_matrices = models.JSONField()
    ranking_data = models.JSONField()
    ranking_list = models.JSONField()
    alternative_scores = models.JSONField()
    weights = models.JSONField()
    consistency_ratio = models.FloatField()

    def __str__(self):
        return self.project_name