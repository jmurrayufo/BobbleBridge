# Power Node Simulation Thing

class PowerNode:

    ColdPlasma = 0
    HotPlasma  = 0

    ColdPlasmaRate = 0
    HotPlasmaRate  = 0

    PlasmaCoolingRate  = 0
    PlasmaHeatingRate  = 0

    def __init__ (self,CurrentCold,CurrentHot):
        self.ColdPlasma = CurrentCold;
        self.HotPlasma  = CurrentHot;

    def __init__ (self, ColdCap, HotCap, ColdRate, HotRate):
        self.ColdPlasmaCapacity = ColdCap
        self.HotPlasmaCapacity  = HotCap

        self.ColdPlasmaRate     = ColdRate
        self.HotPlasmaRate      = HotRate

    def coldPlasmaRoom ():
        return ColdPlasmaCapacity - ColdPlasma

    def hotPlasmaRoom ():
        return HotPlasmaCapacity - HotPlasma

    def addColdPlasma (self, NewColdPlasma):
        self.ColdPlasma += NewColdPlasma

    def addHotPlasma (self, NewHotPlasma):
        self.HotPlasma += NewHotPlasma

    def processPlasma (TimeFactor): # This Function will be used to cause a node to heat/cool the plasma which it contains
        if self.PlasmaCoolingRate>0:
            if self.HotPlasma >= self.PlasmaCoolingRate*TimeFactor and self.ColdPlasma + self.PlasmaCoolingRate*TimeFactor <= ColdPlasmaCapacity:
                self.HotPlasma -= self.PlasmaCoolingRate*TimeFactor
                self.ColdPlasma += self.PlasmaCoolingRate*TimeFactor
            else: if self.HotPlasma < self.PlasmaCoolingRate*TimeFactor and self.ColdPlasma + self.PlasmaCoolingRate*TimeFactor <= ColdPlasmaCapacity:
                self.ColdPlasma += self.HotPlasma
                self.HotPlasma = 0
            else: if self.HotPlasma >= self.PlasmaCoolingRate*TimeFactor and self.ColdPlasma + self.PlasmaCoolingRate*TimeFactor > ColdPlasmaCapacity:
                diff = self.ColdPlasmaCapacity - self.ColdPlasma
                self.HotPlasma -= diff
                self.ColdPlasma = self.ColdPlasmaCapacity
            else: if self.HotPlasma <= (self.ColdPlasmaCapacity - self.ColdPlasma):
                self.ColdPlasma += self.HotPlasma
                self.HotPlasma = 0
            else: if self.HotPlasma > (self.ColdPlasmaCapacity - self.ColdPlasma):
                diff = self.ColdPlasmaCapacity - self.ColdPlasma
                self.ColdPlasma = self.ColdPlasmaCapacity
                self.HotPlasma -= diff
            else:
                print 'An Error Has been encountered in PowerNode.processPlasma, Cooling Rate Calculations'
        # Some sort of messaging needs to be added to this function so that systems which derive power from the 'Cooling' or plasma have the approriate amount of power added to the current operation
        if self.PlasmaHeatingRate>0:
            if self.ColdPlasma >= self.PlasmaHeatingRate*TimeFactor and self.HotPlasma + self.PlasmaHeatingRate*TimeFactor <= HotPlasmaCapacity:
                self.ColdPlasma -= self.PlasmaHeatingRate*TimeFactor
                self.HotPlasma += self.PlasmaHeatingRate*TimeFactor
            else: if self.ColdPlasma < self.PlasmaHeatingRate*TimeFactor and self.HotPlasma + self.PlasmaHeatingRate*TimeFactor <= HotPlasmaCapacity:
                self.HotPlasma += self.ColdPlasma
                self.ColdPlasma = 0
            else: if self.ColdPlasma >= self.PlasmaHeatingRate*TimeFactor and self.HotPlasma + self.PlasmaHeatingRate*TimeFactor > HotPlasmaCapacity:
                diff = self.HotPlasmaCapacity - self.HotPlasma
                self.ColdPlasma -= diff
                self.HotPlasma = self.HotPlasmaCapacity
            else: if self.ColdPlasma <= (self.HotPlasmaCapacity - self.HotPlasma):
                self.HotPlasma += self.ColdPlasma
                self.ColdPlasma = 0
            else: if self.ColdPlasma > (self.HotPlasmaCapacity - self.HotPlasma):
                diff = self.HotPlasmaCapacity - self.HotPlasma
                self.HotPlasma = self.HotPlasmaCapacity
                self.ColdPlasma -= diff
            else:
                print 'An Error Has been encountered in PowerNode.processPlasma, Heating Rate Calculations'

    def exchange ():
        return 
    
class Regulator(PowerNode):

    generator = []
    tank = []
    system = []
    
    def addGenerator (self, FlowRate):
        generator.append(Generator(FlowRate))

    def addTank (self, ColdCap, HotCap, ColdRate, HotRate):
        system.append(Tank(ColdCap, HotCap, ColdRate, HotRate))

    def addSystem (self, ColdCap, HotCap, ColdRate, HotRate):
        system.append(System(ColdCap, HotCap, ColdRate, HotRate))

    def update (self,TimeStep):
        for x in generator:
            x.processPlasma(TimeStep)
        for x in tank:
            x.processPlasma(TimeStep)
        for x in system:
            x.processPlasma(TimeStep)

        TotalColdPressure = 0
        TotalHotPressure  = 0
        for x in generator:
            TotalColdPressure += x.ColdPlasmaRate* TimeStep
            TotalHotPressure  += x.HotPlasmaRate * TimeStep
        for x in system:
			TotalColdPressure += x.ColdPlasmaRate * TimeStep
			TotalHotPressure  += x.HotPlasmaRate  * TimeStep
			
		# The Following Routines Will Attempt to use the Tanks to Equalize the Pressure in The System
		if TotalHotPressure > 0:
			# Push Plasma into Tanks
			if TotalHotPressure > 0:
				# Pressure has exceeded System Capacity, vent the excess Pressure from this timestep.
		else: if TotalHotPressure < 0:
			# Push Pull Plasma From Tanks
		else:
			# Neither Pull Nor Push Plasma From the Tanks
			
		if TotalColdPressure > 0:
			# Push Plasma into Tanks
			if TotalColdPressure > 0:
				#pressure has exceeded System Capacity, vent the excess Pressure from this timestep
		else: if TotalHotPressure < 0:
			# Pull Plasma from Tanks
		else:
			#Neither Push nor pull pressure from Tanks
			


class Generator(PowerNode):
    def __init__ (self, FlowRate):
        PlasmaFlowRate = FlowRate

class Tank(PowerNode):

class System(PowerNode):



