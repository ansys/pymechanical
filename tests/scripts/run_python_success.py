# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.

def get_project_name():
    return DataModel.GetObjectById(4).Name


def get_simple_string():
    return "test"


x = 0
x = x + 1

get_project_name()

get_simple_string()
