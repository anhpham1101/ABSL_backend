import json
from time import time
import numpy as np
import requests

SHIRT_MODEL_API = f'https://salt-ffn-shirt.herokuapp.com/v1/models/cloth_salt_ffn:predict'
PHONE_MODEL_API = f'https://salt-ffn-phone.herokuapp.com/v1/models/phone_salt_ffn:predict'
OTHER_MODEL_API = f'https://salt-ffn-other-gibb.herokuapp.com/v1/models/other_salt_ffn:predict'
GIBB_MODEL_API = f'https://salt-ffn-other-gibb.herokuapp.com/v1/models/gibb_salt_ffn:predict'

class Model:
    def __init__(self, data, signature_name="serving_default"):
        self.data = data
        self.signature_name = signature_name
        self.model_path = None

    def predict(self):
        try:
            data = json.dumps({
                "signature_name": self.signature_name,
                "instances": self.data
            })
            headers = {"content-type": "application/json"}
            json_response = requests.post(
                self.model_path,
                data=data,
                headers=headers
            )
            return json_response
        except Exception as e:
            print(e)

class Shirt(Model):
    def __init__(self, data, signature_name="serving_default"):
        super().__init__(data, signature_name)
        self.model_path = SHIRT_MODEL_API

    def predict(self):
        json_response = super().predict()
        if json_response.status_code == 200:
            sentiment_pred = json.loads(json_response.text)['predictions']
            for comment in sentiment_pred:
                for key, value in comment.items():
                    comment[key] = np.argmax(value).item()
            return sentiment_pred
        else:
            print('Server shirt is overload')
            return []

class Phone(Model):
    def __init__(self, data, signature_name="serving_default"):
        super().__init__(data, signature_name)
        self.model_path = PHONE_MODEL_API

    def predict(self):
        json_response = super().predict()
        if json_response.status_code == 200:
            sentiment_pred = json.loads(json_response.text)['predictions']
            for comment in sentiment_pred:
                for key, value in comment.items():
                    comment[key] = np.argmax(value).item()
            return sentiment_pred
        else:
            print('Server phone is overload')
            return []

class Other(Model):
    def __init__(self, data, signature_name="serving_default"):
        super().__init__(data, signature_name)
        self.model_path = OTHER_MODEL_API

    def predict(self):
        json_response = super().predict()
        if json_response.status_code == 200:
            other_pred = list(map(lambda r: dict({'other': r}), json.loads(json_response.text)['predictions']))
            for comment in other_pred:
                for key, value in comment.items():
                    comment[key] = np.argmax(value).item()
            return other_pred
        else:
            print('Server other is overload')
            return []

class Gibb(Model):
    def __init__(self, data, signature_name="serving_default"):
        super().__init__(data, signature_name)
        self.model_path = GIBB_MODEL_API

    def predict(self):
        json_response = super().predict()
        if json_response.status_code == 200:
            other_pred = list(map(lambda r: dict({'other': r}), json.loads(json_response.text)['predictions']))
            for comment in other_pred:
                for key, value in comment.items():
                    comment[key] = np.argmax(value).item()
            return other_pred
        else:
            print('Server gibb is overload')
            return []
