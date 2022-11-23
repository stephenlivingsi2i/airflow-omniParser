from omniParser.omniparser.parser import OmniParser
from memory_profiler import profile
import time
import os
#
# file = open('data/cclf/cclf8.txt', "r")
# lines = []
# for each in file:
#     lines.append(each)
#
#
# def manipulate_file():
#     sample_file = open('data/cclf/sample.txt', 'w')
#     for _ in range(833334):
#         for each in lines:
#             sample_file.write(each)
#         sample_file.write('\n')
# manipulate_file()
# #
parser = OmniParser("CCLF_CCLF8")
print("started---->>>>")
file_size = os.path.getsize('data/cclf/sample.txt')
print(f"Input file Size is: {file_size} bytes (or) {file_size/(1024*1024) } mb")
start_time = time.time()


@profile
def trans():
    print(parser.transform("data/cclf/sample.txt", "outputs/cclf/cclf8.json"))


trans()
end_time = time.time()
print(f"Total time taken: {end_time - start_time}")
file_size = os.path.getsize('outputs/cclf/cclf8.json')
print(f"Output file Size is: {file_size} bytes (or) {file_size/(1024*1024) } mb")
