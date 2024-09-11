import torch
import warnings
from typing import Any
warnings.filterwarnings('ignore')

random_index_choices = {
    # number of criteria : Random Index (Saaty, 1980)
    1: 0.00,
    2: 0.00,
    3: 0.58,
    4: 0.90,
    5: 1.12,
    6: 1.24,
    7: 1.32,
    8: 1.41,
    9: 1.45,
    10: 1.49,
    11: 1.51,
    12: 1.48,
    13: 1.56,
    14: 1.57,
    15: 1.58
}

class AHP:
    def __init__(self, criteria: list, alternatives: list, project_name: str) -> None:
        self.device = torch.device("cpu")
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        
        self.project_name = project_name
        self.criteria = criteria
        self.alternatives = alternatives
        self.num_criteria = len(criteria)
        self.num_alternatives = len(alternatives)
        self.pairwise_matrix = torch.ones((self.num_criteria, self.num_criteria), device=self.device)
        self.alternative_matrices = torch.ones((self.num_criteria, self.num_alternatives, self.num_alternatives), device=self.device)
        self.weights = None
        self.consistency_ratio = None

    def set_pairwise_matrix(self, matrix: list) -> None:
        self.pairwise_matrix = torch.tensor(matrix, device=self.device)

    def set_alternative_matrix(self, index: int, matrix: list) -> None:
        self.alternative_matrices[index] = torch.tensor(matrix, device=self.device)

    def calculate_weights(self) -> None:
        eig_val, eig_vec = torch.linalg.eig(self.pairwise_matrix)
        self.weights = torch.abs(eig_vec[:, 0]) / torch.sum(torch.abs(eig_vec[:, 0]))

    def calculate_consistency_ratio(self) -> None:
        lambda_max = torch.sum(self.weights * torch.sum(self.pairwise_matrix, axis=1))
        consistency_index = (lambda_max - self.num_criteria) / (self.num_criteria - 1)
        random_index = random_index_choices.get(self.num_criteria, 1.49)
        self.consistency_ratio = consistency_index / random_index

    def calculate_alternative_scores(self) -> torch.Tensor:
        alternative_scores = torch.zeros(self.num_alternatives, dtype=torch.float32, device=self.device)
        for i in range(self.num_alternatives):
            for j in range(self.num_criteria):
                eig_val, eig_vec = torch.linalg.eig(self.alternative_matrices[j])
                weights = torch.abs(eig_vec[:, 0]) / torch.sum(torch.abs(eig_vec[:, 0]))
                alternative_scores[i] += self.weights[j] * weights[i]
        return alternative_scores

    def rank_alternatives(self) -> tuple[torch.Tensor, torch.Tensor]:
        scores = self.calculate_alternative_scores()
        rankings = torch.argsort(scores, descending=True)
        return rankings, scores

    def run(self) -> dict[str, Any]:
        self.calculate_weights()
        self.calculate_consistency_ratio()
        rankings, scores = self.rank_alternatives()
        ranked_alternatives = [self.alternatives[i] for i in rankings]
        return {
            'criteria_comparison_matrix': self.pairwise_matrix.tolist(),
            'alternative_matrices': self.alternative_matrices.tolist(),
            'Ranking data': rankings.tolist(),
            'Ranking list': ranked_alternatives,
            'Alternative scores': scores.tolist(),
            'weights': self.weights.tolist(),
            'consistency_ratio': float(self.consistency_ratio),
        }