import yaml
import os
from hybridbosse.hybrids_shared_infrastructure.run_BOSSEs import run_BOSSEs
from hybridbosse.hybrids_shared_infrastructure.PostSimulationProcessing import PostSimulationProcessing
import pandas as pd


# Main API method to run a Hybrid BOS model:
def run_hybrid_BOS(hybrids_input_dict):
    """
    Returns a dictionary with detailed Shared Infrastructure BOS results.
    """
    wind_BOS, solar_BOS, hydrogen_BOS, H2_production_daily = run_BOSSEs(hybrids_input_dict)
    # Store a copy of both solar only and wind only outputs dictionaries:
    wind_only_BOS = wind_BOS.copy()
    solar_only_BOS = solar_BOS.copy()

    if hybrids_input_dict['hybrid_hydrogen_plant']:
        hydrogen_only_BOS = hydrogen_BOS.copy()
    else:
        hydrogen_only_BOS = 0

    print('wind_only_BOS at ', hybrids_input_dict['wind_plant_size_MW'], ' MW: ' , wind_BOS)
    print('solar_only_BOS ', hybrids_input_dict['solar_system_size_MW_DC'], ' MW: ' , solar_BOS)

    if hybrids_input_dict['hybrid_hydrogen_plant']:
        print('hydrogen_only_BOS ', hybrids_input_dict['solar_system_size_MW_DC'] + (hybrids_input_dict['num_turbines'] * hybrids_input_dict['turbine_rating_MW']) , \
          ' MW: ' , hydrogen_BOS)

    if hybrids_input_dict['wind_plant_size_MW'] > 0:
        # BOS of Wind only power plant:
        print('Wind BOS (USD/W): ', (wind_BOS['total_bos_cost'] /
                             (hybrids_input_dict['wind_plant_size_MW'] * 1e6)))
    else:
        wind_BOS['total_management_cost'] = 0

    if hybrids_input_dict['solar_system_size_MW_DC'] > 0:
        # BOS of Solar only power plant:
        print('Solar BOS (USD/W): ', (solar_BOS['total_bos_cost'] /
                              (hybrids_input_dict['solar_system_size_MW_DC'] * 1e6)))
    else:
        solar_BOS['total_management_cost'] = 0

    if hybrids_input_dict['hybrid_hydrogen_plant']:
        # BOS of Hydrogen only power plant:
        print('Hydrogen BOS (USD/kgH2): ', hydrogen_BOS['total_bos_cost']/(H2_production_daily*365))

    results = dict()
    results['hybrid'] = dict()
    hybrid_BOS = PostSimulationProcessing(hybrids_input_dict, wind_BOS, solar_BOS, hydrogen_BOS)
    results['hybrid']['hybrid_BOS_usd'] = hybrid_BOS.hybrid_BOS_usd
    results['hybrid']['hybrid_BOS_usd_watt'] = hybrid_BOS.hybrid_BOS_usd_watt

    if hybrids_input_dict['hybrid_hydrogen_plant']:
        results['hybrid']['hybrid_gridconnection_usd'] = 0
    else:
        results['hybrid']['hybrid_gridconnection_usd'] = hybrid_BOS.hybrid_gridconnection_usd

    results['hybrid']['hybrid_substation_usd'] = hybrid_BOS.hybrid_substation_usd

    results['hybrid']['hybrid_management_development_usd'] = wind_BOS['total_management_cost'] + \
                                                             solar_BOS['total_management_cost'] + \
                                                             hybrid_BOS.site_facility_usd

    results['Wind_BOS_results'] = hybrid_BOS.update_BOS_dict(wind_BOS, 'wind')
    results['Solar_BOS_results'] = hybrid_BOS.update_BOS_dict(solar_BOS, 'solar')
    return results, wind_only_BOS, solar_only_BOS, hydrogen_only_BOS


