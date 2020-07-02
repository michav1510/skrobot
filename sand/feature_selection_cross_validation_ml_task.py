import os, copy

import pandas as pd

import numpy as np

from sklearn.feature_selection import RFECV

from sklearn.pipeline import Pipeline

from sand.base_cross_validation_ml_task import BaseCrossValidationMlTask

class FeatureSelectionCrossValidationMlTask(BaseCrossValidationMlTask):
  def __init__ (self, estimator_template, data_set_file_path, estimator_params=None, preprocessor_template=None, preprocessor_params=None, scoring='f1', feature_columns='all', id_column='id', label_column='label', random_seed=123456789, verbose=3, n_jobs=1):
    super(FeatureSelectionCrossValidationMlTask, self).__init__(FeatureSelectionCrossValidationMlTask.__name__, locals())

  def run(self, output_directory):
    np.random.seed(self.random_seed)

    self.data_set_data_frame = pd.read_csv(self.data_set_file_path)

    y = self.data_set_data_frame[self.label_column]

    X = self.data_set_data_frame.drop(columns=[self.label_column, self.id_column])

    if self.feature_columns != 'all':
      X = X[self.feature_columns]

    model = RFECV(self._build_estimator(), step=1, cv=self._build_cv_splits(X, y), scoring=self.scoring, verbose=self.verbose, n_jobs=self.n_jobs)

    if self.preprocessor_template:
      model = Pipeline(steps=[('preprocessor', self._build_preprocessor()), ('selection', model)])

    model.fit(X, y)

    if self.preprocessor_template:
      features_selected = np.nonzero(model.named_steps.selection.support_)[0].tolist()
    else:
      features_selected = X.columns[model.support_].values.tolist()

    with open(os.path.join(output_directory, 'features_selected.txt'), "w") as f: f.writelines('\n'.join(map(str, features_selected)))

    return features_selected

  def _build_preprocessor (self):
    preprocessor = copy.deepcopy(self.preprocessor_template)

    if self.preprocessor_params: preprocessor.set_params(**self.preprocessor_params)

    return preprocessor

  def _build_estimator (self):
    estimator = copy.deepcopy(self.estimator_template)

    if self.estimator_params: estimator.set_params(**self.estimator_params)

    return estimator