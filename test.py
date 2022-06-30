from numpy import average
from src.generator import UUIDGenerator, UUIDGeneratorDict
import timeit



def test_generate_btree():
    generator = UUIDGenerator()

    uuids = []
    for i in range(10000):
        uuids.append(generator.generate())
        generator.generate()

    for uuid in uuids:
        assert generator.exists(uuid)

def test_generate_dict():
    generator = UUIDGeneratorDict()

    uuids = []
    for i in range(10000):
        uuids.append(generator.generate())
        generator.generate()

    for uuid in uuids:
        assert generator.exists(uuid)


btree_times = timeit.repeat("test_generate_btree()", "from __main__ import test_generate_btree", number=10, repeat=5)
btree_time = average(btree_times)
dict_times = timeit.repeat("test_generate_dict()", "from __main__ import test_generate_dict", number=10, repeat=5)
dict_time = average(dict_times)

print("Generate btree:", btree_time)
print("Generate dict:", dict_time)

# print("UUIDs:\n", uuids)
# print("\nGenerator:\n", generator)

