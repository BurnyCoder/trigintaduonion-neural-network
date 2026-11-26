"""Pure-data run definitions shared by the trainer, scheduler and research reports."""
from dataclasses import dataclass

STAGES=("pilot","primary","controls","sensitivity","images")


@dataclass(frozen=True)
class Config:
    task: str = "scene"
    model: str = "cd32"
    rule: str = "cd32"
    seed: int = 42
    families: int = 1024
    epochs: int = 80
    batch: int = 128
    lr: float = .003
    tag: str = ""

    @property
    def name(self):
        parts=[self.task,self.model,self.rule,f"s{self.seed}"]
        if self.task=="scene":
            parts.append(f"n{self.families}")
        if self.tag:
            if not self.tag.replace("-","").isalnum():
                raise ValueError("use alphanumeric run tags")
            parts.append(self.tag)
        return "-".join(parts)


def runs(stage):
    """Expand the public matrix without importing a model or accessing any measurements."""
    if stage=="pilot":
        return [Config()]
    if stage=="primary":
        return [Config(model=m,rule=t,seed=s) for s in range(8)
                for t in ("cd32","random") for m in ("cd32","random")]
    if stage=="controls":
        return [Config(model=m,seed=s) for m in ("frozen","onehop","shallow","real","budget","cd16")
                for s in range(8 if m in ("frozen","onehop","shallow") else 3)]
    if stage=="sensitivity":
        return [Config(model=m,seed=0,families=n) for n in (256,4096,32768)
                for m in ("cd32","random")]
    if stage!="images":
        raise ValueError(f"unknown study stage {stage}")
    primary=[Config(task="pixel",model=m,seed=s,epochs=60,lr=.1) for s in range(8)
             for m in ("cd32","random")]
    other=[Config(task="pixel",model=m,seed=s,epochs=60,lr=.1) for s in range(3)
           for m in ("real","budget","cd16")]
    graphs=[Config(task="graph",model=m,seed=0,epochs=60,lr=.003) for m in ("cd32","random")]
    return graphs+primary+other
