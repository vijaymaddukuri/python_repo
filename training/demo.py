from bb_certificate_generation.functions import (get_config)
import os
current_dir = os.getcwd()
yaml_file_path = '{}\{}'.format(current_dir, 'config_new.yaml')

server_ip = get_config('networker_server_details', 'NETWORKER_SERVER_COUNT', yaml_file_path)
print(server_ip)