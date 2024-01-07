import os

victim_path = '/config/mqtt/subscriber/'
minimum_files = int(os.environ.get('COVERT_VICTIMS', "1000000"))
victim_files = os.listdir(victim_path)
counter = 0
for file in victim_files:
    if '.json' in file:
        counter += 1

if counter <= minimum_files:
    print("not enough clients yet")
    exit(1)
