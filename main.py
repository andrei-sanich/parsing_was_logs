import os
import fnmatch
import csv
import re


pattern_msg = r'\s([A-Z]\w{3}[0-9][0-9][0-9][0-9][A-Z])'
pattern_date = r'\d\d.\d\d.\d\d\s\d{1,2}:\d\d:\d\d:\d\d\d'
pattern_host_name = r'Имя хоста:\s(\w+)' 
pattern_profile_name = r'Имя профайла:\s(\w+)'


def get_dirs(root_dir):

    dirs = [root_dir + sub_dir for sub_dir in os.listdir(root_dir)]
    return dirs

	
def get_files(directory, *patterns):

    log_files = []
    for root, dirs, files in os.walk(directory):
        for pattern in patterns:
            for filename in fnmatch.filter(files, pattern):
                log_files.append(os.path.join(root, filename))
    return log_files

	
def parse_info_file(file, *patterns):
  
    data = open(file, encoding='windows-1251').read()
    text = [re.search(pattern, data).group(1) for pattern in patterns]    
    return text             

		
def parse_log_file(file, host_name, profile_name):

    with open(file, 'r', encoding='windows-1251') as input_file:
	    for line in input_file:
	        if line.startswith('['):
	            list_msgs = []
	            date = re.search(pattern_date, line).group(0)
	            date = ''
	            msgs = re.findall(pattern_msg, line)
	            list_msgs.extend(msgs)
	            if date and list_msgs:
	                for msg in list_msgs:
	                    rec = {'date': date, 'type': msg[-1], 'msg': msg, 'host_name': host_name, 'profile_name': profile_name}
	                    write_csv(rec)


def write_csv(data):

    f = open('dataset.csv', 'a')
    writer = csv.writer(f)
    writer.writerow((data['date'], data['type'], data['msg'], data['host_name'], data['profile_name']))
					
					
def main():

    directories = get_dirs('/home/test/')
    for directory in directories:
        log_files = get_files(directory, 'AboutThisProfile.txt', 'SystemOut*.log')
        info_list = parse_info_file(log_files[0], pattern_host_name, pattern_profile_name)
        host_name, profile_name = info_list
        for log_file in log_files[1:]:
	        parse_log_file(log_file, host_name, profile_name)					
					

if __name__ == '__main__':
    main()
