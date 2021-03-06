"""
Example use of Linear Programming for determining irrigated area that maximises profits

Function to be optimised takes the form of negated sum of profits multiplied by area.
This is then constrained by:
  
  Available water resources

  Available land

Profits are negated as the solver attempts to minimize

:math:`f(x) = P_{1}*x_{1} + P_{2}*x_{2} + P_{3}*x_{3}  ... + P_{n}*x_{n}`, where :math:`P` is negated profits and :math:`x_{n}` represents possible area

:math:`x_{1} + x_{2} + x_{3} ... + x_{n} = A`, where :math:`A` is total available area

:math:`W_{1}*x_{1} + W_{2}*x_{2} + W_{3}*x_{3}  ... + W_{n}*x_{n} \leqslant AW`, where :math:`AW` is Available Water, :math:`W` is required water per Ha for each enterprise

:math:`0 \leq x_{1,2,3 ... n} \leq A`

Each :math:`x` therefore represents a combination of soil, crop, irrigation, water source, and soil characteristics

Example::

	area = 300 #Maximum possible area for irrigation

	tomato_cost = Tomato.variable_cost_per_Ha + flood_infra_cost + (pumping_cost*Tomato.water_use_ML_per_Ha)
	wheat_cost = Wheat.variable_cost_per_Ha + flood_infra_cost + (pumping_cost*Wheat.water_use_ML_per_Ha)
	canola_cost = Canola.variable_cost_per_Ha + flood_infra_cost + (pumping_cost*Canola.water_use_ML_per_Ha)

	tomato_profit = Tomato.price_per_yield * Tomato.yield_per_Ha
	wheat_profit = Wheat.price_per_yield * Wheat.yield_per_Ha
	canola_profit = Canola.price_per_yield * Canola.yield_per_Ha

	#Negated profit of each crop type
	c = [(wheat_cost-wheat_profit), (canola_cost-canola_profit), (tomato_cost-tomato_profit)] #variables to minimize

	#Constrain by total area
	A_eq = [[1, 1, 1]] #1*x[1] + 1*x[2] + 1*x[3] ... + 1*x[n] = Total Area
	b_eq = [area]

	#Here, x represents irrigated area for each crop
	#So the negated profit * area is being minimized

	#Costs per Ha of producing the negated profit
	A_ub = [
		[Wheat.water_use_ML_per_Ha, Canola.water_use_ML_per_Ha, Tomato.water_use_ML_per_Ha],
	]

	#Constraints to producing negated profit 
	b_ub = [
		water_entitlement
	]

	bounds = [(0, area), (0, area), (0, area)]

	res = lp(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub, bounds=bounds, options={"disp": True})

	Optimization terminated successfully.
	         Current function value: -3791700.000000
	         Iterations: 2
	  status: 0
	   slack: array([ 200.,  300.,  300.,    0.])
	 success: True
	     fun: -3791700.0
	       x: array([   0.,    0.,  300.])
	 message: 'Optimization terminated successfully.'
	     nit: 2

"""

# from scipy.optimize import linprog as lp

# c = [-500, -400, -600, -350]
# A_ub = [[1, 1, 0, 0], [0, 0, 1, 1]]
# b_ub = [50, 45]
# bounds = ((0, 95), ) * 4

# x = lp(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds)
# print x

if __name__ == '__main__':

	from setup_dev import *

	from scipy.optimize import linprog as lp
	from setup_dev import *
	from Crops.CropInfo import CropInfo

	Tomato = CropInfo(**crop_params['Processing Tomato'].getParams())
	Wheat = CropInfo(**crop_params['Irrigated Winter Wheat'].getParams())
	Canola = CropInfo(**crop_params['Irrigated Winter Canola'].getParams())

	crops = [Tomato, Wheat, Canola]

	area = 300 #Hectares
	water_price = 250 #per ML
	water_sold =  0 #Amount of water Sold (ML)
	water_bought = 0
	flood_infra_cost = Flood.maintenance_rate * Flood.cost_per_Ha if Flood.cost_per_Ha != 0.0 else Flood.maintenance_rate * Flood.replacement_cost_per_Ha

	spray_infra_cost = 120

	pumping_cost = 35 #$/ML

	ongoing_cost = 2700 #per Hectare
	water_entitlement = 2000 #ML

	tomato_cost = Tomato.variable_cost_per_Ha + flood_infra_cost + pumping_cost
	wheat_cost = Wheat.variable_cost_per_Ha + flood_infra_cost + pumping_cost
	canola_cost = Canola.variable_cost_per_Ha + flood_infra_cost + pumping_cost

	tomato_profit = Tomato.price_per_yield * Tomato.yield_per_Ha
	wheat_profit = Wheat.price_per_yield * Wheat.yield_per_Ha
	canola_profit = Canola.price_per_yield * Canola.yield_per_Ha

	#Negated profit of each crop type
	c = [(wheat_cost-wheat_profit), (canola_cost-canola_profit), (tomato_cost-tomato_profit)] #variables to minimize

	#Constrain by total area
	A_eq = [[1, 1, 1]] #1*x[1] + 1*x[2] + 1*x[3] ... + 1*x[n] = Total Area
	b_eq = [area]

	#Costs per Ha of producing the negated profit
	# A_ub = [
	# 	[Wheat.water_use_ML_per_Ha, Canola.water_use_ML_per_Ha, Tomato.water_use_ML_per_Ha],
	# ]

	A_ub = [Wheat.water_use_ML_per_Ha, Canola.water_use_ML_per_Ha, Tomato.water_use_ML_per_Ha]

	#Constraints to producing negated profit 
	b_ub = [
		water_entitlement
	]

	bounds = [(0, area), (0, area), (0, area)]

	res = lp(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub, bounds=bounds, options={"disp": True})

	print(res)

	print c
	print A_ub
	print b_ub

	# print (tomato_cost - tomato_profit) * area
	# print (wheat_cost - wheat_profit) * area
	# print (canola_cost - canola_profit) * area



