import logging
from CDP.PMP.PMPDriver import *

class PMPDriverRunDiags(object):

        def __init__(self, parameter):
            self.parameter = parameter

        def calculate_level(self, var_split_name):
            #There is a height for the variable, ex: hus_850
            if len(var_split_name) > 1:
                self.level = float(var_split_name[-1]) * 100
            else:
                self.level = None

        def load_obs_dic(self):
            json_file_path = os.path.join(os.path.dirname(__file__),
                            'share', 'obs_info_dictionary.json')
            try:
                json_file = open(json_file_path)
            except IOError:
                logging.error('obs dictionary could not be loaded!')
                print 'obs dictionary could not be loaded!'
            except:
                logging.error('Unexpected error: %s' % sys.exc_info()[0])
                print 'Unexpected error: %s' % sys.exc_info()[0]

            self.obs_dic = json.loads(json_file.read())
            print type(self.obs_dic)

            json_file.close()

        def set_regrid_and_realm_from_obs_dic_using_var(self):
            if self.obs_dic[self.var][self.obs_dic[self.var]["default"]]["CMIP_CMOR_TABLE"] == "Omon":
                self.regrid_method = self.parameter.regrid_method_ocn
                self.regrid_tool = self.parameter.regrid_tool_ocn
                self.table_realm = 'Omon'
                self.realm = "ocn"
            else:
                self.regrid_method = self.parameter.regrid_method
                self.regrid_tool = self.parameter.regrid_tool
                self.table_realm = 'Amon'
                self.realm = "atm"

        def setup_metrics_dictionary(self):
            disclaimer_str = 'ADD DISCLAIMER TEXT SOON'
            self.metrics_dictionary['DISCLAIMER'] = disclaimer_str
            self.metrics_dictionary["RESULTS"] = collections.OrderedDict()

            self.metrics_dictionary["Variable"] = {}
            self.metrics_dictionary["References"] = {}
            self.metrics_dictionary["RegionalMasking"] = {}

        def run_diags(self):
            for var_long_name in self.parameter.vars:
                self.metrics_def_dictionary = collections.OrderedDict()
                self.metrics_dictionary = collections.OrderedDict()
                self.setup_metrics_dictionary()

                self.obs_dic = {}
                self.load_obs_dic()

                var_name_split = var_long_name.split('_')
                self.calculate_level(var_name_split)
                self.var = var_name_split[0]

                self.set_regrid_and_realm_from_obs_dic_using_var()