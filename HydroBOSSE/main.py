import os
import pandas as pd
from HydroBOSSE.excelio.create_master_input_dict import XlsxReader
from LandBOSSE.landbosse.excelio.XlsxDataframeCache import XlsxDataframeCache
from HydroBOSSE.model.Manager import Manager


def run_hydrobosse(input_dictionary):
    input_output_path = os.path.dirname(__file__)
    # HydroBOSSE uses LandBOSSE's Excel I/O library for reading in data from Excel
    # files. Accordingly, the environment variables used in HydroBOSSE are called
    # LANDBOSSE_INPUT_DIR & LANDBOSSE_OUTPUT_DIR:
    os.environ["LANDBOSSE_INPUT_DIR"] = input_output_path
    os.environ["LANDBOSSE_OUTPUT_DIR"] = input_output_path

    project_data = read_data(input_dictionary['project_list'])
    xlsx_reader = XlsxReader()
    for _, project_parameters in project_data.iterrows():
        project_data_basename = project_parameters['Project data file']

        project_data_sheets = \
            XlsxDataframeCache.read_all_sheets_from_xlsx(project_data_basename)

        # make sure you call create_master_input_dictionary() as soon as
        # labor_cost_multiplier's value is changed.
    #if project_data_sheets.endswith('_df')
    #    input_dict[''] = pd.to_excel()

        master_input_dict = xlsx_reader.create_master_input_dictionary(
                                            project_data_sheets, project_parameters)

        master_input_dict['error'] = dict()

    # master_input_dict = dict()
    output_dict = dict()

    for key, _ in input_dictionary.items():
        master_input_dict[key] = input_dictionary[key]

    if 'grid_system_size_MW_DC' not in master_input_dict:
        master_input_dict['grid_system_size_MW_DC'] = master_input_dict['system_size_MW_DC']

    if 'grid_size_MW_AC' not in master_input_dict:
        master_input_dict['grid_size_MW_AC'] = \
            master_input_dict['system_size_MW_DC'] / master_input_dict['dc_ac_ratio']

    # Manager class (1) manages the distribution of inout data for all modules
    # and (2) executes hydrobosse
    mc_hydro = Manager(input_dict=master_input_dict, output_dict=output_dict)
    mc_hydro.execute_hydrobosse()

    # results dictionary that gets returned by this function:
    results = dict()
    results['errors'] = []
    if master_input_dict['error']:
        for key, value in master_input_dict['error'].items():
            msg = "Error in " + key + ": " + str(value)
            results['errors'].append(msg)
    else:   # if project runs successfully, return a dictionary with results
        # that are 3 layers deep (but 1-D)
        results['total_bos_cost'] = output_dict['total_bos_cost']
        # results['total_racking_cost'] = output_dict['total_racking_cost_USD']
        # results['siteprep_cost'] = output_dict['total_road_cost']
        # results['substation_cost'] = output_dict['total_substation_cost']
        # results['total_transdist_cost'] = output_dict['total_transdist_cost']
        # results['total_management_cost'] = output_dict['total_management_cost']
        # results['epc_developer_profit'] = output_dict['epc_developer_profit']
        # results['bonding_usd'] = output_dict['bonding_usd']
        # results['development_overhead_cost'] = output_dict['development_overhead_cost']
        # results['total_sales_tax'] = output_dict['development_overhead_cost']
        # results['total_foundation_cost'] = output_dict['total_foundation_cost']
        # results['total_erection_cost'] = output_dict['total_erection_cost']
        # results['total_collection_cost'] = output_dict['total_collection_cost']
        # results['total_bos_cost_before_mgmt'] = output_dict['total_bos_cost_before_mgmt']

    return results, output_dict


# This method reads in the two input Excel files (project_list; project_1)
# and stores them as data frames. This method is called internally in
# run_hydrobosse(), where the data read in is converted to a master input
# dictionary.
def read_data(file_name):
    path_to_project_list = os.path.dirname(__file__)
    sheets = XlsxDataframeCache.read_all_sheets_from_xlsx(file_name,
                                                          path_to_project_list)

    # If there is one sheet, make an empty data frame as a placeholder.
    if len(sheets.values()) == 1:
        first_sheet = list(sheets.values())[0]
        project_list = first_sheet

    # If the parametric and project lists exist, read them
    elif 'Project list' in sheets.keys():
        project_list = sheets['Project list']


    # Otherwise, raise an exception
    else:
        raise KeyError(
            "Project list needs to have a single sheet or sheets named "
            "'Project list' and 'Parametric list'."
        )

    return project_list


def read_weather_data(file_path):
    weather_data = pd.read_csv(file_path,
                               sep=",",
                               header=None,
                               skiprows=5,
                               usecols=[0, 1, 2, 3, 4]
                               )
    return weather_data


def read_hydro_data(file_path):
    # metadata = pd.read_excel(file_path, sheet_name='Metadata', index_col=0)
    # usacost = pd.read_excel('project_list_30MW.xlsx', sheet_name='USACost')
    usacost = pd.read_excel(file_path, sheet_name='USACost')

    # lcmcost = pd.read_excel('project_list_30MW.xlsx', sheet_name='LCMCosts')
    return usacost




class Error(Exception):
    """
        Base class for other exceptions
    """
    pass


class NegativeInputError(Error):
    """
        User entered a negative input. This is an invalid entry.
    """
    pass

# <><><><><><><><> EXAMPLE OF RUNNING THIS HydroBOSSE API <><><><><><><><><><><>
# TODO: uncomment these lines to run HydroBOSSE as a standalone model.

# sizes = [5, 50, 100]
# head_height = [20, 90, 250] #feet


project_types = ['Non-powered Dam', 'New Stream-reach Development',
                 'Canal/Conduit Project', 'Pumped Storage Hydropower Project', 'Unit Addition Project',
                 'Generator Rewind Project']

# Set project input parameters
size = 26  # MW
# Go to the closed roundup value [1 10 30 100]

head_height = 90  # feet

# Create input and output dictionaries
input_dict = dict()
BOS_results = dict()
BOS_results.update({str(size)+' MW scenario': ' '})

# Set input parameters
# input_dict['project_list'] = 'project_list_' + str(size) + 'MW'
input_dict['project_list'] = 'project_list_30MW'
input_dict['system_size_MW_DC'] = size
input_dict['grid_system_size_MW_DC'] = size
input_dict['grid_size_MW_AC'] = size
input_dict['head_height_ft'] = head_height
input_dict['greenfield_or_existing'] = 'greenfield'

for project_type in project_types:
    input_dict['project_type'] = project_type  # Non-powered Dam, New Stream-reach Development,\
    # Canal/Conduit Project, Pumped Storage Hydropower Project, Unit Addition Project, Generator Rewind Project

    # Run HydroBOSSE
    BOS_results, detailed_results = run_hydrobosse(input_dict)

    # Print Results
    print(BOS_results)
    bos_capex_total = BOS_results['total_icc_cost']
    bos_capex = bos_capex_total / (size * 1e6)
    print(str(size) + ' MW CAPEX (USD/Watt) = ' + str(round(bos_capex, 2)))

# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><
