#!/usr/bin/python3
# -*- coding: utf-8 -*-
# batch example
# Author: Pierre Martinon
# Inria Paris and LJLL Jussieu
# 2019
# NB. this script is NOT compliant with Python 2 syntax !

# Call: python3 batch.py [outputfolder]

import os
import shutil
import subprocess
import sys

import BocopUtils as bocop
import numpy as np

#-----------------------------------------------------------------------
# Main script
#-----------------------------------------------------------------------
if len(sys.argv) == 1:
  output_prefix = 'batch'
else:
  output_prefix = sys.argv[1]
fnull = open(os.devnull, 'w')

# set and clear output folder
output_path = output_prefix
print('Optimization batch saved in '+output_path+'/')
if os.path.exists(output_path):
  shutil.rmtree(output_path, ignore_errors=True)
os.mkdir(output_path)

# values for constraint limit C
c_list = np.linspace(1,0.5,num=5)

# solve sequence of problems
resultfile = open(output_path+'/results.txt','w')
clean = 1
debug = 0
verbose = 1
bocop.buildProblem(clean,debug,verbose)
	
for c in c_list:
	
	# set constant C
	sys.stdout.write('Optimize for C = '+str(c))
	sys.stdout.flush()
	bocop.setConstant(5,c)

	# solve problem
	maxtime = 3600
	verbose = 0
	bocop.launchProblem(clean,maxtime,verbose)
	
	# save solution
	target = 'problem.sol'
	solfile = 'C-'+str(c)+'.sol'
	subprocess.call('cp ' + target + ' ' + output_path +'/'+ solfile,shell=True,stdout=fnull,stderr=fnull)
	
	# append results to log
	objective, time_steps, time_stages, state, control, parameters, costate, boundary_mult, status = bocop.readSolFile(target)
	sys.stdout.write('\t Objective: '+str(objective)+'\n')
	sys.stdout.flush()
	resultfile.writelines(str(c)+' '+str(objective)+'\n')


resultfile.close()
