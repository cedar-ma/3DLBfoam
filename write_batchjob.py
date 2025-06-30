import os
from tqdm import tqdm
import glob
# Read all directories in the given path
def read_all_dirs(path):
    dirs = glob.glob(f'{path}/*')
    return dirs

def get_sim_name(dir_path):
    return os.path.basename(dir_path)


if __name__ == "__main__":
    sim_dirs = read_all_dirs('/scratch/08780/cedar996/lbfoam/fno/fracture_sims')

    # Read in batchjob template
    with open('hyprogram.sh', 'r') as t:
        templ = t.read()

    for sim_path in tqdm(sim_dirs):

        sim_name = get_sim_name(sim_path)

        # Make a copy of the template
        templ_copy = str(templ)


        # Replace template strings with given values
        templ_copy = templ_copy.replace('{jobname}', sim_name)
        templ_copy = templ_copy.replace('{stdout_directory}', sim_path)
        templ_copy = templ_copy.replace('{stderr_directory}', sim_path)
        templ_copy = templ_copy.replace('{number_of_nodes}', '1')
        templ_copy = templ_copy.replace('{tasks_per_node}', '128')
        templ_copy = templ_copy.replace('{time}', '01:30:00')
        templ_copy = templ_copy.replace('{queue_name}', 'normal')
        templ_copy = templ_copy.replace('{TACC_project}', 'OTH21076')
        templ_copy = templ_copy.replace('{sim_directory_path}', sim_path)


        # Write out batchjob template
        with open(os.path.join(sim_path, 'batchjob.sh'), 'w') as f:
            f.write(templ_copy)


