from dataclasses import dataclass
from typing import List


@dataclass
class Question:
    """
    Class representing a question

    Attributes:
    - id: Question ID
    - question: Question text
    - answers: List of answers
    - correct_answer: Index of the correct answer
    """
    id: int
    question: str
    answers: List[str]
    correct_answer: int
