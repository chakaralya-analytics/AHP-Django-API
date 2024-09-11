import torch
import warnings
from typing import Any
warnings.filterwarnings('ignore')


random_index_choices = {
    # number of criteria : Random Index (Saaty, 1980)
    1:0.00,
    2:0.00,
    3:0.58,
    4:0.90,
    5:1.12,
    6:1.24,
    7:1.32,
    8:1.41,
    9:1.45,
    10:1.49,
    11:1.51,
    12:1.48,
    13:1.56,
    14:1.57,
    15:1.58
}

class AHP:
    def __init__(self, criteria:list, alternatives:list, project_name:str) -> None:
        self.device = torch.device("cpu")
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        # elif torch.backends.mps.is_available():
        #     self.device = torch.device("mps")
        
        self.project_name = project_name
        self.criteria = criteria
        self.alternatives = alternatives
        self.num_criteria = len(criteria)
        self.num_alternatives = len(alternatives)
        self.pairwise_matrix = torch.ones((self.num_criteria, self.num_criteria), device = self.device)
        self.alternative_matrices = torch.ones((self.num_criteria, self.num_alternatives, self.num_alternatives))
        self.weights = None
        self.consistency_ratio = None

    def set_pairwise_matrix(self, matrix: list) -> None:
        self.pairwise_matrix = torch.tensor(matrix, device = self.device)

    def set_alternative_matrix(self, index: int, matrix: list) -> None:
        self.alternative_matrices[index] = torch.tensor(matrix, device = self.device)

    def calculate_weights(self) -> None:
        # weights of each criteria = eigenvector of that row /sum of eigenvector elements
        eig_val, eig_vec = torch.linalg.eig(self.pairwise_matrix)
        self.weights = eig_vec[:, 0] / torch.sum(eig_vec[:, 0]) 



    def calculate_consistency_ratio(self) -> None:

        # λ_max  = weighted sum of the rows of pairwise matrix
        lambda_max = torch.sum(self.weights * torch.sum(self.pairwise_matrix, axis=1))

        # Consistency index = (λ_max - n)/(n-1)
        consistency_index = (lambda_max - self.num_criteria) / (self.num_criteria - 1)
        
        # This value depends on the number of criteria
        random_index = random_index_choices.get(self.num_criteria, 1.49)

        self.consistency_ratio = consistency_index / random_index



    def calculate_alternative_scores(self)-> tuple[torch.Tensor]:
        alternative_scores = torch.zeros(self.num_alternatives, dtype=torch.cfloat, device = self.device)
        eig_vals = torch.zeros(self.num_criteria, device = self.device)
        eig_vecs = torch.zeros((self.num_criteria, self.num_alternatives, self.num_alternatives),device = self.device)
        for i in range(self.num_alternatives):
            for j in range(self.num_criteria):
                #  weights of an row (alternative) = eigen vector of the row / sum of the eigen vector elements
                eig_val, eig_vec = torch.linalg.eig(self.alternative_matrices[j])
                weights = eig_vec[:, 0] / torch.sum(eig_vec[:, 0])


                # Ranking Factor or Score = Inner dot product of weights of the Criteria (we got from pairwise matrix) and the weights of the Alternatives
                alternative_scores[i] += self.weights[j] * weights[i]
        return alternative_scores



    def rank_alternatives(self) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        scores= self.calculate_alternative_scores()
        # argsort returns the indices of the sorted form of the array (sorted array is not assigned)
        rankings = torch.argsort(torch.view_as_real(scores)[:,0])
        return rankings


    def run(self) -> dict[str, Any]:
        """ returns a json of format:
            'criteria_comparison_matrix'    : the pairwise comparison matrix of criteria
            'alternative_matrices'          : the alternative matrix
            'Ranking data'                  : the data each alternative's ranking score
            'Ranking list'                  : the ordered list of alternatives by ranks
            'weights'                       : weights of the AHP model's alternative selection process
            'consistency_ratio'             : consistency ratio
        """
        self.calculate_weights()
        self.calculate_consistency_ratio()
        rankings = self.rank_alternatives()
        # Ranking the alternatives from the ranked indices
        ranked_alternatives = [self.alternatives[i] for i in rankings]
        return {
                'criteria_comparison_matrix': self.pairwise_matrix.tolist(),
                'alternative_matrices': self.alternative_matrices.tolist(),
                'Ranking data': rankings.tolist(),
                'Ranking list': ranked_alternatives,
                'weights': self.weights.tolist(),
                'consistency_ratio': self.consistency_ratio,
            }

