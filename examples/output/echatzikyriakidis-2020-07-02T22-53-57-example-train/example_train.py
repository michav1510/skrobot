from os import path

from sand.experiment import Experiment
from sand.train_ml_task import TrainMlTask

experiment = Experiment('output', __file__).set_experimenter('echatzikyriakidis').build()

######### Experiment

from sklearn.linear_model import LogisticRegression

random_seed = 42

estimator = LogisticRegression(solver='liblinear', random_state=random_seed)

results = experiment.run(TrainMlTask(estimator_template=estimator,
                                     data_set_file_path=path.join('data','data.csv'),
                                     random_seed=random_seed))

print(results['estimator'])