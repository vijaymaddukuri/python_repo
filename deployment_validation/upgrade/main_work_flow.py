import logging as logger
from os.path import dirname, abspath, join
from argparse import ArgumentParser
from tas_middleware_validation.middleware_worker_validation import perfrom_middlewre_enpoint_validation, Middleware
from tas_middleware_validation.tas_validation import perfrom_tas_endpoint_validation, TAS
from common.functions import convert_csv_to_yaml, copy_file, save_execution_log, search_for_file_in_dir, tsa_service_operations
from time import sleep

current_dir = dirname(dirname(abspath(__file__)))


def main(csv_files_path):

    logger.info("###############START#########################")
    yaml_file_list = convert_csv_to_yaml('deployment', csv_files_path)
    logger.info('Converted deployment CSV input to yaml format')
    logger.info("###############END###########################\n")
    sleep(2)

    while True:
        option = input ("""Please choose one option from following:
        1.	Upgrade
        2.	Configuration update
        3.	Validation/Health Check
        """)

        if int(option) == 1:
            print("##############################################")
            print("You have selected Upgrade option \n")
            options = 'abcde'
            while True:
                upgrade = input("""Choose one or more options separated by space for upgrade:
                a.	Middleware
                b.	TAMS
                c.	Worker
                d.	Salt CherryPy
                e.	 All

                Example: For Middleware and worker upgrade, pass the following input
                        a c
                """)
                upgrade = upgrade.split()
                flag = 1
                for item in upgrade:
                    if item in options:
                        continue
                    else:
                        flag = 0

                if flag:
                    for item in upgrade:

                        if item == 'a' or item == 'e':

                            logger.info("###############START#########################")
                            logger.info("Middleware Upgrade is started \n")

                            logger.info('Converted Middleware data from CSV to yaml format\n')
                            logger.info('Middleware upgrade is successfully completed')
                            logger.info("###############END###########################\n")

                        if item == 'b' or item == 'e':
                            # Need to update
                            logger.info("###############START#########################")
                            logger.info("TAMS Upgrade is started \n")
                            logger.info('Converted TAMS data from CSV to yaml format\n')
                            logger.info('TAMS upgrade is successfully completed')
                            logger.info("###############END###########################\n")

                        if item == 'c' or item == 'e':
                            # Need to update
                            logger.info("###############START#########################")
                            logger.info("Worker Upgrade is started \n")
                            logger.info('Converted Worker data from CSV to yaml format\n')
                            logger.info('Worker upgrade is successfully completed')
                            logger.info("###############END###########################\n")

                        if item == 'd' or item == 'e':
                            # Need to update
                            logger.info("###############START#########################")
                            logger.info('Salt is updated')
                            logger.info("###############END###########################\n")

                    logger.info("###############START#########################")
                    logger.info("Executed deployment validation")
                    logger.info("###############END###########################\n")

                    break
                else:
                    print('Sorry, that was incorrect option')
                    continue

        elif int(option) == 2:
            options = 'abcd'
            print("##############################################")
            print("You have selected configuration update (YAML update) option \n")
            while True:
                yaml_update = input("""Choose one or more options separated by space for configuration update:
                  a.	Middleware
                  b.	TAMS
                  c.	Worker
                  d.	All

                  Example: For Middleware and worker configuration update, pass the following input
                                a c
                  """)
                yaml_update = yaml_update.split()
                flag = 1
                for item in yaml_update:
                    if item in options:
                        continue
                    else:
                        flag = 0
                # Copy the deployment yaml file to config dir
                copy_file(source_filename=yaml_file_list[0])
                # Create Object for Middleware
                mw_obj = Middleware()

                # Stop Worker and Middleware service
                mw_obj.stop_mw_worker_services()

                # Get base middleware and worker yaml file from the Middleware VM
                mw_obj.get_mw_worker_config()

                if flag:
                    for item in yaml_update:
                        if item == 'a' or item == 'd':
                            logger.info("###############START#########################")

                            logger.info("Middleware configuration update is started \n")

                            convert_csv_to_yaml('middleware', csv_files_path,
                                                base_yaml_name='config_mw.yaml',
                                                file_name='middleware')
                            logger.info('Converted Middleware data from CSV to yaml format\n')

                            mw_obj.upload_yaml_files(service='middleware')
                            logger.info('Middleware configuration yaml is updated')

                            logger.info("###############END###########################\n")

                        if item == 'b' or item == 'd':
                            logger.info("###############START#########################")
                            logger.info("TAMS configuration update is started \n")
                            flag = 1
                            tas_yaml_dir = join(current_dir, 'config', 'tas')
                            for yaml_file in yaml_file_list:
                                tenant_id = yaml_file.split('_')[0]
                                copy_file(yaml_file)
                                tams_obj = TAS()
                                tams_obj.get_tas_config()
                                if flag:
                                    convert_csv_to_yaml('tas', csv_files_path,
                                                        base_yaml_name='config_tas.yaml')
                                    logger.info('Converted TAMS data from CSV to yaml format\n')
                                    flag=0
                                tenant_yaml_file = search_for_file_in_dir(tas_yaml_dir, tenant_id)
                                if tenant_yaml_file:
                                    tams_obj.upload_yaml_file(filename=tenant_yaml_file)
                                    logger.info('TAMS configuration yaml is updated for the tenant {}'.format(tenant_id))

                                else:
                                    raise Exception("Unable to get the yaml file")

                            logger.info("###############END###########################\n")

                        if item == 'c' or item == 'd':
                            # Need to update
                            logger.info("###############START#########################")
                            logger.info("Worker configuration update is started \n")

                            convert_csv_to_yaml('worker', csv_files_path,
                                                base_yaml_name='config_worker.yaml',
                                                file_name='worker')


                            logger.info('Converted Worker data from CSV to yaml format\n')

                            mw_obj.upload_yaml_files(service='worker')
                            logger.info('Worker configuration yaml is updated')
                            logger.info("###############END###########################\n")

                    # Start Middleware and Worker service
                    tsa_service_operations(sshObject=mw_obj, login=False, service='mws.service')
                    tsa_service_operations(sshObject=mw_obj, login=False, service='bws.service')

                    break
                else:
                    print('Sorry, that was incorrect input')
                    continue

        elif int(option) == 3:
            logger.info("###############START#########################")

        else:
            print('Sorry, that was incorrect input')
            continue
        flag = 1

        if len(yaml_file_list):
            for yaml_file in yaml_file_list:
                logger.info("Deployment Validation started for the tenant {}".format(yaml_file.split('_')[0]))
                copy_file(source_filename=yaml_file)
                if flag:
                    perfrom_middlewre_enpoint_validation()
                    flag=0
                perfrom_tas_endpoint_validation()

        logger.info("###############END###########################\n")

        break

if __name__ == '__main__':
    save_execution_log('upgrade_console')
    parser = ArgumentParser(description='Arguments for upgrading/config update/validation')
    parser.add_argument('-csv', '--csv_path',
                        default=None,
                        action='store',
                        help='Deployment CSV file location')
    args = parser.parse_args()
    if args.csv_path is None:
        csv_path = join(current_dir, 'config', 'csv_files')
        main(csv_path)
    else:
        main(args.csv_path)
