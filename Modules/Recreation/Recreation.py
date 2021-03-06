# Recreatoin.py

class Recreation:
    """
    Generate recreation value of Lake Eppalock
    Input: Daily dam storage/water level at Lake Eppalock
    Output: index based recreation value for the Lake Eppalock
    """
    def recreationIndex(self, dam_storage, threshold):
        """
        give index based on dam storage, can be a series of if-then, or curve
        """
        if dam_storage < threshold:
            recreation_index=0
        else:
            recreation_index = 1
        return recreation_index