#!/usr/bin/env python3
# Tami Leppert
# 7/9/2025
# v 1.0
# 1/28/2026 move file to vm-scripts and chmod 775
# v 2.0
#
# fin contains two columns, tab separated
# first column is size in base #s
# second column is SRR number
#
# program invoke_mycosnp_script.py reads in input file, list of samples and sizes
# finds corresponding vm-scripts/SRR*startup*.script file
# The script file in vm-scripts is used to download and process the SRR in a google cloud vm
# This program finds 1000 of the xlow or 1000 low or 1000 med or 1000 large size, 100 xlarge or 10 xxlarge files and queues them.
# They are only queueable if they have a script file in the vm-scripts directory.
# Once they have run, the vm-script/SRR*startup*.script file is removed.
#
# This program creates the queuing scripts.  It does not execute them, the user will need to execute them manually.

import os
from pathlib import Path
from datetime import datetime

# Get the current time
now = datetime.now()
# Format the current time
format_date_time = now.strftime("%Y-%m-%d.%H.%M")

xsmall_count = 0
small_count = 0
medium_count = 0
large_count = 0
xlarge_count = 0
xxlarge_count = 0

#find the current directory path
from pathlib import Path
current_directory = Path.cwd()
#print(current_directory)
#current_directory = input("Enter the full path to vm-running (e.g. /Users/tleppert/Desktop/candidas/cloud3): ")

# Determine the number of each size file that the user wishes to queue
# Note that the suggested numbers are somewhat arbitrary, sometimes there are no vm's available
# Watch the queuing process to see that machines were available to accept the queuing.
xlow_max = int(input("Enter the number of xlow (<1GB) sra files to queue (1000): "))
low_max = int(input("Enter the number of low (1-<2GB) sra files to queue (1000): "))
medium_max = int(input("Enter the number of medium (2-<4GB) sra files to queue (was 50-now 1000): "))
large_max = int(input("Enter the number of large (>=4GB-10GB) sra files to queue (was 10-now 1000): "))
xlarge_max = int(input("Enter the number of xlarge (>=10-15GB) sra files to queue (was 10-now 100): "))
xxlarge_max = int(input("Enter the number of xxlarge (>=15GB) sra files to queue (10): "))

# open input file and output files
fin = open("sra_now.list", 'r')
if xlow_max > 0:
    filexlow = f"execute-vm-xlow-{format_date_time}.script"
    foutxlow = open(filexlow, 'w')
if low_max > 0:
    filelow = f"execute-vm-low-{format_date_time}.script"
    foutlow = open(filelow, 'w')
if medium_max > 0:
    filemed = f"execute-vm-med-{format_date_time}.script"
    foutmed = open(filemed, 'w')
if large_max > 0:
    filelarge = f"execute-vm-large-{format_date_time}.script"
    foutlarge = open(filelarge, 'w')
if xlarge_max > 0:
    filexlarge = f"execute-vm-xlarge-{ormat_date_time}.script"
    foutxlarge = open(filexlarge, 'w')
if xxlarge_max > 0:
    filexxlarge = f"execute-vm-xxlarge-{format_date_time}.script"
    foutxxlarge = open(filexxlarge, 'w')

# for each line in input sra file list
for line in fin:

    # debug print("line: " + line.strip())
    # split the line into columns, two columns
    columns = line.strip().split('\t')

    # get the sra string of the second column put it into srr_number
    srr_number = columns[1]
    srr_size = columns[0]
    lower_srr_number = srr_number.lower()  # lower case the srr or err number
    vm1 = 0     # If run needs to be not preempted instead of preempted
