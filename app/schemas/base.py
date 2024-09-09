from pydantic import BaseModel

class CustomBaseModel(BaseModel):
    def dict(self, *args, **kwargs):
        dictionary = super().model_dump(*args, **kwargs)
        dictionary = { k: v for k, v in dictionary.items() if v is not None } #retornar os valores que nao sao NONE
        return dictionary