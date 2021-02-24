

H2A_total_direct_capital_cost = int(scaled_total_installed_cost)
cost_scaling_factor = 1                                            # combined plant scaling and escalation factor

     #------------Indirect Depreciable Capital Costs---------------------#
site_preparation = 0.02*H2A_total_direct_capital_cost/(CEPCI_inflator*consumer_price_inflator)*cost_scaling_factor
engineering_design = 0.1*H2A_total_direct_capital_cost/(CEPCI_inflator*consumer_price_inflator)*cost_scaling_factor
project_contingency = 0.15*H2A_total_direct_capital_cost/(CEPCI_inflator*consumer_price_inflator)*cost_scaling_factor
upfront_permitting_cost = 0.15*H2A_total_direct_capital_cost/(CEPCI_inflator*consumer_price_inflator)*cost_scaling_factor

total_depreciable_costs = int(H2A_total_direct_capital_cost + site_preparation + engineering_design + project_contingency + upfront_permitting_cost)

     #------------Non Depreciable Capital Costs---------------------#
cost_of_land = 50000                                              #($2016)/acre
land_required = 5                                                 #acres
land_cost = cost_of_land*land_required
other_nondepreciable_cost = 0

total_nondepreciable_costs = land_cost + other_nondepreciable_cost


total_capital_costs = total_depreciable_costs + total_nondepreciable_costs

      #--------------------------------------Fixed Operating Costs------------------------------------------------#
total_plant_staff = 10                                           #number of FTEs employed by plant
burdened_labor_cost = 50                                         #including overhead ($/man-hr)
labor_cost = total_plant_staff*burdened_labor_cost*2080          #($2016)/year

GA_rate = 20                                                     #percent labor cos (general and admin)
GA_cost = labor_cost*(GA_rate/100)                               #$/year
licensing_permits_fees = 0                                       #$/year
propertytax_insurancerate = 2                                    #percent of total capital investment per year
propertytax_insurancecost =  total_capital_costs*(propertytax_insurancerate/100)   #$/year
rent = 0                                                         #$/year
material_costs_for_maintenance = 0.03*H2A_total_direct_capital_cost/(CEPCI_inflator*consumer_price_inflator)
production_maintenance_and_repairs = 0                           #$/year
other_fees = 0                                                   #$/year
other_fixed_OM_costs = 0                                         #$/year

total_fixed_operating_costs = int(labor_cost + GA_cost + licensing_permits_fees + propertytax_insurancecost + rent \
        +  material_costs_for_maintenance + production_maintenance_and_repairs +  other_fees +  other_fixed_OM_costs)
    
    
    
    
    
    
    
    
    
    
    
    # H2['cap_factor'] = 0.97
    # H2['avg_production_rate'] = 50000                                                      # kgH2/day
    # H2['current_density'] = 2                                                              # A/cm^2
    # H2['voltage'] = 1.9                                                                    # V/cell
    # H2['operating_temp'] = 80                                                              # C
    # H2['H2_outlet_pressure'] = 450                                                         # psi
    # H2['cell_active_area'] = 450                                                           # cm^2
    # H2['cellperstack'] = 150                                                               # cells
    # H2['degradation_rate'] = 1.5                                                           # mV/1000 hrs
    # H2['stack_life'] = 7                                                                   # years
    # H2['stack_degradation_oversize'] = 0.13                                                # factor
    # H2['total_system_electrical_usage'] = 55.5                                                # kWh/kgH2
    # H2['stack_electrical_usage'] = 50.4                                                       # kWh/kgH2
    # H2['BoP_electrical_usage'] = 5.1                                                          # kWh/kgH2
    
    
    
    # H2['process_water_flowrate'] = 3.78
    # H2['system_unit_cost'] = 1.3                                                              # $/cm^2
    # H2['mechanical_BoP_unit_cost'] = 76                                                       # kWhH2/day
    # H2['electrical_BoP_cost'] = 82                                                            # $/kW
    # H2['current_year_for_capital_cost'] = 2016