#    if int(srr_size) >= 2000000000:  # Anything >= 2GB is not preemptible
#    if int(srr_size) >= 4000000000:  # Anything >= 4GB is not preemptible
#    if int(srr_size) >= 10000000000:  # Anything >= 10GB is not preemptible
    if int(srr_size) >= 90000000000:  # Anything >= 90GB is not preemptible
        vm1 = 1
        filein = f"{srr_number}-startup-vm1.script"
        filepathin = f"{current_directory}/vm-scripts/{srr_number}-startup-vm1.script"        
    if vm1 == 0:                    # else is preemptible
        filein = f"{srr_number}-startup.script"
        filepathin = f"{current_directory}/vm-scripts/{srr_number}-startup.script"

    filein_path = Path(filepathin)
    
    if filein_path.exists():
        # variable initialization
        xsmall_size = 0
        small_size = 0
        medium_size = 0
        large_size = 0
        xlarge_size = 0
        xxlarge_size = 0
        
        # file size evaluation
        if int(srr_size) < 1000000000:  # XSmall
            xsmall_size = 1
        elif int(srr_size) < 2000000000:  # Small
            small_size = 1        
        elif int(srr_size) < 4000000000:  # Medium
            medium_size = 1                
        elif int(srr_size) < 10000000000:  # Large
            large_size = 1                        
        elif int(srr_size) < 15000000000:  # XLarge
            xlarge_size = 1                        
        elif int(srr_size) >= 15000000000:  # XXLarge
            xxlarge_size = 1                        
        #debug print("3 columns, position: " + columns[1] + " number: " + columns[2])

        #
        # Write the scripts that will queue the vms
        #
        #1000 of these
        if (xsmall_size == 1) and (xsmall_count < xlow_max):
            xsmall_count += 1
            foutxlow.write('gcloud compute instances create-with-container ' + lower_srr_number + '-pathogen-vm --preemptible --zone=us-west1-a --machine-type=e2-highmem-4 --boot-disk-size=50 --container-image="us-west1-docker.pkg.dev/c-auris-cdc/pathogen-repo/pathogentotree" --metadata-from-file user-data=' + srr_number + '-startup.script --service-account=250856040547-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_write\n')
            foutxlow.write("mv " + str(current_directory) + "/vm-scripts/" + filein + " " + str(current_directory) + "/vm-running/xlow/" + filein + "\n")
        # 1000 of these
        if (small_size == 1) and (small_count < low_max):
            small_count += 1
#            foutlow.write('gcloud compute instances create-with-container ' + lower_srr_number + '-pathogen-vm --preemptible --zone=us-west1-a --machine-type=e2-highmem-16 --boot-disk-size=100 --container-image="us-west1-docker.pkg.dev/c-auris-cdc/pathogen-repo/pathogentotree" --metadata-from-file user-data=' + srr_number + '-startup.script --service-account=250856040547-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_write\n')
            foutlow.write('gcloud compute instances create-with-container ' + lower_srr_number + '-pathogen-vm --preemptible --zone=us-west1-a --machine-type=e2-highmem-4 --boot-disk-size=50 --container-image="us-west1-docker.pkg.dev/c-auris-cdc/pathogen-repo/pathogentotree" --metadata-from-file user-data=' + srr_number + '-startup.script --service-account=250856040547-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_write\n')
            foutlow.write("mv " + str(current_directory) + "/vm-scripts/" + filein + " " + str(current_directory) + "/vm-running/low/" + filein + "\n")
        # 1000 of these
        if (medium_size == 1) and (medium_count < medium_max):
            medium_count += 1
#            foutmed.write('gcloud compute instances create-with-container ' + lower_srr_number + '-pathogen-vm1 --preemptible --zone=us-west1-a --machine-type=n1-highmem-32 --boot-disk-size=300 --container-image="us-west1-docker.pkg.dev/c-auris-cdc/pathogen-repo/pathogentotree" --metadata-from-file user-data=' + srr_number + '-startup-vm1.script --service-account=250856040547-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_write\n')
            foutmed.write('gcloud compute instances create-with-container ' + lower_srr_number + '-pathogen-vm --preemptible --zone=us-west1-a --machine-type=e2-highmem-4 --boot-disk-size=50 --container-image="us-west1-docker.pkg.dev/c-auris-cdc/pathogen-repo/pathogentotree" --metadata-from-file user-data=' + srr_number + '-startup.script --service-account=250856040547-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_write\n')
            foutmed.write("mv " + str(current_directory) + "/vm-scripts/" + filein + " " + str(current_directory) + "/vm-running/medium/" + filein + "\n")
        # 10 of these
        if (large_size == 1) and (large_count < large_max):
            large_count += 1
