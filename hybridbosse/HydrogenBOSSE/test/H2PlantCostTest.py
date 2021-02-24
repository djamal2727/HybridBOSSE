

import math
import pandas as pd
import numpy as np


class H2PlantCost:

    def __init__(self, input_dict, output_dict):

        self.input_dict = input_dict
        self.output_dict = output_dict

    def Calc_Electrolyzer_Cost(self, input_dict):
#---------------------------------------------------H2A PROCESS FLOW----------------------------------------------------------#
        avg_production_rate = input_dict['H2 Plant Electrical Input (kW)']/(input_dict['total_system_electrical_usage'] / 24)
        hours_per_stack_life = input_dict['stack_life']*365*24*input_dict['cap_factor']                              # hrs/life
        degradation_rate_Vperlife = hours_per_stack_life*input_dict['degradation_rate']/1000           # V/life
        peak_production_rate = avg_production_rate*(1+input_dict['stack_degradation_oversize'])        # kgH2/day

        total_active_area = math.ceil((avg_production_rate/2.02*1000/24/3600)*2*96485/input_dict['current_density']/(100**2))           # m^2
        total_active_area_degraded= math.ceil((peak_production_rate/2.02*1000/24/3600)*2*96485/input_dict['current_density']/(100**2)) # m^2



        total_system_input = input_dict['total_system_electrical_usage']/24*peak_production_rate/1000     #MW
        stack_input_power = input_dict['stack_electrical_usage']/24*peak_production_rate/1000             #MW


        stack_system_cost = input_dict['system_unit_cost']/(input_dict['current_density']*input_dict['voltage'])*1000                 # $/kW
        mechanical_BoP_cost= 76*peak_production_rate/stack_input_power/1000                # $/kW
        total_system_cost_perkW = stack_system_cost+mechanical_BoP_cost+input_dict['electrical_BoP_cost'] # $/kW

        total_system_cost = total_system_cost_perkW * stack_input_power * 1000              # $
        return avg_production_rate, peak_production_rate, total_active_area_degraded, stack_input_power, total_system_cost

    def ScaledPlantCost(self, input_dict, output_dict):
    #-------------------------------------------------CAPITAL COST--------------------------------------------------------------#
        avg_production_rate, peak_production_rate, total_active_area_degraded, stack_input_power, total_system_cost = H2PlantCost.Calc_Electrolyzer_Cost(self, input_dict)

        gdpdef = {'Year':[2015,2016,2017,2018,2019,2020], 'CEPCI':[104.031,104.865,107.010,109.237,111.424,113.415]}      #GDPDEF (2012=100), https://fred.stlouisfed.org/series/GDPDEF/
        CEPCI = pd.DataFrame(data=gdpdef)                                                                                    #Deflator Table

        pci = {'Year':[2015,2016,2017,2018,2019,2020], 'PCI':[556.8, 541.7, 567.5, 603.1, 607.5, 610]}     #plant cost index, Chemical Engineering Magazine
        CPI = pd.DataFrame(pci)

        baseline_plant_design_capacity = avg_production_rate
        basis_year_for_capital_cost = 2016
        CEPCI_inflator = int((CEPCI.loc[CEPCI['Year']==input_dict['current_year_for_capital_cost'],'CEPCI']))/int((CEPCI.loc[CEPCI['Year']==basis_year_for_capital_cost,'CEPCI']))
        consumer_price_inflator = int(CPI.loc[CPI['Year']==input_dict['current_year_for_capital_cost'],'PCI'])/int(CPI.loc[CPI['Year']==basis_year_for_capital_cost,'PCI'])                   #lookup


    #--------------------------CAPITAL INVESTMENT---------------------------------#
    #----Inputs required in basis year (2016$)----#

        baseline_uninstalled_stack_capital_cost = CEPCI_inflator*consumer_price_inflator*input_dict['system_unit_cost']*total_active_area_degraded*100**2       #($2016)
        stack_installation_factor = 1.12
        baseline_installed_stack_capital_cost = stack_installation_factor*baseline_uninstalled_stack_capital_cost

        baseline_uninstalled_mechanical_BoP_cost = CEPCI_inflator*consumer_price_inflator*input_dict['mechanical_BoP_unit_cost']*peak_production_rate              #($2016)
        mechanical_BoP_installation_factor = 1
        baseline_installed_mechanical_BoP_cost = mechanical_BoP_installation_factor*baseline_uninstalled_mechanical_BoP_cost

        baseline_uninstalled_electrical_BoP_cost = CEPCI_inflator*consumer_price_inflator*input_dict['electrical_BoP_cost']*stack_input_power*1000             #($2016)
        electrical_BoP_installation_factor = 1.12
        baseline_installed_electrical_BoP_cost = electrical_BoP_installation_factor*baseline_uninstalled_electrical_BoP_cost

        baseline_total_installed_cost = baseline_installed_stack_capital_cost + baseline_installed_mechanical_BoP_cost + baseline_installed_electrical_BoP_cost


    #------------------------------------------------PLANT SCALING-------------------------------------------------------------------#

        scale_ratio = 1                            #ratio of new design capacity to baseline design capacity (linear scaling)
        scale_factor = 1                           #rato of total scaled installed capital cost to total baseline installed capital cost (exponential scaling)
        default_scaling_factor_exponent = 1        #discrepancy
        lower_limit_for_scaling_capacity = 20000   #kgH2/day
        upper_limit_for_scaling_capacity = 200000  #kgH2/day

        scaled_uninstalled_stack_capital_cost = baseline_uninstalled_stack_capital_cost**default_scaling_factor_exponent
        output_dict['scaled_installed_stack_capital_cost'] = scaled_uninstalled_stack_capital_cost * stack_installation_factor

        scaled_uninstalled_mechanical_BoP_cost = baseline_uninstalled_mechanical_BoP_cost**default_scaling_factor_exponent
        output_dict['scaled_installed_mechanical_BoP_cost'] = scaled_uninstalled_mechanical_BoP_cost * mechanical_BoP_installation_factor

        scaled_uninstalled_electrical_BoP_cost = baseline_uninstalled_electrical_BoP_cost**default_scaling_factor_exponent
        output_dict['scaled_installed_electrical_BoP_cost'] = scaled_uninstalled_electrical_BoP_cost * electrical_BoP_installation_factor

        scaled_total_installed_cost = output_dict['scaled_installed_stack_capital_cost'] + output_dict['scaled_installed_mechanical_BoP_cost'] + output_dict['scaled_installed_electrical_BoP_cost']

        return scaled_total_installed_cost, CEPCI_inflator, consumer_price_inflator, output_dict

    def H2CapitalCost(self, input_dict, output_dict):
        scaled_total_installed_cost, CEPCI_inflator, consumer_price_inflator, output_dict = H2PlantCost.ScaledPlantCost(self, input_dict, output_dict)
        H2A_total_direct_capital_cost = int(scaled_total_installed_cost)
        cost_scaling_factor = 1                                            # combined plant scaling and escalation factor

     #------------Indirect Depreciable Capital Costs---------------------#
        output_dict['site_preparation'] = 0.02*H2A_total_direct_capital_cost/(CEPCI_inflator*consumer_price_inflator)*cost_scaling_factor
        output_dict['engineering_design'] = 0.1*H2A_total_direct_capital_cost/(CEPCI_inflator*consumer_price_inflator)*cost_scaling_factor
        output_dict['project_contingency'] = 0.15*H2A_total_direct_capital_cost/(CEPCI_inflator*consumer_price_inflator)*cost_scaling_factor
        output_dict['upfront_permitting_cost'] = 0.15*H2A_total_direct_capital_cost/(CEPCI_inflator*consumer_price_inflator)*cost_scaling_factor

        total_depreciable_costs = int(H2A_total_direct_capital_cost + output_dict['site_preparation'] + output_dict['engineering_design'] + output_dict['project_contingency'] + output_dict['upfront_permitting_cost'])

     #------------Non Depreciable Capital Costs---------------------#

        output_dict['land_cost'] = input_dict['cost_of_land']*input_dict['land_required']
        other_nondepreciable_cost = 0

        total_nondepreciable_costs = output_dict['land_cost'] + other_nondepreciable_cost

        total_capital_costs = total_depreciable_costs + total_nondepreciable_costs

      #--------------------------------------Fixed Operating Costs------------------------------------------------#

        output_dict['labor_cost'] = input_dict['total_plant_staff']*input_dict['burdened_labor_cost']*2080          #($2016)/year

        input_dict['GA_rate'] = 20                                                     #percent labor cos (general and admin)
        output_dict['GA_cost'] = output_dict['labor_cost']*(input_dict['GA_rate']/100)                               #$/year
        output_dict['licensing_permits_fees'] = 0                                       #$/year

        output_dict['propertytax_insurancecost'] =  total_capital_costs*(input_dict['propertytax_insurancerate']/100)   #$/year
        rent = 0                                                         #$/year
        material_costs_for_maintenance = 0.03*H2A_total_direct_capital_cost/(CEPCI_inflator*consumer_price_inflator)
        production_maintenance_and_repairs = 0                           #$/year
        other_fees = 0                                                   #$/year
        other_fixed_OM_costs = 0                                         #$/year

        total_fixed_operating_costs = int(output_dict['labor_cost'] + output_dict['GA_cost'] + output_dict['licensing_permits_fees'] + output_dict['propertytax_insurancecost'] + rent \
        +  material_costs_for_maintenance + production_maintenance_and_repairs +  other_fees +  other_fixed_OM_costs)
        #return site_preparation, engineering_design, project_contingency, upfront_permitting_cost, land_cost, labor_cost,

    def run_module(self):
        self.ScaledPlantCost(self.input_dict, self.output_dict)
        self.H2CapitalCost(self.input_dict, self.output_dict)
        return self.input_dict, self.output_dict








