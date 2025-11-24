from functools import lru_cache
from typing import List

import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer

from .config import settings


def _providers() -> List[str]:
    preferred = ["CUDAExecutionProvider", "CPUExecutionProvider"]
    available = set(ort.get_available_providers())
    return [provider for provider in preferred if provider in available] or ["CPUExecutionProvider"]


class EmbeddingService:
    def __init__(self) -> None:
        self.session = self._load_session()
        self.tokenizer = self._load_tokenizer()

    def _load_session(self) -> ort.InferenceSession:
        options = ort.SessionOptions()
        options.intra_op_num_threads = settings.ORT_INTRA_OP_THREADS
        options.inter_op_num_threads = settings.ORT_INTER_OP_THREADS
        return ort.InferenceSession(settings.ONNX_MODEL_PATH, sess_options=options, providers=_providers())

    def _load_tokenizer(self):
        return AutoTokenizer.from_pretrained(settings.ONNX_TOKENIZER_PATH, local_files_only=True)

    @lru_cache()
    def _session_inputs(self) -> List[str]:
        return [inp.name for inp in self.session.get_inputs()]

    def encode(self, texts: List[str], prefix: str, normalize: bool) -> List[List[float]]:
        processed = self._prepare_inputs(texts, prefix)
        tokens = self.tokenizer(
            processed,
            padding=True,
            truncation=True,
            max_length=settings.TOKENIZER_MAX_LENGTH,
            return_tensors="np",
        )
        ort_inputs = {name: tokens[name] for name in self._session_inputs() if name in tokens}
        last_hidden_state = self.session.run(None, ort_inputs)[0]
        embeddings = self._mean_pool(last_hidden_state, tokens["attention_mask"])
        if normalize:
            embeddings = self._normalize(embeddings)
        return embeddings.tolist()

    @staticmethod
    def _prepare_inputs(texts: List[str], prefix: str) -> List[str]:
        pref = prefix.strip()
        return [(f"{pref} {text.strip()}").strip() if pref else text.strip() for text in texts]

    @staticmethod
    def _mean_pool(last_hidden_state: np.ndarray, attention_mask: np.ndarray) -> np.ndarray:
        mask = attention_mask.astype(np.float32)
        mask_expanded = np.expand_dims(mask, axis=-1)
        summed = np.sum(last_hidden_state * mask_expanded, axis=1)
        counts = np.clip(np.sum(mask_expanded, axis=1), 1e-9, None)
        return (summed / counts).astype(np.float32)

    @staticmethod
    def _normalize(vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / np.clip(norms, 1e-12, None)


service = EmbeddingService()
