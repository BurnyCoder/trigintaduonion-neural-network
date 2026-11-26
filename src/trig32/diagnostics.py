"""Independent least-squares diagnostics for parameter estimation and blind bilinear learning."""
import numpy as np
from scipy.linalg import lstsq
from .paths import RESULTS, write_json
from .reference import reference_table,left_matrix,products
from .scenes import filter_vector


def nmse(target,pred):
    return float(np.square(target-pred).sum()/np.square(target).sum())


def fit(a,b):
    """Minimum-norm fits; QR with pivoting permits underdetermined inputs."""
    return lstsq(a,b,lapack_driver="gelsy",check_finite=False)[0]


def diagnostics(seeds):
    records=[]
    for seed in seeds:
        rng=np.random.default_rng(np.random.SeedSequence([seed,501]))
        w=filter_vector(seed).astype(float)
        inputs=rng.normal(size=(128,32))
        test=rng.normal(size=(512,32))
        tables={r:reference_table(r,seed) for r in ("cd32","random")}
        for teacher,table in tables.items():
            train_y=inputs@left_matrix(w,table).T
            test_y=test@left_matrix(w,table).T
            for n in (2,8,32,128):
                for learner in ("cd32","random","real"):
                    if learner=="real":
                        pred=test@fit(inputs[:n],train_y[:n])
                    else:
                        matrices=np.stack([left_matrix(e,tables[learner]) for e in np.eye(32)])
                        design=np.einsum("wij,bj->biw",matrices,inputs[:n])
                        coeff=fit(design.reshape(-1,32),train_y[:n].ravel())
                        pred=test@left_matrix(coeff,tables[learner]).T
                    records.append(dict(task="multiplier",seed=seed,teacher=teacher,model=learner,
                                        n=n,nmse=nmse(test_y,pred)))
        a,b=rng.normal(size=(2,2048,32))
        aa,bb=rng.normal(size=(2,512,32))
        y=products(a,b,tables["cd32"])
        yy=products(aa,bb,tables["cd32"])
        features=(a[:,:,None]*b[:,None,:]).reshape(2048,1024)
        query=(aa[:,:,None]*bb[:,None,:]).reshape(512,1024)
        basis=products(np.eye(32)[:,None,:],np.eye(32)[None,:,:],tables["cd32"]).reshape(1024,32)
        ordidx=np.arange(1024)
        k=abs(basis).argmax(1)
        for n in (256,1024,2048):
            permutation=rng.permutation(n)
            target=np.concatenate((y[:n],y[:n][permutation]),axis=1)
            params=fit(features[:n],target)
            for model,p in zip(("bilinear","shuffled"),np.hsplit(params,2)):
                ix=abs(p).argmax(1)
                correct=(ix==k)&(np.sign(p[ordidx,ix])==basis[ordidx,k])
                records.append(dict(task="product",seed=seed,model=model,n=n,
                                    nmse=nmse(yy,query@p),basis_correct=int(correct.sum())))
                # The fitted tensor is directly loadable as a PyTorch Bilinear weight.
                from .paths import CHECKPOINTS
                from safetensors.numpy import save_file
                folder=CHECKPOINTS/f"product-{model}-s{seed}-n{n}"
                folder.mkdir(parents=True,exist_ok=True)
                save_file({"weight":np.ascontiguousarray(p.T.reshape(32,32,32))},str(folder/"model.safetensors"))
        records.append(dict(task="product",seed=seed,model="analytic",n=0,nmse=0.,basis_correct=len(basis)))
        write_json(RESULTS/"algebra"/f"seed-{seed}.json",[row for row in records if row["seed"]==seed])
    return records
