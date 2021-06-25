#!/usr/bin/env python

import time
import json
import requests
import argparse
import sys
import os



url = {
    "production": 'https://testdata.svc.eng.vmware.com',
    "staging": 'https://testdata.svc-stage.eng.vmware.com',
    "development": 'http://localhost:3001'

}

# env is production or staging or development - Set the env variable: export API_ENV=development
server_env = os.environ.get('API_ENV', 'production')

server_url = url[server_env]

def milli_time():
    return int(time.time_ns() / 1000000)  # Requires python 3.7


def check_http(result):
    if result.status_code < 200 or result.status_code > 202:
        if result.text:
            raise requests.HTTPError(result.text)
        result.raise_for_status()


class Upm(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Execute UPM APIs',
            usage='''upm <api> [<args>]

            API options are:
               start_pipeline     To start the pipeline
               start_test         To start the test
               finish_test        To finish the test
               finish_pipeline    To finish the pipeline ''')
        parser.add_argument('api', help='api to run')

        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.api):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.api)()

    def start_pipeline(self):
        parser = argparse.ArgumentParser(
            description='Start the pipeline')
        # prefixing the argument with -- means it's optional
        parser.add_argument('--pipeline_name', required=True, action='store',
                                    help='Hint: pipeline_name')  # True
        parser.add_argument('--pipeline_build_number', required=False, action='store', default=milli_time(),
                                    type=int,
                                    help='Hint: pipeline_build_number as an integer (Optional)')
        parser.add_argument('--bu', required=False, action='store', default='cpbu', help='Hint: BU details (Default cpbu)')
        parser.add_argument('--title', required=False, action='store', default=None,
                            help='Hint: Title')
        parser.add_argument('--jenkins_url', required=False, action='store', default=None,
                            help='Hint: jenkins_url')

        # now that we're inside a start_pipeline function
        args = parser.parse_args(sys.argv[2:])
        result = requests.post(server_url + '/v1/api/testdata/start_pipeline', json={
            'bu': args.bu,
            'pipeline_name': args.pipeline_name.upper(),
            'pipeline_build_number': args.pipeline_build_number,
            'title': args.title,
            'jenkins_url': args.jenkins_url,
            'url': args.jenkins_url
        })
        check_http(result)
        print(result.text)
        return result.text

    def start_test(self):
        parser = argparse.ArgumentParser(
            description='Start test')
        parser.add_argument('--test_name', required=False, action='store', default=None, help='Hint: test_name')
        parser.add_argument('--pipeline_fk', required=True, action='store', default=None,
                            help='Hint: pipeline id as a string')
        parser.add_argument('--build_id', required=True, action='store', type=int,
                                help='Hint: build_id as integer')  # True
        parser.add_argument('--build_system', required=True, action='store',
                                help='Hint: build_system OB or SB')  # True
        parser.add_argument('--product', required=True, action='store', help='Hint: product details')  # True
        parser.add_argument('--bu', required=False, action='store', default='cpbu', help='Hint: BU details (Default cpbu)')
        parser.add_argument('--test_tag', required=False, action='store', default='build', help='Hint: Test tag')
        parser.add_argument('--test_type', required=False, action='store', default='BUILD', help='Hint: Test Type')
        parser.add_argument('--owner', required=True, action='store', help='Hint: Test owner')

        # now that we're inside a start_pipeline function
        args = parser.parse_args(sys.argv[2:])
        if not args.test_name:
            test_name = args.product + '_' + args.build_system
        else:
            test_name = args.test_name
        result = requests.post(server_url + '/v1/api/testdata/start_test', json={
            'pipeline_fk': args.pipeline_fk,
            'test_name': test_name,
            'product': args.product,
            'triage_owners': args.owner,
            'buildweb_id': args.build_id,
            'buildweb_system': args.build_system,
            'test_tag': args.test_tag,
            'test_type': args.test_type
        })
        check_http(result)
        print(result.text)
        return result.text

    def get_test(self, test_fk):
        result = requests.get(server_url + '/v1/api/testdata/test/{}'.format(test_fk))
        check_http(result)
        return result.json()

    def get_pipeline(self, pipeline_id):
        result = requests.get(server_url + '/v1/api/testdata/pipeline/{}'.format(pipeline_id))
        check_http(result)
        return result.json()

    def finish_test(self, state_dump_filename=None):
        parser = argparse.ArgumentParser(
            description='Finish test')
        parser.add_argument('--test_result', required=True, action='store',
                                 help='Hint: test result: Passed/Failed')  # True
        parser.add_argument('--test_fk', required=True, action='store', help='Hint: test fk')  # True
        parser.add_argument('--pipeline_fk', required=True, action='store', default=None,
                            help='Hint: pipeline id as a string')
        # now that we're inside a start_pipeline function
        args = parser.parse_args(sys.argv[2:])
        state_dump = None
        if state_dump_filename:
            with open(state_dump_filename, "r") as state_dump_file:
                state_dump = json.load(state_dump_file)
        test_data = self.get_test(args.test_fk)

        if 'test_details' in test_data:
            test_details = test_data['test_details']
        else:
            test_details = None
        finish_test_data = {
            'test_fk': args.test_fk,
            'state_dump': state_dump,
            'change_details': [test_details],
            'result': args.test_result,
            'end_time': milli_time()
        }
        result = requests.post(server_url + '/v1/api/testdata/finish_test_with_state_dump', json=finish_test_data)
        check_http(result)
        print(result.text)
        pipeline_details = self.get_pipeline(args.pipeline_fk)

        if args.test_result == "Passed":
            pipeline_status = "SUCCESS"
        else:
            pipeline_status = "FAILURE"

        self.update_pipeline(pipeline_id=args.pipeline_fk, update_data=pipeline_details, change_details=test_details, pipeline_status=pipeline_status)
        print(result.text)
        return result.text

    def update_pipeline(self, pipeline_id, update_data, change_details, pipeline_status):
        final_products = []
        for product in update_data['products']:
            del product['_update_time']
            del product['_add_time']
            if pipeline_status == "SUCCESS":
                product['pass_percentage'] = 100
                product['recommendation'] = True
                final_products.append(product)
            else:
                product['pass_percentage'] = 0
                product['recommendation'] = False
                final_products.append(product)
        update_data['products'] = final_products

        data = {
            'pipeline_fk': pipeline_id,
            "change_details": [change_details]
        }
        data.update(update_data)
        result = requests.patch(server_url + '/v1/api/testdata/update_pipeline', json=data)
        check_http(result)
        return result.text

    def finish_pipeline(self):
        parser = argparse.ArgumentParser(
            description='Finish pipeline')
        parser.add_argument('--pipeline_fk', required=True, action='store', default=None,
                            help='Hint: pipeline id as a string')
        parser.add_argument('--pipeline_status', required=True, action='store', default='SUCCESS',
                                     help='Hint: Pipeline status [SUCCESS or FAILURE]')
        # now that we're inside a start_pipeline function
        args = parser.parse_args(sys.argv[2:])

        data = {
            'pipeline_fk': args.pipeline_fk,
            'status': args.pipeline_status
        }
        result = requests.post(server_url + '/v1/api/testdata/finish_pipeline', json=data)
        check_http(result)
        print(result.text)
        return result.text


if __name__ == '__main__':
    Upm()

"""
Sample execution commands:
// Start pipeline
python3 test3.py start_pipeline --pipeline_name="bundle-test"

// Start test with sb build
python3 test3.py start_test --pipeline_fk=5faa8e181a3f39abc27458c6 --build_id=41019398 --build_system=sb --product=sddc-bundle --owner=demo_team

// Finish the test for sb build
python3 test3.py finish_test --test_result=Passed --pipeline_fk=5faa8e181a3f39abc27458c6 --test_fk=5faa8e287d16d9db5df58eaf

// Start test with ob build
python3 test3.py start_test --pipeline_fk=5faa8e181a3f39abc27458c6 --build_id=17102532 --build_system=ob --product=sddc-bundle --owner=demo_team

// Finish the test for ob build
python3 test3.py finish_test --test_result=Passed --pipeline_fk=5faa8e181a3f39abc27458c6 --test_fk=5faa8e507d16d9db5df58eb0

// Finish pipeline
python test3.py finish_pipeline --pipeline_fk=5faa8e181a3f39abc27458c6 --pipeline_status=SUCCESS
"""