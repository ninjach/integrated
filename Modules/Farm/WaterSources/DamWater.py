import WaterSources

class DamWaterSource(WaterSources.WaterSources):

	def __init__(self, name, water_level):
		self.name = name
		self.water_level = water_level
	#End init()

#End DamWaterSource()