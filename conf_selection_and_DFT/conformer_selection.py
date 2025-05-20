#################################################
#                                               #
# Perform conformer selection of crest results  #
# to prepare for DFT runs.                      #
#                                               #
#################################################

from utils import *
import PL_conformer_selection_200411 as PLcs
from datetime import datetime

if __name__ == '__main__':
	print("Script started at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	print("Current working directory:", os.getcwd())
	# Retrieve the list of ligands to run
	
	ligands = ligands_from_file(input) 

	# Run the conformer selection
	with Pool() as p:
		p.map(PLcs.conformer_selection_main, ligands)
