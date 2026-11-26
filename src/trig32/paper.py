"""Typeset the paper from exactly the records used for the README and explorer."""
from datetime import date
import os
from pathlib import Path
import shutil
import subprocess

from .paths import ROOT

SOURCES=[
    ("Biss, Dugger and Isaksen. Large annihilators in Cayley--Dickson algebras. Definition 2.1.","https://arxiv.org/abs/math/0511691"),
    ("Saniga et al. Cayley--Dickson algebras and finite geometry.","https://arxiv.org/abs/1405.6888"),
    ("LeCun et al. Gradient-based learning applied to document recognition.","https://leon.bottou.org/papers/lecun-98h"),
    ("He et al. Deep residual learning for image recognition.","https://arxiv.org/abs/1512.03385"),
    ("Trabelsi et al. Deep complex networks.","https://arxiv.org/abs/1705.09792"),
    ("Gaudet and Maida. Deep quaternion networks.","https://arxiv.org/abs/1712.04604"),
    ("Wu et al. Deep octonion networks.","https://arxiv.org/abs/1903.08478"),
    ("Bojesomo, Liatsis and Al Marzouqi. Traffic flow prediction using Deep Sedenion Networks.","https://arxiv.org/abs/2012.03874"),
    ("Saoud and Al-Marzouqi. Metacognitive Sedenion-Valued Neural Network and its Learning Algorithm.","https://doi.org/10.1109/ACCESS.2020.3014690"),
    ("Johnson et al. CLEVR. A diagnostic dataset for compositional language and elementary visual reasoning.","https://cs.stanford.edu/people/jcjohns/clevr/"),
    ("Gilmer et al. Neural message passing for quantum chemistry.","https://proceedings.mlr.press/v70/gilmer17a.html"),
    ("Satorras et al. E(n) equivariant graph neural networks.","https://proceedings.mlr.press/v139/satorras21a.html"),
    ("Dwivedi et al. Benchmarking graph neural networks.","https://www.jmlr.org/papers/v24/22-0567.html"),
    ("Barz and Denzler. Do we train on test data? ciFAIR data and code.","https://cvjena.github.io/cifair/"),
    ("Cayley--Dickson scalar reference, pinned implementation.","https://github.com/discretegames/hypercomplex/tree/d026ee205a4bf41f93b5c67df17e212ca3be5de2"),
    ("Preregistration and versioned analysis protocol.","https://github.com/BurnyCoder/trigintaduonion-neural-network/blob/4552d4d/reports/preregistration.md"),
]


def esc(x):
    return "".join({"%":r"\%","_":r"\_","&":r"\&","#":r"\#","—":"---","−":"$-$","–":"--"}.get(c,c) for c in str(x))


def tabular(head,rows,spec):
    return (r"\begin{longtable}{"+spec+"}\n"+r"\hline " + " & ".join(esc(x) for x in head)+
            r"\\\hline\endhead"+"\n"+"\n".join(" & ".join(esc(x) for x in row)+r"\\" for row in rows)+
            "\n"+r"\hline\end{longtable}"+"\n")


def plot(file,caption):
    if not (ROOT/"docs"/"figures"/(file+".png")).exists():
        return ""
    return (r"\begin{center}\includegraphics[width=.94\linewidth,height=.29\textheight,keepaspectratio]{docs/figures/"+file+
            ".png}\n"+r"\\{\small "+esc(caption)+r"}\end{center}"+"\n")


