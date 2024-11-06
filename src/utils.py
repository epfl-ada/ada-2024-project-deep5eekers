import ast
import json

def clean_column(dict_string):
    try:
        parsed_dict = ast.literal_eval(dict_string)
        return ', '.join(parsed_dict.values())  # Join all names into a single string
    except (ValueError, SyntaxError):
        return dict_string  # Return the string as it is if parsing fails
    
def string_to_list(df, column):
    """ Turn the column specified of the df from a string to a list """
    df[column] = df[column].str.split(', ')
    return df

def string_to_dict(df, column):
    """ Turn the column specified of the df from a string to a dictionary and replace the dictionary column 
    with several columns with the keys of the dictionary """
    df[column] = df[column].apply(json.loads)
    keys = list(df[column][0].keys())

    for key in keys:
        df[key] = df[column].apply(lambda x: x[key])

    df = df.drop(columns = column)
    return df
