"""Regenerate the public study from immutable evaluations, without importing a model."""
from collections import defaultdict
import shutil

from .analysis import collect, percent, table, row_metrics, HEADERS, interval
from .figures import figures
from .paths import ROOT,write_json
from .protocol import STAGES,runs as planned_runs

GH="https://github.com/BurnyCoder/trigintaduonion-neural-network"
PAGES="https://burnycoder.github.io/trigintaduonion-neural-network/"
REPORTS=ROOT/"reports"
DOCS=ROOT/"docs"


def write(path,body):
    """Preserve file modification time if its reproducible contents are identical."""
    path.parent.mkdir(parents=True,exist_ok=True)
    body=body.rstrip()+"\n"
    if not path.exists() or path.read_text(encoding="utf-8")!=body:
        path.write_text(body,encoding="utf-8")


def metrics_block(path,body):
    text=path.read_text(encoding="utf-8")
    a,b="<!-- metrics:start -->","<!-- metrics:end -->"
    before,tail=text.split(a,1)
    _,after=tail.split(b,1)
    write(path,before+a+"\n"+body+"\n"+b+after)


def label(r):
    c=r["config"]
    return f"{c['task']} / {c['model']} / {c['rule']} / {c['families']} families" if c["task"]=="scene" else f"{c['task']} / {c['model']}"


def grouped(data):
    groups=defaultdict(list)
    for r in data["runs"]:
        groups[(label(r),r["config"]["seed"]==42)].append(r)
    rows=[]
    for (name,pilot),rs in groups.items():
        scores=[r["splits"]["test"]["accuracy"] for r in rs if "test" in r["splits"]]
        v=interval(scores)
        ci=f"{percent(v['lo'])} to {percent(v['hi'])}" if v["lo"] is not None else "—"
        rows.append([name+(" (pilot)" if pilot else ""),len(scores),rs[0]["trainable"],percent(v["mean"]),ci])
    return rows


def decision_rows(data):
    rows=[]
    for i,c in enumerate(data["contrasts"]):
        def display(v):
            return percent(v) if i<2 or v is None else f"{100*v:.2f} pp"
        ci=display(c["lo"])+" to "+display(c["hi"]) if c["n"]>1 else "—"
        rows.append([c["title"],c["n"],display(c["mean"]),ci,display(c["threshold"]),c["decision"]])
    return rows


def headline(data):
    pilot=next((r for r in data["runs"] if r["config"]["seed"]==42 and r["splits"]),None)
    if not pilot:
        return "The pilot has no released test prediction yet."
    s=pilot["splits"]["test"]
    return (f"The pilot classified {percent(s['accuracy'])} of {s['examples']:,} unseen scenes correctly and answered "
            f"both mates correctly in {percent(s['both_correct'])} of families. The constant control scored "
            f"{percent(s['constant_accuracy'])} and the privileged sensor-and-geometry oracle scored {percent(s['oracle_accuracy'])}. "
            f"On unseen sensor coordinates accuracy was {percent(pilot['splits']['heldout']['accuracy'])}. "
            "Seed 42 is excluded from all confirmatory contrasts.")


def algebra_rows(data):
    groups=defaultdict(list)
    for a in data["algebra"]:
        groups[(a["task"],a.get("teacher","cd32"),a["model"],a["n"])].append(a)
    return [[*key,len(rs),f"{sum(r['nmse'] for r in rs)/len(rs):.3g}",
             f"{sum(r['basis_correct'] for r in rs)/len(rs):.1f}" if "basis_correct" in rs[0] else "—"]
            for key,rs in groups.items()]


def algebra_finding(data):
    rows=data["algebra"]
    def means(**condition):
        groups=[r for r in rows if all(r.get(k)==v for k,v in condition.items())]
        return sum(r["nmse"] for r in groups)/len(groups) if groups else None
    worlds={r["seed"] for r in rows}
    if len(worlds)!=8:
        return "The algebra diagnostics await the full planned world set."
    errors=[means(task="multiplier",teacher=t,model=m,n=8) for t,m in
            (("cd32","cd32"),("cd32","random"),("random","random"),("random","cd32"))]
    product=[r for r in rows if r["task"]=="product" and r["model"]=="bilinear" and r["n"]==2048]
    return (f"Across {len(worlds)} algebra worlds, eight training vectors gave mean normalized squared errors "
            f"of {errors[0]:.2g} and {errors[1]:.3f} for the matched and mismatched canonical-sensor fits. "
            f"On randomized sensors those errors were {errors[2]:.2g} and {errors[3]:.3f}. "
            f"With 2,048 input pairs, the blind bilinear learner recovered at least {min(r['basis_correct'] for r in product):,} "
            f"of the 1,024 signed basis products per world. Its mean error was {means(task='product',model='bilinear',n=2048):.2g}, "
            f"compared with {means(task='product',model='shuffled',n=2048):.2f} after shuffling targets.")


