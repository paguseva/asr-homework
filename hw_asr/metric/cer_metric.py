from typing import List

import torch
from torch import Tensor

from hw_asr.base.base_metric import BaseMetric
from hw_asr.base.base_text_encoder import BaseTextEncoder
from hw_asr.metric.utils import calc_cer


class ArgmaxCERMetric(BaseMetric):
    def __init__(self, text_encoder: BaseTextEncoder, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_encoder = text_encoder

    def __call__(self, log_probs: Tensor, log_probs_length: Tensor, text: List[str], *args, **kwargs):
        cers = []
        log_probs = log_probs.detach().cpu()
        predictions = [
            inds[: int(ind_len)]
            for inds, ind_len in zip(log_probs, log_probs_length)
        ]
        for log_prob_vec, target_text in zip(predictions, text):
            if hasattr(self.text_encoder, "ctc_beam_search"):
                hypos = self.text_encoder.ctc_beam_search(log_prob_vec)
                pred_text = hypos[0][0]
            else:
                pred_text = self.text_encoder.decode(torch.argmax(log_prob_vec, dim=-1))
            cers.append(calc_cer(target_text, pred_text))
        return sum(cers) / len(cers)