def read_hybrid_scenario(file_path):
    """
    [Optional method]

    Reads in default hybrid_inputs.yaml (YAML file) shipped with
    hybrids_shared_infrastructure, and returns a python dictionary with all required
    key:value pairs needed to run the hybrids_shared_infrastructure API.
    """
    if file_path:
        input_file_path = file_path['input_file_path']
        with open(input_file_path, 'r') as stream:
            data_loaded = yaml.safe_load(stream)
    else:
        input_file_path = os.path.dirname(__file__)
        with open(input_file_path + '/hybrid_inputs.yaml', 'r') as stream:
            data_loaded = yaml.safe_load(stream)

    hybrids_scenario_dict = data_loaded['hybrids_input_dict']

    if hybrids_scenario_dict['num_turbines'] is None or \
        hybrids_scenario_dict['num_turbines'] == 0:

        hybrids_scenario_dict['num_turbines'] = 0

    hybrids_scenario_dict['wind_plant_size_MW'] = hybrids_scenario_dict['num_turbines'] * \
                                                  hybrids_scenario_dict['turbine_rating_MW']

    hybrids_scenario_dict['hybrid_plant_size_MW'] = hybrids_scenario_dict['wind_plant_size_MW'] + \
                                                    hybrids_scenario_dict['solar_system_size_MW_DC']

    hybrids_scenario_dict['hybrid_construction_months'] = \
        hybrids_scenario_dict['wind_construction_time_months'] + \
        hybrids_scenario_dict['solar_construction_time_months']

    return hybrids_scenario_dict



yaml_file_path = dict()



def display_results(hybrid_dict, wind_only_dict, solar_only_dict, hydrogen_only_dict = None):

    hybrids_df = pd.DataFrame(hybrid_dict['hybrid'].items(), columns=['Type', 'USD'])

    hybrids_solar_df = pd.DataFrame(
        hybrid_dict['Solar_BOS_results'].items(), columns=['Type', 'USD'])

    hybrids_wind_df = pd.DataFrame(
        hybrid_dict['Wind_BOS_results'].items(), columns=['Type', 'USD'])

    solar_only_bos = dict()
    solar_only_bos['gridconnection_usd'] = solar_only_dict['total_transdist_cost']
    solar_only_bos['substation_cost'] = solar_only_dict['substation_cost']
    solar_only_bos['total_management_cost'] = solar_only_dict['total_management_cost']

    solar_only_bos_df = pd.DataFrame(
        solar_only_bos.items(), columns=['Solar Only BOS Component', 'USD'])

    wind_only_bos = dict()
    wind_only_bos['total_gridconnection_cost'] = wind_only_dict['total_gridconnection_cost']
    wind_only_bos['total_substation_cost'] = wind_only_dict['total_substation_cost']
    wind_only_bos['total_management_cost'] = wind_only_dict['total_management_cost']
    wind_only_bos_df = pd.DataFrame(
        wind_only_bos.items(), columns=['Wind Only BOS Component', 'USD'])

    if hydrogen_only_dict:
        hydrogen_only_bos = dict()
        #hydrogen_only_bos['scaled_installed_stack_capital_cost'] = hydrogen_only_dict['scaled_installed_stack_capital_cost']
        hydrogen_only_bos['scaled_installed_mechanical_BoP_cost'] = hydrogen_only_dict['scaled_installed_mechanical_BoP_cost']
        hydrogen_only_bos['scaled_installed_electrical_BoP_cost'] = hydrogen_only_dict['scaled_installed_electrical_BoP_cost']
        hydrogen_only_bos['site_preparation'] = hydrogen_only_dict['site_preparation']
        hydrogen_only_bos['engineering_design'] = hydrogen_only_dict['engineering_design']
        hydrogen_only_bos['project_contingency'] = hydrogen_only_dict['project_contingency']
        hydrogen_only_bos['upfront_permitting_cost'] = hydrogen_only_dict['upfront_permitting_cost']
        hydrogen_only_bos['land_cost'] = hydrogen_only_dict['land_cost']
        #hydrogen_only_bos['labor_cost'] = hydrogen_only_dict['labor_cost']
        #hydrogen_only_bos['licensing_permits_fees'] = hydrogen_only_dict['licensing_permits_fees']
        #hydrogen_only_bos['propertytax_insurancecost'] = hydrogen_only_dict['propertytax_insurancecost']
        hydrogen_only_bos_df = pd.DataFrame(
            hydrogen_only_bos.items(), columns=['Hydrogen Only BOS Component', 'USD'])

    else:
        hydrogen_only_bos = 0

    print(hybrids_df)
    print(solar_only_bos_df)
    print(wind_only_bos_df)
    if hydrogen_only_dict:
        print(hydrogen_only_bos_df)

    return hybrids_df, hybrids_solar_df, hybrids_wind_df, solar_only_bos, wind_only_bos, hydrogen_only_bos



hybrids_scenario_dict = read_hybrid_scenario(yaml_file_path)
hybrid_results, wind_only, solar_only, hydrogen_only = run_hybrid_BOS(hybrids_scenario_dict)
print(hybrid_results)
display_results(hybrid_results, wind_only_dict=wind_only, solar_only_dict=solar_only, hydrogen_only_dict=hydrogen_only)



