##############################################
#                                            #
# Common utilities for managing Kraken jobs. #
#                                            #
##############################################

# Maaaaaassiff import stack
import os
import sys
import shutil
import os.path
from glob import glob
from typing import List
from pathlib import Path
from contextlib import suppress
from multiprocessing import Pool
from subprocess import run, PIPE
import yaml

config_path = Path(__file__).resolve().parent / 'config.yaml'
with open(config_path) as f:
	config = yaml.safe_load(f)


main_kraken_dir    = Path(config["main_kraken_dir"])
dft_results_dir    = Path(config["dft_results_dir"])
selected_confs_dir = Path(config["selected_confs_dir"])
input = Path(config["input_file"])
tobi_path = Path(config["tobi"])
sub_script_folder = Path(config["sub_script_folder"])
gsub = Path(config["gsub"])
selected_confs_dir = Path(config["selected_confs_dir"])
pint = Path(config["Pint"])
ded_path = Path(config["ded"])
multiwfn_path = Path(config["multiwfn_path"])
dftd3 = Path(config["dftd3_path"]) #got errors with conda/pip install dftd3, ergo this.


def ligands_from_file(fname: str) -> List[str]:
	"""
	Load a list of ligands from file.
	"""
	with open(fname, 'r') as f:
		return [line.strip().zfill(8) for line in f.readlines()]


def conformers_from_folder(folder: str) -> List[str]:
	"""
	Load a list of conformers from a folder of Gaussian input files.
	"""
	return [fname.rstrip('.com') for fname in os.listdir(folder)]


def ligands_from_conformers(conformers: List[str]) -> List[str]:
	"""
	Extract the ligands from a list of conformers.
	"""
	return [conformer.split('_')[0] for conformer in conformers]


def unzip(ligand: str) -> None:
	"""
	Unzip ligand dir, if zip exists but folder does not.
	"""
	if not os.path.isdir(ligand):
		run(['unzip', f"{ligand}.zip"])
	with suppress(FileNotFoundError):
		os.remove(f"{ligand}.zip")


def ligand_stragglers() -> List[str]:
	"""
	Determine the ligands that are present in the selected conformers directory,
	but that do not have dft results computed.
	"""

	# Determine the lists of ligands
	select_list = [file for file in os.listdir(selected_confs_dir) if file[0] == '0']
	dft_list    = [file for file in os.listdir(dft_results_dir)    if file[0] == '0']

	# Isolate the IDs
	select_ids = set([name.split('_')[0].split('.')[0] for name in select_list])
	dft_ids    = set([name.split('_')[0].split('.')[0] for name in dft_list])

	# Return the stragglers
	print(f"Selected confs: {len(select_ids)}")
	print(f"DFT results:    {len(dft_ids)}")

	return list(sorted(select_ids - dft_ids))
