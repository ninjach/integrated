from __future__ import division
from integrated.Modules.Core.IntegratedModelComponent import Component

class FarmComponent(Component):

	"""
	Interface Class for Farm Components.
	All methods defined here should be redefined by implementing child classes.
	"""

	def __init__(self, implemented=False):
		self.implemented = implemented
	#End init()

	def calcTotalCostsPerHa(self):
		pass
	#End calcTotalCosts()

	def calcGrossMarginsPerHa(self):
		pass
	#End calcGrossMargins()

	def calcOperationalCostPerHa(self):
		pass
	#End calcOperationalCostPerHa()

	def calcImplementationCostPerHa(self):
		pass
	#End calcImplementationCostPerHa()

	def annualizeCapital(self, capital, discount_rate=0.07, num_years=20):

	    """
	    Calculates capital value per year over a given number of years

	    :param capital: Amount of money in dollars ($)
	    :param discount_rate: The percentage to discount future value to get present-day value; Arshad et al. (2013) used 7%
	    :param num_years: Number of years for the scenario
	    :returns: Annualised capital cost discounted to present day value 
	    :return type: numeric
	    
	    """

	    annuity_factor = (1 - 1/(1 + discount_rate)**num_years)/discount_rate

	    return capital/annuity_factor

	#End calcCapitalCostPerYear()