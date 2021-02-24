import traceback
import math
from .H2PlantCost import H2PlantCost


class Manager:
    """
    The Manager class distributes input and output dictionaries among
    the various modules. It maintains the hierarchical dictionary
    structure.
    """

    def __init__(self, input_dict, output_dict):
        """
        This initializer sets up the instance variables of:

        self.cost_modules: A list of cost module instances. Each of the
            instances must implement the method input_output.

        self.input_dict: A placeholder for the inputs dictionary

        self.output_dict: A placeholder for the output dictionary
        """
        self.input_dict = input_dict
        self.output_dict = output_dict

    def execute_hydrogenBOSSE(self):


        PlantCost = H2PlantCost(input_dict=self.input_dict, output_dict=self.output_dict)
        avg_production_rate, self.input_dict, self.output_dict = PlantCost.run_module()



        self.output_dict['total_bos_cost'] = \
            self.output_dict['scaled_installed_mechanical_BoP_cost'] + \
            self.output_dict['scaled_installed_electrical_BoP_cost'] + \
            self.output_dict['site_preparation'] + \
            self.output_dict['engineering_design'] + \
            self.output_dict['project_contingency'] + \
            self.output_dict['upfront_permitting_cost'] + \
            self.output_dict['land_cost']
            #self.output_dict['labor_cost'] + \
            #self.output_dict['licensing_permits_fees'] + \
           # self.output_dict['propertytax_insurancecost'] + \
        # self.output_dict['scaled_installed_stack_capital_cost'] + \

        return avg_production_rate, self.output_dict

