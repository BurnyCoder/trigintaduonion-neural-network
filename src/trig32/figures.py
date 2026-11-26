"""Export publication figures from raw records and fixed held-out example indices."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

from .paths import ROOT
from .analysis import interval

FIG=ROOT/"docs"/"figures"
INK="#142b39"
TEAL="#147d7a"
GOLD="#b36422"
BLUE="#315ca8"


def save(fig,name):
    FIG.mkdir(parents=True,exist_ok=True)
    fig.savefig(FIG/(name+".png"),dpi=140,bbox_inches="tight",facecolor="white")
    plt.close(fig)


def architecture():
    """Draw the visible variables, learned stages and supervisory signal in reading order."""
    fig,ax=plt.subplots(figsize=(10.2,2.4))
    ax.set(xlim=(0,10.2),ylim=(0,2.4))
    ax.axis("off")
    items=[("Objects","excitation, channel,\nnoisy measurement"),("Sensor encoder","signed linear bank\n+ nonlinear MLP"),
           ("Landmarks","distance attention\nfrom objects"),("Beacons","distance attention\nfrom landmarks"),
           ("Readout","symmetric pair\n→ same-type score")]
    for i,(name,desc) in enumerate(items):
        x=.07+2.06*i
        ax.add_patch(FancyBboxPatch((x,.68),1.81,1.14,boxstyle="round,pad=.05",fc="#e2f1f0" if i in (1,2,3) else "#eef1f6",ec=TEAL if i in (1,2,3) else BLUE))
        ax.text(x+.90,1.49,name,ha="center",weight="bold",color=INK,fontsize=10)
        ax.text(x+.90,1.02,desc,ha="center",va="center",color=INK,fontsize=8)
        if i<4:
            ax.annotate("",(x+2.03,1.25),(x+1.85,1.25),arrowprops={"arrowstyle":"->","color":INK})
    ax.text(.05,.21,"Training target   ·   One equality label per scene. Gradients propagate through both spatial hops and the sensor bank.",fontsize=9,color=INK)
    save(fig,"architecture")


def sample_size_figure(finished):
    """Compare the preselected seed on nested training samples and one shared test population."""
    series={"cd32":{}, "random":{}}
    for run in finished:
        c=run["config"]
        if c["task"]=="scene" and c["rule"]=="cd32" and c["seed"]==0 and c["model"] in series:
            series[c["model"]][c["families"]]=run["splits"]["test"]
    sizes=sorted(series["cd32"].keys() & series["random"].keys())
    if len(sizes)<2:
        return False
    fig,ax=plt.subplots(figsize=(7.1,3.2),layout="constrained")
    for model,label,color in (("cd32","Canonical learner",TEAL),("random","Randomized learner",GOLD)):
        acc=[100*series[model][n]["accuracy"] for n in sizes]
        ax.plot(sizes,acc,color=color,marker="o",label=label)
    test=series["cd32"][sizes[0]]
    for metric,desc,style in (("constant_accuracy","Constant","dotted"),("oracle_accuracy","Known-filter oracle","dashed")):
        ax.axhline(100*test[metric],color="#677482",linestyle=style,lw=1,label=desc)
    ax.set_xscale("log",base=2)
    ax.set_xticks(sizes,[f"{n:,}" for n in sizes])
    ax.set(xlabel="Training families (log scale)",ylabel="Held-out scene accuracy (%)",ylim=(0,100))
    ax.grid(axis="y",alpha=.18)
    ax.legend(ncol=2,fontsize=8,frameon=False)
    save(fig,"sample-size")
    return True


def figures(data):
    architecture()
    runs=data["runs"]
    finished=[r for r in runs if "test" in r["splits"]]
    has_sample_sizes=sample_size_figure(finished)
    if finished:
        group={}
        for r in finished:
            c=r["config"]
            key=(c["task"],c["model"],c["rule"],c["families"],"pilot" if c["seed"]==42 else "study")
            group.setdefault(key,[]).append(r["splits"]["test"]["accuracy"])
        fig,ax=plt.subplots(figsize=(8,max(2.5,.36*len(group)+1.2)))
        for i,(key,vals) in enumerate(group.items()):
            if len(vals)>=3:
                v=interval(vals)
                ax.hlines(i,100*v["lo"],100*v["hi"],color=TEAL,lw=2)
            offset=np.linspace(-.11,.11,len(vals)) if len(vals)>1 else np.zeros(1)
            ax.scatter(np.array(vals)*100,i+offset,c=BLUE,s=15,alpha=.7)
            ax.scatter(np.mean(vals)*100,i,marker="|",s=135,c=INK)
        labels=[]
        for task,model,rule,size,stage in group:
            if task=="scene":
                name=f"{model} learner / {rule} sensor / {size:,} families"
                labels.append(name+" (pilot)" if stage=="pilot" else name)
            else:
                labels.append(f"{'CIFAR-10 pixels' if task=='pixel' else 'CIFAR-10 superpixels'} / {model}")
        ax.set_yticks(range(len(group)),labels,fontsize=8)
        ax.set(xlabel="Held-out accuracy (%)   ·   points are individual runs",xlim=(0,100))
        ax.grid(axis="x",alpha=.22)
        save(fig,"scores")
    effects=[r for r in data["contrasts"][2:] if r["values"]]
    if effects:
        fig,ax=plt.subplots(figsize=(8,1.3+.64*len(effects)),layout="constrained")
        for i,r in enumerate(effects):
            scores=np.array(list(r["values"].values()))*100
            ax.scatter(scores,np.full(len(scores),i),color="#83a6a4",s=13)
            if r["lo"] is not None:
                ax.hlines(i,100*r["lo"],100*r["hi"],color=TEAL,lw=2)
            ax.scatter(100*r["mean"],i,s=35,c=INK)
            ax.scatter(100*r["threshold"],i,marker="x",c=GOLD,s=40)
        ax.axvline(0,color="#adb9b4",zorder=-1)
        ax.set_yticks(range(len(effects)),[r["title"] for r in effects],fontsize=8)
        ax.set_xlabel("Paired accuracy difference (percentage points)   ·   × decision threshold")
        ax.grid(axis="x",alpha=.18)
        save(fig,"effects")
    events=[]
    if runs:
        r=next((x for x in runs if x["config"]["seed"]==42),runs[0])
        events=r["curve"]
        if events:
            fig,axes=plt.subplots(1,2,figsize=(8,2.7),layout="constrained")
            for ax,key,label in zip(axes,("loss","accuracy"),("Cross-entropy loss","Accuracy (%)")):
                for split,color in (("train",TEAL),("val",GOLD)):
                    ax.plot([e["epoch"] for e in events],[e[split+"_"+key]*(100 if key=="accuracy" else 1) for e in events],label=split,color=color)
                ax.set(xlabel="Epoch",ylabel=label)
                if key=="accuracy": ax.set_ylim(0,100)
                ax.legend(frameon=False,fontsize=8)
            save(fig,"learning")
    scene=next((r for r in finished if "examples" in r and r["config"]["seed"]==42),None)
    if scene:
        f=scene["examples"]
        fig,axes=plt.subplots(1,2,figsize=(7,3.3),layout="constrained")
        for i,ax in enumerate(axes):
            b,l,o=[np.asarray(f[k][i]) for k in ("beacon","land","pos")]
            for p in b:
                q=l[np.linalg.norm(l-p,axis=1).argmin()]
                t=o[np.linalg.norm(o-q,axis=1).argmin()]
                ax.plot(*np.stack((p,q,t)).T,color="#829598",lw=1,ls="--")
            ax.scatter(*o.T,c=f["z"][i],cmap="coolwarm",vmin=-3,vmax=3,s=34,edgecolors=INK,lw=.4)
            ax.scatter(*l.T,marker="s",c=TEAL,s=36,label="landmark")
            ax.scatter(*b.T,marker="*",c=GOLD,s=100,label="beacon")
            ax.set(xlim=(0,1),ylim=(0,1),aspect="equal",xticks=[],yticks=[],
                   title=f"Label {int(f['labels'][i])}    P(same) {f['scores'][i]:.3f}")
        axes[0].legend(loc="upper left",fontsize=6)
        save(fig,"example")
    # Compare identical example IDs and observations before plotting across architectures.
    by_seed={}
    for r in finished:
        c=r["config"]
        if "examples" in r and c["rule"]=="cd32" and c["families"]==1024:
            by_seed.setdefault(c["seed"],[]).append(r)
    if by_seed:
        selected=by_seed[min(by_seed)]
        ex=selected[0]["examples"]
        names=["Ground truth","Known-filter oracle","Constant control"]
        values=[ex["labels"],ex["oracle"],np.zeros(len(ex["labels"]))]
        for r in selected:
            if r["examples"]["labels"]!=ex["labels"] or r["examples"]["z"]!=ex["z"]:
                raise ValueError("the displayed examples must come from the same world and sensor")
            names.append(r["config"]["model"])
            values.append(r["examples"]["scores"])
        fig,ax=plt.subplots(figsize=(7,max(2.4,.31*len(names)+1.2)),layout="constrained")
        pic=ax.imshow(np.asarray(values),aspect="auto",cmap="viridis",vmin=0,vmax=1)
        ax.set_yticks(range(len(names)),names)
        ax.set_xticks(range(len(ex["labels"])),[f"{i//2+1} {'swap' if i%2 else 'original'}" for i in range(len(ex["labels"]))],fontsize=8)
        for row,v in enumerate(values):
            for col,s in enumerate(v):
                ax.text(col,row,f"{s:.2f}",size=8,ha="center",va="center",color="black" if s>.55 else "white")
        fig.colorbar(pic,ax=ax,label="P(same) or binary decision",shrink=.8)
        save(fig,"predictions")
    # Reproduction in a fresh output directory may supply fewer results than the released clone.
    # Remove only named generator-owned images whose source observations are absent in this report.
    active={"scores":finished,"effects":effects,"learning":events,"example":scene,"predictions":by_seed,
            "sample-size":has_sample_sizes}
    for task in ("graph","pixel"):
        active["gallery-"+task]=any(r["config"]["task"]==task and "image_examples" in r for r in runs)
    for name,present in active.items():
        if not present:
            (FIG/(name+".png")).unlink(missing_ok=True)
