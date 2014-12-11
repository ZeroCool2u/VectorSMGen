VectorSMGen
===========
Author: @theocoyne

Shoutout to the beautiful people over at http://www.snowball.tartarus.org/

A small python program to visually compare normalized vector representations of Presidential speeches. The dataset format for this version is currently 4 speeches per speaker, to give you an averaged speech vector in the form of a dotproduct. You will encounter serious errors if your dataset is not in the correct format of 4 speeches per speaker.

VectorSMGen was built with the miniconda interpreter. If you'd like to run VSMG as is, it is reccomended you install miniconda as the easiest method of dependency resolution. Running VSMG neccesitates the 'files.py' file be in the same directory as the 'Presidents.py' file. 

Installation Guide:

1. Install miniconda: http://conda.pydata.org/miniconda.html

2. Install setuptools module by running 'conda install setuptools' from the commandline in minicondas your miniconda directory. 

3. Install the package manager pip by running 'conda install pip'.

4. Install the pure python implementation of the snowball stemmer 'pip install stemming'.

5. You're now ready to run Presidents.py!

Thanks for checking out the project!
