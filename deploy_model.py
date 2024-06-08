from azureml.core import Workspace, Model
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AciWebservice, Webservice

# Connect to your workspace
ws = Workspace.from_config()

# Register the model
model = Model.register(workspace=ws, model_name='chembl_model', model_path='model/SARS_coronavirus.pkl')

# Define inference configuration
inference_config = InferenceConfig(entry_script="scripts/score.py", environment=env)

# Deploy the model
deployment_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=1)
service = Model.deploy(workspace=ws,
                       name='chembl-service',
                       models=[model],
                       inference_config=inference_config,
                       deployment_config=deployment_config)
service.wait_for_deployment(show_output=True)
print(service.state)
print(service.scoring_uri)
