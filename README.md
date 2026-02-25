
# invoke_mycosnp_script.py
Python code to invoke google vms by pushing make_mycosnp_script sample scripts to google vms running a docker image tleppertwood/pathogentotree.<br/>
The docker image tleppertwood/pathogentotree processes sra sample data from nih.<br/>
The docker image compares sample data to reference sequence and returns comparison edits in the form of .g.vcf.gz and .maple files.<br/>
See [Docker container pathogentotree](https://github.com/tleppertbio/pathogentotree/blob/main/README.md) the docker container that performs the comparisons.<br/>

---

## What will you need

1) [collect metadata](https://github.com/tleppertbio/pathogentotree/blob/main/metadata.README.md), to determine if you have the correct samples and the size of the sample file.
2) [sra_now.list](https://github.com/tleppertbio/pathogentotree/blob/main/README.md#create-sra_nowlist-file), a file containing the size of the sample file and the sra number, tab separated.
3) [google buckets](https://github.com/tleppertbio/pathogentotree/blob/main/README.md#how-to-create-a-bucket-identify-your-google-region-and-viewing-pricing-tablessizes-for-vms), creating a bucket to house your output data until you can retrieve it to your local machine.
4) [reference data](https://github.com/tleppertbio/pathogentotree/blob/main/README.md#create-and-execute-ref-bucket-setupscript-file), reference files prepped for analysis using nucmer, bedtools maskfasta, samtools faidx, picard.jar and bwa, which reside in the google bucket and vms during analysis.
5) [directory structure](https://github.com/tleppertbio/pathogentotree/blob/main/README.md#directory-structure-on-your-local-machine), the directory structure that is created on your local machine, pathogentotree's expected structure.
6) [after this program](https://github.com/tleppertbio/pathogentotree/blobl/main/README.md#execute-scripts-to-invoke-docker-image-on-google-vms) how to execute the script created by this program, where it is located and what is it doing.
7) [complete pathogentotree package](https://github.com/tleppertbio/pathogentotree/blob/main/README.md) full documentation to the entire process, setting up google cloud vms to run pathogentotree docker container to analyze nih sra datasets to find reference compared sequence edits.

### Running invoke_mycosnp_script.py

  **What does this do?**
  
  invoke_mycosnp_script.py reads sra_now.list and finds corresponding vm scripts in ./vm-scripts.<br/>
  This python program creates an invoke script which starts the vm with the correct configuration.<br/>
  This script pushes the process script to the vm running the docker container tleppertwood/pathogentotree.<br/>
  The processing scripts are invoked in the appropriately configured vm size and location.<br/>

  **How to run it?**
  
  python3 invoke_mycosnp_script.py

  **Things to know**
  
  - You will need to know the number of samples in each size category of your sample set.
  - The user enters the number of files to queue (up to 1000 in most cases) per size category.
  - The 1000 or 100 or 10 is a recommended number of vms to invoke, occasionally there will not be a vm available to queue.
  - When you execute the ./execute-vm-size-date-time.script watch the execution carefully.
  - You may sometimes see a failed queue because a vm is not available.
  - You can enter '0' for the number of files to queue, if you do not wish to queue any file in that size category.
  - This program makes scripts to invoke the *RR#.scripts in the ./vm-scripts directory
  - These invoke scripts are made executable and moved into the ./vm-scripts directory
  - These directories are created if they don't already exist vm-running, vm-running/xlow, vm-running/low,
    vm-running/medium, vm-running/large, vm-running/xlarge and vm-running/xxlarge   

Here is an example of the type of file that is created by this invoke_mycosnp_scripts.py python program
[example vm invoke script](https://github.com/tleppertbio/pathogentotree/blob/main/execute-vm-large-2026-01-29.15.48.script)
