from pydantic import BaseModel
from datetime import datetime


def merge_model(tar_obj: BaseModel, subset_obj: BaseModel, skip_field: list = []) -> BaseModel:
    tar_obj_key = tar_obj.keys()
    for field_name, field_var in subset_obj.items():
        if (field_name in tar_obj_key) and (field_var is not None) and (field_name != 'id' and field_name not in skip_field):
            setattr(tar_obj, field_name, field_var)
    return tar_obj
