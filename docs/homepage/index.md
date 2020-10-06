## Introduction

The need to merge VCD files with `Python` has emerged as feature for the
`pyvcd` project. At the same time there was a need to test the traceability
features in `sltoo`. Hence this project was born.

Usage and installation is described in the *Readme.md* file. In a nutshell:

```bash
pip install pymergevcd
pymergevcd -o merged_out.vcd in1.vcd in2.vcd
```


## Concept

In regulatory environments there's a need for released documents. In this
section we try to document one approach using
*[sltoo](https://www.github.com/kown7/sltoo)* to generate the requirements
specifications.

There's an in-depth discussion in [ReqSecDevOps](reqsecdevops.md).

## Create documents

These documents are regenerated on every push. The `assets/` folder need to be
in the repository, otherwise it's ignored by travis' deploy script.

The documents are versioned by calling git describe over the respective
subfolder, e.g., for the architecture document

```bash
git describe $(git log -n 1 --format=%H -- docs/arch)
```

The idea is to have the equivalent of versioned documents. 

To set a version for a document create an annotated tag, e.g., for version `1A`
of the *software component specification* use `git tag -a SWC-RS/1A`.
Alternatively use the same tags that are used for the release of the software.
This will unfortunately lead to what can seem as outdated documents.

### Requirements

[Requirements specification](assets/requirements/artifacts/specification.pdf).

### Architecture

[Software Architecture](assets/arch/artifacts/specification.pdf).

### Autodoc

TODO

