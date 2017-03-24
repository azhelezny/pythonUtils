import argparse
import os
import re
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

arg_parser = argparse.ArgumentParser(description='extracts requests from JMX file and run them using ODBC driver')
arg_parser.add_argument('-t', '--tableName', help='Table name', type=str, default="CLOB_TABLE")
arg_parser.add_argument('-s', '--schemaName', help='Schema name', type=str, default="CLOB_SCHEMA")
arg_parser.add_argument('-r', '--rowCount', help='rows in result table', type=int, required=True)
arg_parser.add_argument('-z', '--size', help='size od CLOB', type=str, required=True)
arg_parser.add_argument('-o', '--outputFile', help='output file name', type=str, default="query.sql")
args = arg_parser.parse_args()

table_name = args.tableName
schema_name = args.schemaName
size = args.size
rows = args.rowCount
output_file = args.outputFile

available_symbols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
available_symbols_limit = len(available_symbols) - 1


def get_size(size_str):
    """
    @type size_str:str
    """
    num_size_local = int(re.search('\d+', size_str).group(0))
    if size_str.endswith("K"):
        num_size_local *= 1024
    if size_str.endswith("M"):
        num_size_local *= 1024 ** 2
    if size_str.endswith("G"):
        num_size_local *= 1024 ** 3
    return num_size_local


def fill_buffer(buffer_size):
    """
    @type buffer_size:int
    """
    string_buffer = ''
    print "Start buffering"
    start_ts = time.time()
    min_lc = ord(b'a')
    min_bc = ord(b'A')
    len_lc = 26
    ba = bytearray(os.urandom(buffer_size))
    for i, b in enumerate(ba):
        ba[i] = min_bc + b % len_lc
    stop_ts = time.time()
    print "Stop buffering, time spent %s sec" % str(stop_ts - start_ts)
    return str(ba)


create_table_pattern = 'CREATE TABLE %s.%s (col CLOB(%s));' % (schema_name, table_name, size)
num_size = get_size(size)

file = open(output_file, "w")
file.write(create_table_pattern + '\n')

iterations = 100 * num_size // 2147483648
if iterations == 0:
    iterations = 1

buffer_size = num_size // iterations
rest = num_size % iterations

print "iterations :" + str(iterations)
print "buffer_size :" + str(buffer_size)
print "rest :" + str(rest)

print "Start generation"
start_timestamp = time.time()

for i in range(rows):
    file.write('INSERT INTO %s.%s values (\'' % (schema_name, table_name))
    for j in range(iterations):
        file_line = fill_buffer(buffer_size)
        file.write(file_line)
    file_line = fill_buffer(rest)
    file.write(file_line)
    file.write('\');\n')

stop_timestamp = time.time()
print "Stop buffering, time spent %s sec" % str(stop_timestamp - start_timestamp)
print "done"
