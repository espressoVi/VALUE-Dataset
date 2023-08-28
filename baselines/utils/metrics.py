#!/usr/bin/env python
import toml
import numpy as np
from utils.rule import Rules

class Metrics:
    def __init__(self): 
        self.rules = Rules()
    def contradiction_count(self, predicts):
        res = 0
        for i in predicts:
            valid = self.rules.check(i)
            res += 0 if valid else 1
        return res/len(predicts)
    def strict_f_measure(self, labels, outputs):
        f1 = 0
        for pred, lab in zip(outputs, labels):
            valid = self.rules.check(pred)
            if not valid:
                continue
            n_gt, n_pred = np.where(lab>0, 1, 0).sum(), np.where(pred>0, 1, 0).sum()
            n_int = np.where(np.where(lab == pred, lab, 0)!=0,1,0).sum()
            f = 2*n_int/(n_pred+n_gt) if (n_pred+n_gt) > 0 else 0
            f1+=f
        return f1/len(labels)
    def f_measure(self, labels, outputs):
        n_gt, n_pred = np.where(labels>0, 1, 0).sum(-1), np.where(outputs>0, 1, 0).sum(-1)
        n_int = np.where(np.where(labels == outputs, labels, 0)!=0,1,0).sum(-1).astype(float)
        deno = (n_gt+n_pred).astype(float)
        return np.divide(2*n_int, deno, where=deno!=0, out=np.zeros_like(deno,dtype=float)).mean()
    def exact_match(self, labels, outputs):
        matches = np.all(np.where(labels==outputs, True, False), axis = -1).astype(float)
        return matches.mean()
    @property
    def metrics(self):
        return {'F1': lambda x,y : self.f_measure(x,y),
                'sF1': lambda x,y : self.strict_f_measure(x,y),
                'EM': lambda x,y : self.exact_match(x,y),
                'Contradiction': lambda _, x: self.contradiction_count(x),}
    def compute(self, labels, outputs):
        res = dict()
        for key,value in self.metrics.items():
            res[key] = value(labels, outputs)
        return res
    def eval_and_show(self, labels, outputs):
        res = self.compute(labels, outputs)
        answer = [f"{key} = {value:.4f} | " for key,value in res.items()]
        return ''.join(answer)
