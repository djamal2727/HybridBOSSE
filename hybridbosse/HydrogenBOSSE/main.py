import os
import pandas as pd
from hybridbosse.HydrogenBOSSE.model.Manager import Manager


def run_hydrogenbosse(electrical_input):
    input_output_path = os.path.dirname(__file__)

    master_input = pd.read_excel(r'C:\Users\DJAMAL\Documents\GitHub\HybridBOSSE\hybridbosse\HydrogenBOSSE\project_list.xlsx', index = False)
    master_input.loc[0,'H2 Plant Electrical Input (kW)'] = electrical_input
    #master_input.loc[0,'cap_factor'] = 0.4
    output_dict = dict()

    # Manager class (1) manages the distribution of inout data for all modules
    # and (2) executes hydrogenbosse
    mc = Manager(input_dict=master_input, output_dict=output_dict)
    avg_production_rate, output_dict = mc.execute_hydrogenBOSSE()

    # results dictionary that gets returned by this function:
    results = dict()

    results['total_bos_cost'] = output_dict['total_bos_cost']
    #results['scaled_installed_stack_capital_cost'] = output_dict['scaled_installed_stack_capital_cost']
    results['scaled_installed_mechanical_BoP_cost'] = output_dict['scaled_installed_mechanical_BoP_cost']
    results['scaled_installed_electrical_BoP_cost'] = output_dict['scaled_installed_electrical_BoP_cost']
    results['site_preparation'] = output_dict['site_preparation']

    results['engineering_design'] = output_dict['engineering_design']
    results['project_contingency'] = output_dict['project_contingency']
    results['upfront_permitting_cost'] = output_dict['upfront_permitting_cost']
    results['land_cost'] = output_dict['land_cost']

    #results['labor_cost'] = output_dict['labor_cost']
    #results['licensing_permits_fees'] = output_dict['licensing_permits_fees']
    #results['propertytax_insurancecost'] = output_dict['propertytax_insurancecost']

    return avg_production_rate, results, output_dict



#<><><><><><><><> EXAMPLE OF RUNNING THIS HydrogenBOSSE API <><><><><><><><><><><>
##TODO: uncomment these lines to run SolarBOSSE as a standalone model.
#
# input_dict = dict()
# BOS_results = dict()
#
# input_dict['project_list'] = 'project_list_example'
#
# H2_production_daily, BOS_results, detailed_results = run_hydrogenbosse(electrical_input = 115625)
# print(BOS_results)
# bos_capex_total = BOS_results['total_bos_cost']
# bos_capex = bos_capex_total / (H2_production_daily*365)
# print('BOS CAPEX (USD/kgH2) = ' + str(round(bos_capex, 4)))
# print('')
# print('')

#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><
