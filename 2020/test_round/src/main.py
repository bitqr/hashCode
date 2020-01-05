from instance import Instance

inputs_array = ['a_example.in', 'b_small.in', 'c_medium.in', 'd_quite_big.in', 'e_also_big.in']

file_name = '../inputs/' + inputs_array[0]

instance = Instance(file_name)
print(instance.to_string())