#!/bin/sh

#SBATCH --job-name=ffmpeg-blames	# Name for your job
#SBATCH --comment="Calculating git blames for ffmpeg"

#SBATCH --account=vhp	
#SBATCH --partition=debug		# change to tier3 when ready, usually debug

#SBATCH --output=%x_%j.out		# Output file
#SBATCH --error=%x_%j.err		# Error file

#SBATCH --mail-user=slack:@axmvse	# Slack username to notify
#SBATCH --mail-type=END			# Type of slack notifications to send

#SBATCH --time=0-1:00:00	# 0 days, 16 hour time limit

#SBATCH --nodes=1			# How many nodes to run on
#SBATCH --ntasks=2			# How many tasks per node
#SBATCH --cpus-per-task=1		# Number of CPUs per task
#SBATCH --mem-per-cpu=4g		# Memory per CPU

echo "Script running!"
date

hostname				# Run the command hostname

spack env activate ~/vhp_env

echo "Spack env activated"
date

cp -r ~/ffmpeg /dev/shm

echo "Blame dumping..."
date

for i in $(seq 0 25 100); do
  echo "Starting task $i"

  srun --nodes=1 --ntasks=1 --cpus-per-task=1 --exclusive \
      sqlite3 ~/blames/blame-$SLURM_JOB_NAME-$SLURM_JOB_ID-$i.sqlite \
      ".param set :repo ~/ffmpeg" \
      ".param set :offset $i" \
      ".read src/create_filepaths.sql" \
      ".import ./ffmpeg_smaller.txt filepaths" \
      ".read src/blame-dump.sql" 

done
