#!/bin/bash

# 1. Aislamos el hilo y configuramos el path desde el script
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export PYTHONPATH=.

# 2. Capturamos la ruta exacta del Python de tu entorno virtual activo
VENV_PYTHON=$(which python)

# 3. Lanzamos srun usando esa ruta absoluta
srun -p compute -w m08-19 --ntasks=1 --cpus-per-task=1 --mem=2G $VENV_PYTHON -m src.tests.algorithms.test_layer_filler_rts