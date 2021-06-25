"""
Copyright 2019 - 2020 VMWare Inc. Proprietary, All Rights Reserved, Confidential
"""

import time
import json
import requests
import argparse


def milli_time():
    return int(time.time_ns() / 1000000)  # Requires python 3.7


def check_http(result):
    if result.status_code < 200 or result.status_code > 202:
        if result.text:
            raise requests.HTTPError(result.text)
        result.raise_for_status()

def get_args():
    parser = argparse.ArgumentParser(description='Recommend Build')
    parser.add_argument('--pipeline_name', required=True, action='store',
                        help='pipeline_name')
    parser.add_argument('--build_id', required=True, action='store', type=int,
                        help='build_id')
    parser.add_argument('--build_system', required=True, action='store',
                        help='build_system')
    parser.add_argument('--product', required=True, action='store',
                        help='product')
    parser.add_argument('--pipeline_build_number', required=False, action='store', default=milli_time(), type=int,
                        help='pipeline_build_number')
    parser.add_argument('--jenkins_url', required=False, action='store', default=None,
                        help='jenkins_url')
    parser.add_argument('--bu', required=False, action='store', default='cpbu',
                        help='bu')
    parser.add_argument('--title', required=False, action='store', default=None,
                        help='title')
    parser.add_argument('--test_name', required=False, action='store', default=None,
                        help='test_name')
    parser.add_argument('--owner', required=False, action='store', default=None,
                        help='owner')
    parser.add_argument('--pipeline_status', required=False, action='store', default='SUCCESS',
                        help='Pipeline status [Success or Failure]')
    parser.add_argument('--api_env', required=False, action='store', default='development',
                        help='Env [production or staging or development]')
    args = parser.parse_args()
    return args


class Uts:
    def __init__(self,
                 pipeline_name,
                 build_id,
                 build_system,
                 product,
                 pipeline_build_number=milli_time(),
                 jenkins_url=None,
                 bu='cpbu',
                 title=None,
                 test_name=None,
                 owner=None,
                 pipeline_status="SUCCESS",
                 api_env='development'):
        self.pipeline_name = pipeline_name
        self.build_id = build_id
        self.build_system = build_system
        self.product = product
        self.pipeline_build_number = pipeline_build_number
        self.jenkins_url = jenkins_url
        self.business_unit = bu
        self.title = title
        if not test_name:
            self.test_name = pipeline_name+'_'+self.build_system
        else:
            self.test_name = test_name
        self.owner = owner
        self.pipeline_status = pipeline_status
        if pipeline_status=="SUCCESS":
            self.test_status = "Passed"
        else:
            self.test_status = "Failed"
        if api_env == 'production':
            self.server_url = 'https://testdata.svc.eng.vmware.com'
        elif api_env == 'staging':
            self.server_url = 'https://testdata.svc-stage.eng.vmware.com'
        else:
            self.server_url = 'http://localhost:3001'

    def start_pipeline(self):
        result = requests.post(self.server_url + '/v1/api/testdata/start_pipeline', json={
            'bu': self.business_unit,
            'pipeline_name': self.pipeline_name,
            'pipeline_build_number': self.pipeline_build_number,
            'title': self.title,
            'jenkins_url': self.jenkins_url,
            'url': self.jenkins_url
        })
        check_http(result)
        return result.text

    def get_pipeline(self, pipeline_id):
        result = requests.get(self.server_url + '/v1/api/testdata/pipeline/{}'.format(pipeline_id))
        check_http(result)
        return result.json()

    def start_test(self, pipeline_id):
        result = requests.post(self.server_url + '/v1/api/testdata/start_test', json={
            'pipeline_fk': pipeline_id,
            'test_name': self.test_name,
            'product': self.product,
            'triage_owners': self.owner,
            'buildweb_id': self.build_id,
            'buildweb_system': self.build_system,
            'test_tag': 'build',
            'test_type': 'BUILD'
        })
        check_http(result)
        return result.text

    def get_test(self, test_fk):
        result = requests.get(self.server_url + '/v1/api/testdata/test/{}'.format(test_fk))
        check_http(result)
        return result.json()

    def finish_test(self, test_id, test_details, data={}, state_dump_filename=None):
        state_dump = None
        if state_dump_filename:
            with open(state_dump_filename, "r") as state_dump_file:
                state_dump = json.load(state_dump_file)
        finish_test_data = {
            'test_fk': test_id,
            'state_dump': state_dump,
            'change_details': [test_details],
            'result': self.test_status,
            'end_time': milli_time()
        }
        finish_test_data.update(data)
        result = requests.post(self.server_url + '/v1/api/testdata/finish_test_with_state_dump', json=finish_test_data)
        check_http(result)
        return result.text

    def finish_pipeline(self, pipeline_id, finish_data):
        final_products = []
        for product in finish_data['products']:
            del product['_update_time']
            del product['_add_time']
            if self.pipeline_status == "SUCCESS":
                product['pass_percentage'] = 100
                product['recommendation'] = True
                final_products.append(product)
            else:
                product['pass_percentage'] = 0
                product['recommendation'] = False
                final_products.append(product)
        finish_data['products'] = final_products

        data = {
            'pipeline_fk': pipeline_id,
            'status': self.pipeline_status
        }
        data.update(finish_data)
        result = requests.post(self.server_url + '/v1/api/testdata/finish_pipeline', json=data)
        check_http(result)
        return result.text


if __name__ == "__main__":
    args = get_args()
    uts_obj = Uts(pipeline_name=args.pipeline_name,
                  build_id=int(args.build_id),
                  build_system=args.build_system,
                  product=args.product,
                  pipeline_status=args.pipeline_status,
                  pipeline_build_number=args.pipeline_build_number,
                  jenkins_url=args.jenkins_url,
                  bu=args.bu,
                  title=args.title,
                  test_name=args.test_name,
                  owner=args.owner,
                  api_env=args.api_env)
    pipeline_fk = uts_obj.start_pipeline()
    test_fk = uts_obj.start_test(pipeline_id=pipeline_fk)

    test_data = uts_obj.get_test(test_fk)
    if 'test_details' in test_data:
        test_details = test_data['test_details']
    else:
        test_details = None
    uts_obj.finish_test(test_id=test_fk, test_details=test_details)
    pipeline_details = uts_obj.get_pipeline(pipeline_fk)
    data = uts_obj.finish_pipeline(pipeline_id=pipeline_fk, finish_data=pipeline_details)
    print(data)

"""
Sample execution command: 

python3 recommend_builds.py --pipeline_name=bundle_test --build_id=17102532 --build_system=ob --product=sddc-bundle

"""



