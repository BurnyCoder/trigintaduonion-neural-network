"""Animate the first held-out pilot family directly from its saved neural predictions."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory
import warnings

import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
import numpy as np

from .paths import ROOT, atomic_replace


def exchanged_objects(before, after):
    """Require two readings to have traded positions before displaying motion."""
    changed = np.flatnonzero(np.asarray(before) != np.asarray(after))
    if len(changed) != 2 or not np.array_equal(np.asarray(before)[changed], np.asarray(after)[changed[::-1]]):
        raise ValueError("the displayed family must exchange exactly two complete readings")
    return tuple(map(int, changed))


def swap_video(examples, directory):
    """Write a silent MP4 and poster. The network scores only the two measured endpoints."""
    movie, poster = directory/"reading-swap.mp4", directory/"reading-swap.png"
    if examples is None or shutil.which("ffmpeg") is None:
        movie.unlink(missing_ok=True)
        poster.unlink(missing_ok=True)
        return
    pair = {k: examples[k][:2] for k in ("pos","beacon","land","z","labels","scores")}
    if pair["labels"][0] == pair["labels"][1] or any(not np.array_equal(*pair[k]) for k in ("pos","beacon","land")):
        raise ValueError("the displayed family must share its geometry and have opposite labels")
    digest = hashlib.sha256(Path(__file__).read_bytes() + json.dumps(pair).encode()).hexdigest()
    scratch = ROOT/".work"
    scratch.mkdir(exist_ok=True)
    stamp = scratch/"reading-swap.sha256"
    if movie.exists() and poster.exists() and stamp.exists() and stamp.read_text() == digest:
        return

    swapped = list(exchanged_objects(*pair["z"]))
    objects, beacons, lands = (np.array(pair[k][0]) for k in ("pos","beacon","land"))
    fig, (space, notes) = plt.subplots(1,2,figsize=(7.6,3.8),gridspec_kw={"width_ratios":[1.1,1]})
    fig.subplots_adjust(left=.055,right=.98,bottom=.15,top=.9,wspace=.18)
    ink, teal, amber = "#183946", "#147d7a", "#ba6c20"
    space.set(xlim=(0,1),ylim=(0,1),aspect="equal",xticks=[],yticks=[])
    space.set_title("Scene geometry",loc="left",color=ink,weight="bold")
    space.set_facecolor("#f6f9f8")
    for beacon in beacons:
        land = lands[np.linalg.norm(lands-beacon,axis=1).argmin()]
        selected = objects[np.linalg.norm(objects-land,axis=1).argmin()]
        space.plot(*np.stack((beacon,land,selected)).T, "--", color="#789195", lw=1.3, zorder=1)
        space.scatter(*selected,s=185,facecolors="none",edgecolors=ink,lw=1.1,zorder=2)
    space.scatter(*objects.T,s=35,color="#b8c6c7",edgecolors=ink,lw=.5,label="object")
    space.scatter(*lands.T,s=50,marker="s",color=teal,label="landmark",zorder=4)
    space.scatter(*beacons.T,s=110,marker="*",color=ink,label="beacon",zorder=4)
    space.legend(loc="upper center",bbox_to_anchor=(.5,-.035),ncol=3,fontsize=7.6,frameon=False)
    markers = space.scatter(*objects[swapped].T,s=80,c=[amber,"#456bb2"],edgecolors="white",lw=1,zorder=5)

    notes.axis("off")
    notes.set(xlim=(0,1),ylim=(0,1))
    notes.text(0,.94,"Exchanging two readings",fontsize=13.5,color=ink,weight="bold")
    notes.text(0,.75,"Gold and blue track the exchanged readings.\nRings mark the two selected objects.",
               fontsize=9.4,color=ink,linespacing=1.5)
    for i, y in enumerate((.58,.27)):
        relation = "same type" if pair["labels"][i] else "different types"
        p = pair["scores"][i]
        probability = "< 0.001" if p < .001 else f"{p:.3f}"
        notes.text(0,y,"After exchange" if i else "Original",color=teal,weight="bold",fontsize=10)
        notes.text(0,y-.12,f"Truth   {relation}\nModel P(same)   {probability}",color=ink,fontsize=9.5,linespacing=1.45)
    phase = notes.text(0,-.055,"",fontsize=9.5,color=ink,weight="bold")
    first, last = objects[swapped], objects[swapped[::-1]]
    direction = first[1]-first[0]
    bend = np.array([-direction[1],direction[0]])*.18
    stages = np.r_[np.zeros(13), np.linspace(0,1,24)[1:-1], np.ones(17)]
    # Stream actual Matplotlib frames to the encoder: https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FFMpegWriter.html
    writer = FFMpegWriter(fps=12,codec="libx264",extra_args=["-pix_fmt","yuv420p","-crf","19","-threads","1","-movflags","+faststart"])
    try:
        with TemporaryDirectory(dir=scratch) as temporary:
            path = Path(temporary)
            with writer.saving(fig,str(path/movie.name),dpi=120):
                for index, t in enumerate(stages):
                    position = first*(1-t) + last*t + np.sin(np.pi*t)*np.stack((bend,-bend))
                    markers.set_offsets(position)
                    phase.set_text("Original scene" if t == 0 else "Counterfactual scene" if t == 1 else "Moving the reading bundles")
                    if index == 0:
                        fig.savefig(path/poster.name,dpi=120)
                    writer.grab_frame()
            atomic_replace(path/movie.name,movie)
            atomic_replace(path/poster.name,poster)
        stamp.write_text(digest)
    except (BrokenPipeError, subprocess.CalledProcessError) as error:
        movie.unlink(missing_ok=True)
        poster.unlink(missing_ok=True)
        warnings.warn(f"FFmpeg could not encode the optional reading-swap movie: {error}", RuntimeWarning)
    finally:
        plt.close(fig)
