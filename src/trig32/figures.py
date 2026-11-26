"""Export publication figures from raw records and fixed held-out example indices."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

from .paths import ROOT

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


def figures(data):
    architecture()
    runs=data["runs"]
    finished=[r for r in runs if "test" in r["splits"]]
    if finished:
        group={}
        for r in finished:
            c=r["config"]
            key=(c["task"],c["model"],c["rule"],c["families"],"pilot" if c["seed"]==42 else "study")
            group.setdefault(key,[]).append(r["splits"]["test"]["accuracy"])
        fig,ax=plt.subplots(figsize=(8,max(2.5,.36*len(group)+1.2)))
        for i,(key,vals) in enumerate(group.items()):
            ax.scatter(np.array(vals)*100,np.full(len(vals),i),c=BLUE,s=15,alpha=.7)
            ax.scatter(np.mean(vals)*100,i,marker="|",s=135,c=INK)
        ax.set_yticks(range(len(group)),[" / ".join(map(str,k)) for k in group],fontsize=8)
        ax.set(xlabel="Held-out accuracy (%)   ·   points are individual runs",xlim=(0,100))
        ax.grid(axis="x",alpha=.22)
        save(fig,"scores")
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
