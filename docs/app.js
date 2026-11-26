/* Render only published records. A local dashboard additionally supplies live epoch snapshots. */
const el = id => document.getElementById(id);
const pct = n => n == null ? "—" : (100*n).toFixed(2)+"%";
const pp = n => n == null ? "—" : (100*n).toFixed(2)+" pp";
let study, current;
function cells(parent, values) {
  const tr=document.createElement("tr");
  for (const value of values) { const td=document.createElement("td"); td.textContent=value; tr.append(td); }
  parent.append(tr);
}
function surface(id) {
  const canvas=el(id), w=canvas.clientWidth, h=canvas.clientHeight, scale=window.devicePixelRatio || 1;
  canvas.width=w*scale; canvas.height=h*scale;
  const c=canvas.getContext("2d"); c.scale(scale,scale); c.font="11px system-ui"; return [c,w,h];
}
function curve() {
  const [c,w,h]=surface("curve"), key=el("metric").value, ev=current.curve;
  if (!ev.length) return;
  const max=key==="accuracy"?1:Math.max(.001,...ev.flatMap(e=>[e.train_loss,e.val_loss]))*1.03;
  const x=i=>36+(w-49)*i/Math.max(1,ev.length-1), y=v=>h-27-(h-47)*v/max;
  for(let i=0;i<5;i++){
    const v=i*max/4; c.strokeStyle="#dce4e1"; c.beginPath(); c.moveTo(32,y(v)); c.lineTo(w-10,y(v)); c.stroke();
    c.fillStyle="#405c63"; c.fillText(key==="accuracy"?Math.round(100*v)+"%":v.toFixed(2),0,y(v)+3);
  }
  for(const [split,color] of [["train","#147d7a"],["val","#b36422"]]){
    c.strokeStyle=color; c.lineWidth=2; c.beginPath();
    ev.forEach((e,i)=>{const a=x(i),b=y(e[split+"_"+key]); if(i===0)c.moveTo(a,b); else c.lineTo(a,b);});c.stroke();
  }
  c.fillText("Epoch "+ev[0].epoch,32,h-5);c.fillText(String(ev.at(-1).epoch),w-26,h-5);
}
function scene() {
  if(!current.examples) return;
  const [c,w,h]=surface("scene"), f=current.examples, first=Number(el("family").value)*2;
  const size=Math.min(w/2-12,h-34);
  for(let j=0;j<2;j++){
    const i=first+j,left=j*w/2+(w/2-size)/2,top=18, xy=p=>[left+p[0]*size,top+(1-p[1])*size];
    c.strokeStyle="#cedbd7";c.strokeRect(left,top,size,size);
    const nearest=(p,arr)=>arr.reduce((a,b)=>Math.hypot(p[0]-a[0],p[1]-a[1])<Math.hypot(p[0]-b[0],p[1]-b[1])?a:b);
    for(const p of f.beacon[i]){const q=nearest(p,f.land[i]), t=nearest(q,f.pos[i]);c.setLineDash([3,3]);c.strokeStyle="#708687";
      c.beginPath();c.moveTo(...xy(p));c.lineTo(...xy(q));c.lineTo(...xy(t));c.stroke();c.setLineDash([]);}
    f.pos[i].forEach((p,k)=>{const z=f.z[i][k];c.fillStyle=z>0?"#ba512f":"#3f72a6";c.globalAlpha=.35+Math.min(.65,Math.abs(z)/2);
      c.beginPath();c.arc(...xy(p),4,0,Math.PI*2);c.fill();});c.globalAlpha=1;
    for(const p of f.land[i]){const [x,y]=xy(p);c.fillStyle="#117c70";c.fillRect(x-3,y-3,6,6);}
    for(const p of f.beacon[i]){const [x,y]=xy(p);c.save();c.translate(x,y);c.rotate(Math.PI/4);c.fillStyle="#835e21";c.fillRect(-4,-4,8,8);c.restore();}
    c.fillStyle="#17333d";c.fillText(j?"Swapped":"Original",left,top-5);
  }
  const answer=i=>(f.labels[i]?"same":"different")+" · P(same) "+f.scores[i].toFixed(3);
  el("answers").textContent="Ground truth and model output — original: "+answer(first)+"; swapped: "+answer(first+1)+".";
}
function show() {
  current=study.runs[Number(el("run").value)]; if(!current) return;
  el("detail").hidden=false;el("empty").hidden=true;el("metrics").replaceChildren();
  const test=current.splits.test || {};
  for(const [k,v] of [["Validation",pct(current.val_accuracy)],["Test",pct(test.accuracy)],["Both mates",pct(test.both_correct)],["Oracle",pct(test.oracle_accuracy)],["Trainable weights",current.trainable.toLocaleString()]]){
    if(v==="—") continue;const box=document.createElement("span"), strong=document.createElement("strong");strong.textContent=v;box.append(strong,k);el("metrics").append(box);
  }
  el("scene-panel").hidden=!current.examples;curve();scene();
}
async function live(){
  if(!["localhost","127.0.0.1","::1"].includes(location.hostname))return;
  try {const response=await fetch("/live.json",{cache:"no-store"});if(!response.ok)return;
    const e=await response.json();if(!e.epoch)return;
    el("live").hidden=false;el("live-title").textContent=e.finished?"Latest completed training":"Training now";
    el("live-status").textContent=e.run+" · epoch "+e.epoch+" of "+e.epochs+" · "+e.time;
    el("epoch-progress").max=e.epochs;el("epoch-progress").value=e.epoch;
    el("live-values").textContent="Train "+pct(e.train_accuracy)+"   ·   Validation "+pct(e.val_accuracy)+"   ·   Loss "+e.val_loss.toFixed(4)+"   ·   "+e.epoch_seconds.toFixed(1)+" s/epoch";
  }catch{ /* Local live endpoint may be starting. Published runs remain available. */ }
}
async function start(){
  const response=await fetch("study.json",{cache:"no-cache"});if(!response.ok)throw Error("data unavailable");study=await response.json();
  for(const [i,r] of study.contrasts.entries()){const fmt=i<2?pct:pp;cells(el("contrasts"),[r.title,r.n,fmt(r.mean),r.lo==null?"—":fmt(r.lo)+" to "+fmt(r.hi),r.decision]);}
  for(const [i,r] of study.runs.entries()){el("run").add(new Option(r.name,String(i)));}
  if(study.runs.length){const p=study.runs.findIndex(r=>r.config.seed===42);el("run").value=String(Math.max(0,p));show();}
  else{el("empty").textContent="Checkpoint results will appear here after the first fit.";el("run").disabled=true;}
  if(study.algebra.length){el("diagnostics").hidden=false;study.algebra.forEach(r=>cells(el("algebra"),[r.task,r.teacher||"cd32",r.model,r.seed,r.n,r.nmse.toExponential(3)]));}
  el("run").onchange=show;el("family").onchange=scene;el("metric").onchange=curve;
  window.addEventListener("resize",()=>{if(current){curve();scene();}});
}
start().catch(e=>{el("empty").textContent="Unable to load research data. Refresh to try again.";});
live();setInterval(live,5000);
