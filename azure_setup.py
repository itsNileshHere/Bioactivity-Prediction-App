from azureml.core import Workspace, Experiment, Environment
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException

# Connect to your workspace
ws = Workspace.from_config()

# Create an experiment
experiment_name = 'chembl-bioactivity'
experiment = Experiment(ws, experiment_name)

# Create a compute target
compute_name = "cpu-cluster"
try:
    compute_target = ComputeTarget(workspace=ws, name=compute_name)
    print('Found existing compute target.')
except ComputeTargetException:
    compute_config = AmlCompute.provisioning_configuration(vm_size='STANDARD_DS11_V2', max_nodes=4)
    compute_target = ComputeTarget.create(ws, compute_name, compute_config)
    compute_target.wait_for_completion(show_output=True)

# Define a new environment
env = Environment.from_conda_specification(name="chembl-env", file_path="environment.yml")
