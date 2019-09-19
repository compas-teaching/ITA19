# ITA PhD course

*Computational research with COMPAS*

## Description

The PhD-level course (primarily for A&T PhDs) will introduce computational methods for architecture engineering, fabrication & construction, incentivising computational literacy. Students learn the theoretical background and basic implementation details of fundamental data structures and algorithms, and to solve real-world problems using the COMPAS framework and other open-source libraries.

## Learning objectives

* understand the scope and relevance of computational methods for architecture and engineering research and practice,
* the theoretical background of fundamental data structures, 
* the basic principles of algorithmic design; 
* implement basic versions of prevalent algorithms related to architectural geometry, structural design, robotic assembly, volumetric modeling & 3D-printing, high-performance computation; 
* use sophisticated algorithms available through open-source libraries to solve real-world problems; and, 
* use common CAD tools as interfaces to self-implemented solutions.

## Overview

Course will consist of a few lectures, several tutorials and project-based exercises.

Topics will include:

* Intro Python programming
* Intro COMPAS open-source framework (https://compas-dev.github.io/) 
* Intro to geometry processing, data structures, topology, numerical computation
* Domain-specific case studies (e.g. on architectural geometry, structural design, robotic assembly, volumetric modeling and 3D printing, high performance computation)

## Schedule

Week | Date | Lead | Title | Description
---- | ---- | ---- | ----- | ---
1 | Oct 2 | BRG | COMPAS intro | Overview of ecosystem (core & packages).<br />Why should you care?<br />Tools intro.
|||| *Assignment:* Install COMPAS and run checks.
2 | Oct 9 | BRG/GKR | COMPAS examples | COMPAS examples covering all course topics and use cases.
|||| *Assignment:* Make incremental changes to the examples.
3 | Oct 16 | BRG | Data structures and (architectural) geometry | Graph theory, Half-edge data structure, OABB, PCA, Mesh algorithms, ...
|||| *Assignment:* ???
4 | Oct 23 | BRG | Module 1: Structural design | **Theory:** Graphic statics (`compas_ags`, `compas_tna`, `compas_3gs`), Form finding (`compas_fofin`), Finite Element Analysis (`compas_fea`), ...
|||| *Assignment:* ???
5 | Oct 30 | BRG | Module 1: Structural design | **Case study:** Cablenet-and-fabric formwork (HiLo)
|||| *Assignment:* ???
6 | Nov 6 | GKR | Module 2: Robotic assembly | **Theory:** Robotic fabrication planning (`compas_fab`)
|||| *Assignment:* ???
7 | Nov 13 | GKR | Module 2: Robotic assembly | **Case study:** The undulating wall
|||| *Assignment:* ???
8 | Nov 20 | DBT | Module 3: Volumetric modeling | **Theory:** geometry representation, history of display technology, 2D: raster vs. vector, boundary representation (BRep) vs. function representation (FRep), scalar fields, signed distance functions, oop: primitives, combinations, modifications
|||| *Assignment:* model an everyday object (e.g. coffee cup)
9 | Nov 27 | DBT | Module 3: Volumetric modeling | **Case study:** infrastructure integration, internal voids, complex topologies, lattice structures for weight reduction
|||| *Assignment:* Smart Brick
10 | Dec 4 | All | Use COMPAS in research | Make your own package, Best practices, COMPAS projects, COMPAS PhD packages, ...



## Jupyter and extensions

If you have Anaconda installed, then jupyter is already installed. If not, then install jupyter with pip.

To run the jupyter notebook, you simply have to type:

	jupyter notebook

in your command line.

### Configure workspace

To configure the workspace, type

	jupyter notebook --generate-config

This writes a default configuration file into: 
	
`$HOMEPATH$\.jupyter\jupyter_notebook_config.py` (on windows)

or

`~\.jupyter\jupyter_notebook_config.py` (on mac)

If you want jupyter to open in a different directory, then change the following line:

	c.NotebookApp.notebook_dir = 'YOUR_PREFERRED_PATH'

### Download nbextensions

To install nbextensions, execute the commands below in Anaconda Prompt:

	conda install -c conda-forge jupyter_contrib_nbextensions
	conda install -c conda-forge jupyter_nbextensions_configurator

After installing, restart the Jupyter notebook, and you can observe a new tab Nbextensions added to the menu.
Install the following extensions:

1. Split Cells Notebook - Enable split cells in Jupyter notebooks

2. RISE - allows you to instantly turn your Jupyter Notebooks into a slideshow. 