def make_paper(brief,groups,decisions,algebra,data):
    directory=ROOT/"reports"
    header=r"""\documentclass[10pt]{article}
\usepackage[margin=0.8in]{geometry}
\usepackage{graphicx,longtable,hyperref}
\hypersetup{colorlinks=true,urlcolor=blue,linkcolor=black,pdfauthor={Libor Burny Burian}}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}\setlength{\emergencystretch}{3em}
\title{Can a 32-component algebra help a neural network compare spatially selected objects?}
\author{Libor \textquotedblleft Burny\textquotedblright\ Burian}
\date{DATE}
\begin{document}\maketitle
\begin{abstract}
A noisy sensor observes one component of an unknown linear mixing of an object's excitation. A graph neural network must identify two objects through intermediary landmarks and predict whether they have the same hidden type. We cross the multiplication rule used by the sensor with the rule used to tie neural weights. This synthetic intervention measures whether compatible weight sharing improves end-to-end decisions. OUTCOME
\end{abstract}
\section{Motivation and related work}
Spatial structure can restrict which interactions a model must learn. Relational scene benchmarks [10], message passing [11] and distance-conditioned equivariant networks [12] motivate our scene generator and graph processor. We study a second, independent assumption about which observable channels share parameters. Real convolutional and residual networks [3,4], complex [5], quaternion [6], octonion [7] and sedenion networks [8,9] establish precedents for the smaller component counts. Our contribution is the combination of a 32-component trainable graph classifier, paired counterfactual scenes and a crossover intervention. We make no priority claim for 32-component neural layers.
\section{Method}
Starting with real scalars, double five times using
\[
 (a,b)(c,d)=(ac-\bar d b,\;da+b\bar c).
\]
For basis elements $e_i e_j=s_{ij}e_{i\oplus j}$, a learned left multiplier maps $x$ to $y_k=\sum_j s_{k\oplus j,j}w_{k\oplus j}x_j$ [1,2]. One block of 32 real trainable scalars supplies all entries of a $32\times32$ matrix. Ordinary tensor contraction computes that matrix on the accelerator. Each layer has explicit operand order. This construction needs neither associativity nor a multiplicative inverse. Five doublings do not imply five-dimensional spatial equivariance.
 
Each world draws a unit filter $w$ with zero scalar component and equal squared energy in the lower and upper halves. For object type $b\in\{-1,+1\}$, Gaussian excitation $x$ and index $k$, the observed scalar is $z=b(w\star x)_k+\epsilon$, with $\epsilon\sim N(0,0.1^2)$. The canonical sensor uses an independent scalar implementation [15]. The random sensor flips all six signs of 60 uniformly sampled upper basis triples while preserving the ordered-product support, the identity, the imaginary squares, and the lower 16-component table. The randomized rule is a signed bilinear control.

Draw two beacons, four landmarks and eight objects uniformly in the plane. Reject layouts with coinciding nearest choices or a nearest/second-nearest distance margin of at most 0.035 at a selected hop. Half the objects have each type. From each beacon follow its nearest landmark and then its nearest object. Equality of the two object types is the binary target. Swapping the entire reading of a selected object with an opposite-type distractor flips the answer. Full families stay within the same split. An order-independent readings-only predictor or geometry-only predictor makes exactly one correct decision per family.

The encoder mixes the excitation with four learned channel projections, reads each at the observed coordinate and supplies the projections, their products with $z$, and $z$ to a nonlinear MLP. A landmark pools object features and a beacon pools landmark features using a learned function of squared distance plus a learned negative distance slope. Signed linear residual updates transform the pooled features. A real MLP reads the sum and elementwise product of both beacon embeddings. Using distances and symmetric aggregates makes the full prediction invariant to a common planar isometry and within-role index permutations.
"""
    text=header.replace("DATE",date.today().strftime("%d %B %Y")).replace("OUTCOME",esc(brief))
    text+=plot("architecture","Figure 1. End-to-end classifier. Object types and selection indices are withheld from the learner.")
    text+=r"""
\section{Experiment and falsification criteria}
Each primary world has 1,024 training, 256 validation and 1,024 test families. Withhold sensor coordinates 12--15 and 28--31 during training. Evaluate fresh scenes with these coordinates and scenes with 16 objects separately. Both matched and mismatched networks receive identical underlying geometry, labels, excitations, noise and optimizer settings. Fit 80 epochs of AdamW, initial learning rate 0.003, weight decay 0.0001, batch size 128 scenes and cosine decay. Break ties in maximum validation accuracy in favor of the earliest epoch. A frozen random encoder with trained readout, one-hop network, shallow coordinate-aware set network, unrestricted real, low-rank real and sedenion learners control different aspects of the architecture.

Seed 42 is a development pilot. Compute two-sided 95\% Student intervals over paired differences from eight independent confirmatory worlds. A matched learner must have a lower bound above 60\% for task success. Both directional crossover lower bounds must exceed one percentage point for a matching claim. Both depth comparisons must have positive lower bounds for the multistage attribution. Incomplete seed sets defer decisions [16]. Data-size sensitivity and the individual controls are descriptive. Multiple testing, resource limits and optimization sensitivity constrain interpretation.

Auxiliary multiplier and unrestricted bilinear least-squares fits test algebraic recovery. Separate transfer experiments compare structured residual image classifiers on CIFAR-10 and its duplicate-corrected ciFAIR-10 test set [4,14]. Superpixel classification uses the published split [13] with a learned color input and a graph-mean readout. The simulator supplies no sensor rule for natural images. The registered transfer contrast evaluates canonical versus randomized sharing on ciFAIR-10.
\section{Results and claims}
"""+esc(brief)+"\n"
    if groups:
        text+=tabular(["Task / model / rule","Worlds","Params","Test","95% interval"],groups,r"p{.43\linewidth}rrrr")
    text+=tabular(["Endpoint","N","Estimate","95% interval","Decision"],[[r[0],r[1],r[2],r[3],r[5]] for r in decisions],r"p{.37\linewidth}rp{.11\linewidth}p{.17\linewidth}l")
    text+=plot("scores","Each dot is a held-out world. The vertical tick denotes its group's arithmetic mean.")
    text+=plot("learning","Pilot binary cross entropy and accuracy by epoch, from the timestamped training log.")
    text+=plot("example","A fixed held-out family. Circles show object readings, square markers landmarks and stars beacons. Dashed paths show ground-truth selections.")
    text+=plot("predictions","Same-type probabilities and binary controls on three fixed held-out families from the lowest available evaluated seed in the canonical sensor condition.")
    if data["audits"]:
        text+=r"\subsection*{Supplementary fixed-checkpoint interventions}"+"\n"
        for a in data["audits"]:
            if "interventions" in a:
                iso=a["interventions"]["isometry_and_reindexing"]
                broken=a["interventions"]["broken_correspondence"]
                text+=esc(f"{a['run']}. A common orthogonal transformation, translation and node reordering changed {iso['changed_decisions']} of {iso['examples']} decisions. Cyclically shifting sensor payloads among objects changed {broken['changed_decisions']} decisions and gave {100*broken['accuracy_against_original_labels']:.2f}% accuracy against the original labels. This supplementary probe was specified after the pilot evaluation.")+"\n"
    if algebra:
        text+=r"\subsection*{Independent algebra diagnostic}"+"\n"+tabular(["Task","Teacher","Learner","N","Worlds","NMSE","Basis"],algebra,"lllrrrr")
    text+=r"""
\section{Discussion, limitations and conclusion}
A successful crossover identifies an effect of matching the assumed interaction rule to this simulator under this training recipe. The treatment changes the tied matrices throughout the encoder and message blocks, so a net effect alone does not localize the mechanism. Scene families share a world-specific filter, and evaluation addresses fresh scenes within each trained world. The task supplies object segmentation, roles and coordinates. Natural images require separate transfer evidence. The factorization and sample count of the real controls affect representational capacity and optimization. The privileged oracle knows the measurement filter and nearest paths. Noise makes even its decisions fallible. Diagnostic product recovery and gradients alone cannot establish that a scene classifier learned the task.

\section*{Appendix: replication and evidence}
The public repository contains the full seed matrix, pinned environment, checkpoint configurations, training and validation logs, individual test predictions, both mates of fixed example families, and regeneration code as runs are published. To regenerate this paper and every table and figure, run \texttt{uv run trig32 report} at the repository root. See the \href{https://github.com/BurnyCoder/trigintaduonion-neural-network}{source and run guide} and \href{https://burnycoder.github.io/trigintaduonion-neural-network/}{interactive explorer}.
\section*{References}
\begin{enumerate}\setlength{\itemsep}{1pt}
"""
    text+="\n".join(r"\item \href{"+url+"}{"+esc(name)+"}" for name,url in SOURCES)
    text+=r"""
\end{enumerate}
\section*{AI statement}
Codex wrote this codebase and paper. A human provided the exact specification that Codex executed. Human cleanup and rewriting are in progress.
\end{document}
"""
    source=directory/"paper.tex"
    source.write_text(text,encoding="utf-8")
    scratch=ROOT/".work"/"paper"
    scratch.mkdir(parents=True,exist_ok=True)
    compiler=shutil.which("pdflatex")
    if compiler:
        cmd=[compiler,"-interaction=nonstopmode","-halt-on-error","-output-directory",str(scratch),str(source)]
    else:
        cmd=["tectonic","--outdir",str(scratch),str(source)]
    env={**os.environ,"TEXINPUTS":str(ROOT)+os.pathsep+str(directory)+os.pathsep}
    # Keep compiler diagnostics available without flooding epoch logs.
    proc=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,timeout=180)
    (scratch/"engine.log").write_bytes(proc.stdout+proc.stderr)
    if proc.returncode:
        raise RuntimeError(f"paper build failed, see {scratch/'engine.log'}")
    shutil.copyfile(scratch/"paper.pdf",directory/"paper.pdf")
