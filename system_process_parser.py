import subprocess
import numpy
from datetime import datetime

now = datetime.now()


def get_processes():
    output = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE).stdout.readlines()
    headers = [h for h in b' '.join(output[0].strip().split()).split() if h]
    raw_data = list(map(lambda s: s.strip().split(None, len(headers) - 1), output[1:]))
    return raw_data


def system_users(raw_data):
    users = []
    for i in raw_data:
        users.append((i[0].decode("utf-8")))
    number_list = numpy.array(users)
    unique, counts = numpy.unique(number_list, return_counts=True)
    frequencies = numpy.asarray((unique, counts)).T
    return frequencies


def system_memory(raw_data):
    total_memory = []
    for i in raw_data:
        memory = []
        memory.append(i[5].decode("utf-8"))
        memory.append(i[10].decode("utf-8"))
        total_memory.append(memory)
    return total_memory


def system_cpu(raw_data):
    total_cpu = []
    for i in raw_data:
        cpu = []
        cpu.append(i[2].decode("utf-8"))
        cpu.append(i[10].decode("utf-8"))
        total_cpu.append(cpu)
    return total_cpu


def writing_to_a_file(frequencies, total_memory, total_cpu ):
    with open(f"{now.strftime('%d-%m-%Y-%I:%M')}-scan.txt", "w") as file:
        print('System users:', end=' ', file=file)
        for i in frequencies[:-1]:
            print(i[0], end=', ', file=file)
        print(frequencies[-1][0], file=file)

        print('Processes running:', end=' ', file=file)
        processes = 0
        for i in frequencies:
            processes += int(i[1])
        print(processes, file=file)

        print('User processes:', file=file)
        for i in frequencies:
            print(f'{i[0]}: {i[1]}', file=file)

        print('Total memory used:', end=' ', file=file)
        memory = 0
        for i in total_memory:
            memory += int(i[0])
        print(f'{round(memory / 1024, 2)} mB', file=file)

        print('Total cpu used:', end=' ', file=file)
        cpu = 0
        for i in total_cpu:
            cpu += float(i[0])
        print(f'{round(cpu, 1)} %', file=file)

        print('Uses the most memory:', end=' ', file=file)
        max_mem = [0, '']
        for i in total_memory:
            if int(i[0]) > int(max_mem[0]):
                max_mem = i
        print(max_mem[1][:20], file=file)

        print('Uses the most cpu:', end=' ', file=file)
        max_cpu = [0, '']
        for i in total_cpu:
            if float(i[0]) > float(max_cpu[0]):
                max_cpu = i
        print(max_cpu[1][:20], file=file)


raw_data = get_processes()
system_users_ = system_users(raw_data)
memory_ = system_memory(raw_data)
system_cpu_ = system_cpu(raw_data)
writing_to_a_file(system_users_, memory_, system_cpu_)
