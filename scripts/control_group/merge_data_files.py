import pandas as pd

def get_file_part(file_base_name, part):
    try:
        return pd.read_csv(f"../../data/{file_base_name}-{part}.csv")
    except:
        return pd.DataFrame()

file_base_name = 'control_group_commits_loc'
part1 = get_file_part(file_base_name, 1)
part2 = get_file_part(file_base_name, 2)
part3 = get_file_part(file_base_name, 3)
part4 = get_file_part(file_base_name, 4)

result = pd.concat([part1, part2, part3, part4], axis=0, ignore_index=True)
result.to_csv(f'../../data/{file_base_name}.csv', index=False)