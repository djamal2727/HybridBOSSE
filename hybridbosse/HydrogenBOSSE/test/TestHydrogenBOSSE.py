
from H2PlantCostTest import H2PlantCost
import pandas as pd

input_dict = dict()
input_dict['cap_factor'] = 0.97
input_dict['H2 Plant Electrical Input (kW)'] = 115625                                          # kW
input_dict['current_density'] = 2                                                              # A/cm^2
input_dict['voltage'] = 1.9                                                                    # V/cell
input_dict['operating_temp'] = 80                                                              # C
input_dict['H2_outlet_pressure'] = 450                                                         # psi
input_dict['cell_active_area'] = 450                                                           # cm^2
input_dict['cellperstack'] = 150                                                               # cells
input_dict['degradation_rate'] = 1.5                                                           # mV/1000 hrs
input_dict['stack_life'] = 7                                                                   # years
input_dict['stack_degradation_oversize'] = 0.13                                                # factor
input_dict['total_system_electrical_usage'] = 55.5                                                # kWh/kgH2
input_dict['stack_electrical_usage'] = 50.4                                                       # kWh/kgH2
input_dict['BoP_electrical_usage'] = 5.1                                                          # kWh/kgH2



input_dict['process_water_flowrate'] = 3.78
input_dict['system_unit_cost'] = 1.3                                                              # $/cm^2
input_dict['mechanical_BoP_unit_cost'] = 76                                                       # kWhH2/day
input_dict['electrical_BoP_cost'] = 82                                                            # $/kW
input_dict['current_year_for_capital_cost'] = 2016

input_dict['cost_of_land'] = 50000                                              #($2016)/acre
input_dict['land_required'] = 5                                                 #acres
input_dict['total_plant_staff'] = 10                                           #number of FTEs employed by plant
input_dict['burdened_labor_cost'] = 50                                         #including overhead ($/man-hr)
input_dict['propertytax_insurancerate'] = 2                                    #percent of total capital investment per year
#input_dict = pd.DataFrame.to_dict(input_df)

output_dict = dict()
        # self.H2PlantCost(input_dict=self.input_dict, output_dict=self.output_dict)


run_H2PlantCost = H2PlantCost(input_dict, output_dict)
run_H2PlantCost.run_module()

data = pd.DataFrame(list(output_dict.items()), columns= ['Category', 'Cost'])
data.loc['TOTAL']= data.sum(numeric_only=True, axis=0)

print(data)


