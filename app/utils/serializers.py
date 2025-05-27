
from sqlalchemy.orm import class_mapper


def model_to_dict(instance):
    return {column.key: getattr(instance, column.key) for column in class_mapper(instance.__class__).columns}

info="""from utils.serializers import model_to_dict
        data = [model_to_dict(obj) for obj in products]"""



