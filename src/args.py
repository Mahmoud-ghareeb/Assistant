from dataclasses import dataclass
from typing import ClassVar, Dict


@dataclass
class Args:
    k: int = 2
    device: str = "cpu"
    model_id: ClassVar[dict[str, str]] = {
        "bert-base-multilingual-uncased": "google-bert/bert-base-multilingual-uncased",
        "paraphrase-MiniLM": "models/paraphrase-MiniLM-L3-v2",
        "paraphrase-multilingual-MiniLM": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "all-mpnet-base": "sentence-transformers/all-mpnet-base-v2",
        "multilingual-e5-base": "intfloat/multilingual-e5-base"
    }