#            foutlarge.write('gcloud compute instances create-with-container ' + lower_srr_number + '-pathogen-vm1 --preemptible --zone=us-west1-c --machine-type=n2d-highmem-48 --boot-disk-size=500 --container-image="us-west1-docker.pkg.dev/c-auris-cdc/pathogen-repo/pathogentotree" --metadata-from-file user-data=' + srr_number + '-startup-vm1.script --service-account=250856040547-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_write\n')
            foutlarge.write('gcloud compute instances create-with-container ' + lower_srr_number + '-pathogen-vm --preemptible --zone=us-west1-a --machine-type=n4-highmem-8 --boot-disk-size=200 --container-image="us-west1-docker.pkg.dev/c-auris-cdc/pathogen-repo/pathogentotree" --metadata-from-file user-data=' + srr_number + '-startup.script --service-account=250856040547-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_write\n')
            foutlarge.write("mv " + str(current_directory) + "/vm-scripts/" + filein + " " + str(current_directory) + "/vm-running/large/" + filein + "\n")
        if (xlarge_size == 1) and (xlarge_count < xlarge_max):
            xlarge_count += 1
            foutxlarge.write('gcloud compute instances create-with-container ' + lower_srr_number + '-pathogen-vm --preemptible --zone=us-west1-a --machine-type=n4-highmem-8 --boot-disk-size=200 --container-image="us-west1-docker.pkg.dev/c-auris-cdc/pathogen-repo/pathogentotree" --metadata-from-file user-data=' + srr_number + '-startup.script --service-account=250856040547-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_write\n')
            foutxlarge.write("mv " + str(current_directory) + "/vm-scripts/" + filein + " " + str(current_directory) + "/vm-running/xlarge/" + filein + "\n")
        if (xxlarge_size == 1) and (xxlarge_count < xxlarge_max):
            xxlarge_count += 1
            foutxxlarge.write('gcloud compute instances create-with-container ' + lower_srr_number + '-pathogen-vm --preemptible --zone=us-west1-a --machine-type=e2-highmem-16 --boot-disk-size=500 --container-image="us-west1-docker.pkg.dev/c-auris-cdc/pathogen-repo/pathogentotree" --metadata-from-file user-data=' + srr_number + '-startup.script --service-account=250856040547-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_write\n')
            foutxxlarge.write("mv " + str(current_directory) + "/vm-scripts/" + filein + " " + str(current_directory) + "/vm-running/xxlarge/" + filein + "\n")

# close files            
fin.close()

# if /vm-scripts does not exist, create it                                                                     
runpath=f"{current_directory}/vm-scripts"
path_exists=Path(runpath)
path_exists.mkdir(parents=True,exist_ok=True)

# File cleanup and chmod
if xlow_max > 0:
    foutxlow.close()
    # move file to /vm-scripts and chmod to 775
    filemv = f"{current_directory}/vm-scripts/{filexlow}"
    os.rename(filexlow,filemv)
    os.chmod(filemv,0o775)
    
    #check if current_directory/vm-runnning/xlow exists, if not create it.
    runpath=f"{current_directory}/vm-running/xlow"
    path_exists=Path(runpath)
    path_exists.mkdir(parents=True,exist_ok=True)
if low_max > 0:
    foutlow.close()
    # move file to /vm-scripts and chmod to 775
    filemv = f"{current_directory}/vm-scripts/{filelow}"
    os.rename(filelow,filemv)
    os.chmod(filemv,0o775)

    #check if current_directory/vm-runnning/low exists, if not create it.
    runpath=f"{current_directory}/vm-running/low"
    path_exists=Path(runpath)
    path_exists.mkdir(parents=True,exist_ok=True)
if medium_max > 0:
    foutmed.close()
    # move file to /vm-scripts and chmod to 775
    filemv = f"{current_directory}/vm-scripts/{filemed}"
    os.rename(filemed,filemv)
    os.chmod(filemv,0o775)

    #check if current_directory/vm-runnning/medium exists, if not create it.
    runpath=f"{current_directory}/vm-running/medium"
    path_exists=Path(runpath)
    path_exists.mkdir(parents=True,exist_ok=True)
if large_max > 0:
    foutlarge.close()
    # move file to /vm-scripts and chmod to 775
    filemv = f"{current_directory}/vm-scripts/{filelarge}"
    os.rename(filelarge,filemv)
    os.chmod(filemv,0o775)

    #check if current_directory/vm-runnning/large exists, if not create it.
    runpath=f"{current_directory}/vm-running/large"
    path_exists=Path(runpath)
    path_exists.mkdir(parents=True,exist_ok=True)
if xlarge_max > 0:
    foutxlarge.close()
    # move file to /vm-scripts and chmod to 775
    filemv = f"{current_directory}/vm-scripts/{filexlarge}"
    os.rename(filexlarge,filemv)
    os.chmod(filemv,0o775)

    #check if current_directory/vm-runnning/xlarge exists, if not create it.
    runpath=f"{current_directory}/vm-running/xlarge"
    path_exists=Path(runpath)
    path_exists.mkdir(parents=True,exist_ok=True)
if xxlarge_max > 0:
    foutxxlarge.close()    
    # move file to /vm-scripts and chmod to 775
    filemv = f"{current_directory}/vm-scripts/{filexxlarge}"
    os.rename(filexxlarge,filemv)
    os.chmod(filemv,0o775)

    #check if current_directory/vm-runnning/xxlarge exists, if not create it.
    runpath=f"{current_directory}/vm-running/xxlarge"
    path_exists=Path(runpath)
    path_exists.mkdir(parents=True,exist_ok=True)