def documents(data):
    """Build Markdown summaries, each experiment's lab notebook and the machine-readable explorer."""
    runs=data["runs"]
    groups=grouped(data)
    decisions=decision_rows(data)
    algebra=algebra_rows(data)
    gtable=table(groups,["Task / learner / sensor","Tested worlds","Trainable","Mean test","95% interval"])
    dtable=table(decisions,["Registered endpoint","Worlds","Estimate","95% interval","Threshold","Decision"])
    atable=table(algebra,["Diagnostic","Teacher","Learner","Examples","Seeds","Mean NMSE","Correct basis products"])
    pilot=headline(data)
    crosses=data["contrasts"][2:4]
    if any(c["decision"]=="pending" for c in crosses):
        matching="The registered crossover awaits complete paired worlds."
    else:
        outcome=("Both directional matching criteria passed." if all(c["decision"]=="above threshold" for c in crosses)
                 else "The registered crossover did not clear both thresholds.")
        matching=(f"The mean benefit of matching the sensor rule was {100*crosses[0]['mean']:.2f} percentage points "
                  f"on canonical sensors and {100*crosses[1]['mean']:.2f} points on randomized sensors. "+outcome)
    brief=pilot+" "+matching
    audits=[a for a in data["audits"] if "interventions" in a]
    probe=""
    if audits:
        rows=[]
        for a in audits:
            for name,m in a["interventions"].items():
                rows.append([a["run"],name,percent(m["accuracy_against_original_labels"]),
                             m["changed_decisions"],f"{m['max_probability_change']:.3g}"])
        probe="\n\n## Supplementary fixed-checkpoint interventions\n\n"+table(rows,["Run","Input","Accuracy against original labels","Decisions changed","Max Δ probability"])
        for a in audits:
            if "float64_reference" in a:
                m=a["float64_reference"]["isometry_and_reindexing"]
                probe+=f"\n\nThe float64 symmetry reference for {a['run']} changed {m['changed_decisions']} decisions. Maximum absolute probability drift was {m['max_probability_change']:.3g}."
    for r in runs:
        if "image_examples" in r:
            from .paths import RESULTS
            dest=DOCS/"figures"/("gallery-"+r["config"]["task"]+".png")
            shutil.copyfile(RESULTS/r["name"]/"test-gallery.png",dest)
    images=[]
    for key,desc in [("scores","Each dot is one test run and each black tick is the mean."),("example","A fixed pilot pair with the selected paths, ground truth and predicted probability."),("predictions","Ground truth, analytic controls and model predictions on the same held-out pairs."),("learning","Pilot training and validation trajectories.")]:
        if (DOCS/"figures"/(key+".png")).exists():
            images.append(f"![{desc}](docs/figures/{key}.png)")
    readme=ROOT/"README.md"
    text=readme.read_text(encoding="utf-8")
    marker="<!-- highlights:start -->"
    end="<!-- highlights:end -->"
    if marker not in text:
        title,intro,rest=text.split("\n\n",2)
        text="\n\n".join([title,intro,marker+"\n"+end,rest])
    a,tail=text.split(marker,1)
    _,b=tail.split(end,1)
    top=brief
    if (DOCS/"figures"/"example.png").exists():
        top+="\n\n![Held-out scene pair and learned same-type probabilities](docs/figures/example.png)"
    write(readme,a+marker+"\n"+top+"\n"+end+b)
    images=[i for i in images if "figures/example.png" not in i]
    if (DOCS/"figures"/"effects.png").exists():
        images.insert(0,"![Paired differences, seed-level points and 95% intervals](docs/figures/effects.png)")
    metrics_block(readme,"\n\n".join([*images,gtable] if groups else [brief]))
    metrics_block(DOCS/"model-card.md",brief+f" [All measured outcomes]({PAGES})")
    write(REPORTS/"summary.md","# Results\n\n"+brief+"\n\n"+gtable+"\n\n"+dtable+probe+
          "\n\nWorld differences are expressed as percentage points on a 0–100 scale. Intervals use a two-sided Student t across worlds. A single world has no between-world interval. Pilot and confirmatory worlds are reported separately.\n\n[Raw manifests and predictions](../results/) · [Preregistration](preregistration.md) · [Explorer]("+PAGES+")")
    ex=REPORTS/"experiments"
    individual=[]
    for r in runs:
        c=r["config"]
        s=r["splits"].get("test",{})
        name=r["name"]
        meaning=("A family contains the original scene and a counterfactual with reversed ground truth." if c["task"]=="scene"
                 else "Accuracy counts correctly classified held-out images or image graphs.")
        info=f"{label(r)}. Seed {c['seed']}, {c['epochs']} epochs, batch size {c['batch']}, starting learning rate {c['lr']}. "+meaning
        if s:
            outcome=f"The selected epoch was {r['best_epoch']}. Validation accuracy was {percent(r['val_accuracy'])} and test accuracy was {percent(s['accuracy'])}."
            if c["task"]=="scene":
                outcome+=f" Both mates were correct in {percent(s['both_correct'])} of families. The oracle scored {percent(s['oracle_accuracy'])}."
        else:
            outcome=f"The validation-selected epoch was {r['best_epoch']}. Test predictions are pending release."
        write(ex/name/"experiment.md",f"# {name}\n\n{info}\n\n{outcome}\n\n"+table([row_metrics(r)],HEADERS)+
              f"\n\nDevice {r['hardware']['gpu'] or r['hardware']['device']}. Training took {r['seconds']:.1f} epoch-loop seconds. Peak allocated device memory was {r['peak_gpu_bytes']:,} bytes. Source revision {r['hardware']['commit']}.\n\n[Manifest](../../../results/{name}/train.json) · [Epoch log](../../../logs/{name}.jsonl) · [Protocol](../../preregistration.md)")
        write(ex/name/"learnings.md",f"# Observations from {name}\n\n{outcome}\n\n{meaning} Cross-model attribution requires the prespecified paired comparisons. [Aggregated contrasts](../../summary.md)")
        individual.append([f"[{name}]({name}/experiment.md)",*row_metrics(r)[1:]])
    write(ex/"experiments.md","# Experiment index\n\n"+brief+"\n\n"+table(individual,HEADERS)+
          "\n\nThe scene objective is binary cross entropy. The pixel and superpixel objectives are ten-way cross entropy. Each optimizer follows a cosine schedule. The run matrix records the budgets and split choices. Both mates measures the fraction of scene families for which both binary decisions are correct. NMSE divides squared error by total target energy.\n\n[Design and optimizer choices](../planned-runs.md) · [Model details](../../docs/usage.md)\n\n## Independent algebra diagnostics\n\n"+atable)
    if algebra:
        write(ex/"algebra"/"experiment.md","# Algebra diagnostics\n\n"+atable+"\n\n[Raw world measurements](../../../results/algebra/)")
        write(ex/"algebra"/"learnings.md","# Algebra findings\n\n"+algebra_finding(data)+"\n\nThe multiplier and blind bilinear fits isolate coefficient estimation. The neural scene study additionally requires noisy sensor decoding, spatial selection and comparing two objects.\n\n[Measured errors](experiment.md)")
    write(ex/"learnings.md","# Research observations\n\n"+brief+"\n\nThe independent scalar implementation supplies rendering ground truth. Reversing high-basis triples changes coordinate interaction signs while preserving routing, real dimension and the lower subalgebra. An exact multiplier fit tests implementation and identifiability. Generalization of the full scene classifier requires separate held-out predictions.\n\n[Prior methods](../state-of-the-art-review.md) · [Per-run outcomes](experiments.md)")
    write_json(DOCS/"study.json",data)
    by_name={r["name"]:r for r in runs}
    schedule=[]
    for stage in STAGES:
        configs=planned_runs(stage)
        fits=[by_name[c.name] for c in configs if c.name in by_name]
        tested=sum(bool(r["splits"]) for r in fits)
        duration=f"{sum(r['seconds'] for r in fits)/len(fits):.1f} s" if fits else "pending"
        schedule.append([stage,len(configs),len(fits),tested,len(configs)-tested,duration])
    total=sum(s[1] for s in schedule)
    finished=sum(s[3] for s in schedule)
    progress_table=table(schedule,["Stage","Planned","Fitted","Tested","Tests remaining","Mean fit time"])
    write(REPORTS/"progress.md",f"# Study progress\n\nPublic preregistration at [4552d4d]({GH}/commit/4552d4d9bdd1465864d50c9e9bd429631ac2ae2c). "
          f"The reproducible implementation, tests, paper source and explorer accompany the protocol. Completed training manifests: {len(runs)}. Completed neural evaluations: {sum(bool(r['splits']) for r in runs)}. Completed algebra worlds: {len(set(x['seed'] for x in data['algebra']))}.\n\n"+brief+
          f"\n\n{finished} of {total} planned neural evaluations are complete ({percent(finished/total)} by count). "
          "Different datasets require different amounts of compute. Mean fit time covers epoch loops and validation. Data preparation, evaluation and both public releases add wall time.\n\n"+progress_table+
          "\n\nThe matrix resumes at the first unpublished milestone. The live dashboard exposes epoch time and permits an ETA for the current fit. The full schedule depends on the observed runtimes of the largest datasets. [Planned runs](planned-runs.md) · [Experiments](experiments/experiments.md)")
    return brief,groups,decisions,algebra


def report():
    data=collect()
    figures(data)
    brief,groups,decisions,algebra=documents(data)
    from .paper import make_paper
    make_paper(brief,groups,decisions,algebra,data)
    print(f"Regenerated study artifacts for {len(data['runs'])} completed fits.",flush=True)
