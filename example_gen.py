#!/usr/bin/env python3

import yaml, random, json
from sys import argv

# Open schema file and load with yaml
with open(argv[1], "r") as yml:
    schema = yaml.safe_load(yml)

example_data = {}

# Assembles datapoints into dictionary, keys are datapoints, values are data type
for category in schema.items():
    if not category[0] in ["schema_file", "enums"]:  # Skips these categories
        fields = schema[category[0]]  # fields is list of all datapoints
        for field in fields:
            # Support for datapoints without nested fields, e.g. 'datapoint: int'
            try:
                example_data[field] = fields[field]["type"]
            except TypeError:
                example_data[field] = fields[field]  # Runs if datapoint has no "type" field


# Replaces all datatypes ('int', 'str' etc.) with values
# int and float are randomly generated
# List and str prompt the user for an example value(s)
# Enum randomly chooses from the available types in the enum
for item in example_data.items():
    dataType = example_data[item[0]]
    if dataType == "int":
        example_data[item[0]] = random.randrange(1, 10)  # Generate random integer

    elif dataType == "float":
        example_data[item[0]] = round(
            random.uniform(0, 7), 4
        )  # Generate random float rounded to 4 decimals

    elif dataType == "str":
        example_data[item[0]] = input(
            "Input example string for <%s>: " % item[0]
        )  # Prompt user to enter an example string, specifying the datapoint

    elif dataType == "bool":
        example_data[item[0]] = random.choice([True, False])  # Sets to either true or false

    elif dataType == "List":
        # Prompts the user to enter values separated with commas, (e.g. 1,2,3,hello,7,8), splits values into list
        values = input(
            "Input example values for list <%s>\n(Values separated by ','): " % item[0]
        ).split(",")
        # Converts any numbers in list to type int
        for i, value in enumerate(values):
            try:
                values[i] = int(value)
                example_data[item[0]] = values
            except ValueError:
                example_data[
                    item[0]
                ] = values  # Runs if changing value to an int fails, indicating that it is most likely a string

    # Gets list of possible values from the corresponding enum field and chooses a random one.
    elif "Enum" in dataType:
        example_data[item[0]] = random.choice(list(schema["enums"][item[0]].values()))


# Print json-formatted dictionary to console
print(json.dumps(example_data, indent=4))
