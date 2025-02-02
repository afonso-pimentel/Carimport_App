class UnitConverter:
    @staticmethod
    def kw_to_hp(kw):
        """Convert kilowatts to horsepower."""
        hp = kw * 1.34102
        return int(hp) 

    @staticmethod
    def hp_to_kw(hp):
        """Convert horsepower to kilowatts."""
        kw = hp / 1.34102
        return int(kw)