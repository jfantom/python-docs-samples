#!/usr/bin/env python

# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to perform basic operations on prediction
with the Google AutoML Vision API.

For more information, the documentation at
https://cloud.google.com/vision/automl/docs.
"""

# [START automl_vision_tutorial_import]
import argparse
import os

from google.cloud import automl_v1beta1 as automl

# [END automl_vision_tutorial_import]


# [START automl_vision_predict]
def predict(
    project_id, compute_region, model_id, file_path, score_threshold=""
):
    """Make a prediction for an image.
    Args:
        project_id: Id of the project.
        compute_region: Region name.
        model_id: Id of the model which will be used for image classification.
        file_path: File path of the input image.
        score_threshold: A value from 0.0 to 1.0. When the model
            makes predictions for an image, it will only produce
            results that have at least this confidence score threshold.
            The default is 0.5.
    """
    automl_client = automl.AutoMlClient()

    # Get the full path of the model.
    model_full_id = automl_client.model_path(
        project_id, compute_region, model_id
    )

    # Create client for prediction service.
    prediction_client = automl.PredictionServiceClient()

    # Read the image and assign to payload.
    with open(file_path, "rb") as image_file:
        content = image_file.read()
    payload = {"image": {"image_bytes": content}}

    # params is additional domain-specific parameters.
    # score_threshold is used to filter the result
    # Initialize params
    params = {}
    if score_threshold:
        params = {"score_threshold": score_threshold}

    response = prediction_client.predict(model_full_id, payload, params)
    print("Prediction results:")
    for result in response.payload:
        print("Predicted class name: {}".format(result.display_name))
        print("Predicted class score: {}".format(result.classification.score))


# [END automl_vision_predict]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    predict_parser = subparsers.add_parser("predict", help=predict.__doc__)
    predict_parser.add_argument("model_id")
    predict_parser.add_argument("file_path")
    predict_parser.add_argument("score_threshold", nargs="?", default="")

    project_id = os.environ["PROJECT_ID"]
    compute_region = os.environ["REGION_NAME"]

    args = parser.parse_args()

    if args.command == "predict":
        predict(
            project_id,
            compute_region,
            args.model_id,
            args.file_path,
            args.score_threshold,
        )
