"""
This is defined to parse excel sheet to json
"""
from os.path import join
import json
import re
from xlutils.view import View

class ExcelParser(object):

    def __init__(self):
        self.view = None
        self.data_dict = dict()
        self.group = None
        self.default_value = None
        self.supplied_value = None
        self.parameter = None
        self.nested_parameter = None
        self.json_output = None

    def create_json(self):
        sheet_names = self.view.book.sheet_names()
        for index in range(1, len(sheet_names)-1):
            # print('processing {0} sheet'.format(sheet_names[index]))
            sheet = self.view.book.sheet_by_index(index)
            for row in sheet.get_rows():
                if row[0].value == 'Description':
                    # print('skipping first row')
                    continue
                # print('{0}'.format(row[2].value))
                # print('IS boolean: {0}'.format(isinstance(row[2].value, bool)))
                self.supplied_value = str(row[1].value)
                self.supplied_value = re.sub('\\\\', '/', self.supplied_value)
                self.default_value = str(row[2].value)
                # if self.supplied_value.strip():
                #     self.param_value = self.supplied_value
                # else:
                #     self.param_value = self.default_value
                # checking if supplied or default values are istance of integer
                try:
                    if self.supplied_value:
                        f = float(self.supplied_value)
                        self.supplied_value = int(f)
                    if self.default_value:
                        f = float(self.default_value)
                        self.default_value = int(f)

                except ValueError as v:
                    pass

                self.group = str(row[3].value).replace(' ', '_').lower()
                self.parameter = str(row[4].value).replace(' ', '_').lower()
                self.nested_parameter = str(row[5].value).replace(' ', '_')
                if self.group not in self.data_dict:
                    self.data_dict[self.group] = {}
                if self.nested_parameter:
                    if self.parameter not in self.data_dict[self.group]:
                        if self.group == 'vcenter_details' and self.parameter == 'esxi_hosts':
                            continue
                        self.data_dict[self.group][self.parameter] = {}
                    if self.supplied_value:
                        self.data_dict[self.group][self.parameter][self.nested_parameter] = \
                            self.supplied_value
                    else:
                        self.data_dict[self.group][self.parameter][self.nested_parameter] = \
                            self.default_value
                else:
                    if self.supplied_value:
                        self.data_dict[self.group][self.parameter] = \
                            self.supplied_value
                    else:
                        self.data_dict[self.group][self.parameter] = \
                            self.default_value

            count = 0
            temp_dict = dict()
            tem_list = list()
            if sheet_names[index] == 'EHC_vCenter':
                # print 'will be processing vsphere host details'
                sheet = self.view.book.sheet_by_index(index)
                for row in sheet.get_rows():
                    if row[0].value == 'Description':
                      # print('skipping first row')
                      continue
                    self.supplied_value = str(row[1].value)
                    self.supplied_value = re.sub('\\\\', '/', self.supplied_value)
                    self.default_value = str(row[2].value)
                    self.group = str(row[3].value).replace(' ', '_').lower()
                    self.parameter = str(row[4].value).replace(' ', '_').lower()
                    self.nested_parameter = str(row[5].value).replace(' ', '_')

                    if self.parameter != 'esxi_hosts':
                        # print 'continuing for unwanted lines'
                        continue
                    # if not self.supplied_value and not self.default_value:
                    #     print 'continuing for empty value'
                    #     print row
                    #     continue
                    else:
                        # print self.supplied_value
                        if self.group not in self.data_dict:
                            self.data_dict[self.group] = {}

                        if self.parameter:
                            if self.parameter not in self.data_dict[self.group]:
                                # print 'creating list'
                                self.data_dict[self.group][self.parameter] = []

                        if count == 0:
                            if self.supplied_value:
                                temp_dict['esxiName'] = self.supplied_value
                            else:
                                temp_dict['esxiName'] = self.default_value
                            count = 1
                        elif count == 1:
                            if self.supplied_value:
                                temp_dict['hostName'] = self.supplied_value
                            else:
                                temp_dict['hostName'] = self.default_value

                            self.data_dict[self.group][self.parameter].append(temp_dict)
                            tem_list.append(temp_dict)
                            count = 0
                            temp_dict = dict()


        # Handleing the boolean values
        if self.data_dict['active_directory']['use_ssl']:
            self.data_dict['active_directory']['use_ssl'] = True
        else:
            self.data_dict['active_directory']['use_ssl'] = False

        if self.data_dict['vrealize_automation']['merger_restriction']:
            self.data_dict['vrealize_automation']['merger_restriction'] = True
        else:
            self.data_dict['vrealize_automation']['merger_restriction'] = False

        if self.data_dict['smtp']['auth_required']:
            self.data_dict['smtp']['auth_required'] = True
        else:
            self.data_dict['smtp']['auth_required'] = False

        if self.data_dict['smtp']['enable_starttls']:
            self.data_dict['smtp']['enable_starttls'] = True
        else:
            self.data_dict['smtp']['enable_starttls'] = False

        if self.data_dict['smtp']['ssl']:
            self.data_dict['smtp']['ssl'] = True
        else:
            self.data_dict['smtp']['ssl'] = False

        if self.data_dict['smtp']['self_signed_certificate_accepted']:
            self.data_dict['smtp']['self_signed_certificate_accepted'] = True
        else:
            self.data_dict['smtp']['self_signed_certificate_accepted'] = False

        self.json_output = json.dumps(self.data_dict, ensure_ascii=False)
        return self.json_output

    def get_sheet_view(self, sheet_dir, sheet_name):
        self.view = View(join(sheet_dir, sheet_name))

# if __name__ == '__main__':
#     print ('checking excel parser')
#     sh = ExcelParser()
#     sh.get_sheet_view(r'C:\Users\volups\Desktop\excel_parser', 'EHC_VxRail_AutoDeploy_inputs_v1.3_filled.xlsx')
#     json_file = sh.create_json()
#     from pprint import pprint
#     pprint(json_file)
#     with open('test.json', 'w') as wr:
#         wr.write(str(json_file))
