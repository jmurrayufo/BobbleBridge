# Power Node Simulation Thing

class PowerNode:

    ColdPlasma = 0 # Keeps Track of the Amount of Plasma Currently in the Node's 'Cold Tank'
    HotPlasma  = 0 # Keeps Track of the Amount of Plasma Currently in the Node's 'Hot Tank'
	
	ColdPlasmaCapacity = 0 # The Maximum Cold Plasma the node can hold, for implimentation reasons
							# The ColdPlasma Capacity should be >= whatever feeds the system each clock tick
	HotPlasmaCapacity  = 0 # The Maximum Hot Plasma the node can hold

    ColdPlasmaPressure = 0 # Keeps Track of the Current Rate of Cold Plasma Flow. Positive Rates are Flow in
    HotPlasmaPressure  = 0 # Keeps Track of the Current Rate of Hot Plasma Flow.
	
	ColdPlasmaPressureMax = 0
	HotPlasmaPressureMax  = 0

    PlasmaCoolingRate  = 0 # Keeps Track of the Current Rate at Which The system Cools or otherwise uses Plasma
    PlasmaHeatingRate  = 0 # Keeps Track of the Current Rate at Which the System Heats Plasma

    def __init__ (self,ColdCap,HotCap):
        self.ColdPlasmaCapacity = ColdCap;
        self.HotPlasmaCapacity  = HotCap;


    def coldPlasmaRoom ():
        return ColdPlasmaCapacity - ColdPlasma

    def hotPlasmaRoom ():
        return HotPlasmaCapacity - HotPlasma

    def addColdPlasma (self, NewColdPlasma):
        self.ColdPlasma += NewColdPlasma

    def addHotPlasma (self, NewHotPlasma):
        self.HotPlasma += NewHotPlasma
		
	def setCoolingRate(self,newRate):
		self.PlasmaCoolingRate = newRate
	
	def setHeatingRate(self, newRate):
		self.PlasmaHeatingRate = newRate
		
	def setColdPressure(self, newPressure):
		self.ColdPlasmaPressure = newPressure
		
	def setHotPlasmaPressure(self, newPressure):
		self.HotPlasmaPressure = newPressure
		
	
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
		
		# The Following Lines set the Pressures equal to the avlaible room to prevent overflow. If applicable.
		if self.ColdPlasmaCapacity - self.ColdPlasma < self.ColdPlasmaPressure:
			self.ColdPlasmaPressure = self.ColdPlasmaCapacity - self.ColdPlasma
		if self.HotPlasmaCapacity - self.HotPlasma < self.HotPlasmaPressure:
			self.HotPlasmaPressure = self.HotPlasmaCapacity - self.HotPlasma
		
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
            TotalColdPressure += x.ColdPlasmaPressure* TimeStep
            TotalHotPressure  += x.HotPlasmaPressure * TimeStep
        for x in system:
			TotalColdPressure += x.ColdPlasmaPressure * TimeStep
			TotalHotPressure  += x.HotPlasmaPressure  * TimeStep
			
		# The Following Routines Will Attempt to use the Tanks to Equalize the Pressure in The System
		if TotalHotPressure > 0:
			for x in tank:
				if TotalHotPressure >= x.HotPlasmaPressureMax:
					TotalHotPressure -= x.HotPlasmaPressureMax
					x.AddHotPlasma(x.HotPlasmaPressureMax)
				else:
					x.AddHotPlasma(TotalHotPressure)
					TotalHotPressure = 0
				if TotalHotPressure <= 0:
					break
		else: if TotalHotPressure < 0:
			# Pull Plasma From Tanks
		else:
			# Neither Pull Nor Push Plasma From the Tanks
			
		if TotalHotPressure > 0:
			# Pressure has exceeded System Capacity, vent the excess Pressure from this timestep.
			
		if TotalColdPressure > 0:
			# Push Plasma into Tanks
			for x in tank:
				if TotalColdPressure >= x.ColdPlasmaPressureMax:
					TotalColdPressure -= x.ColdPlasmaPressureMax
					x.AddColdPlasma(x.ColdPlasmaPressureMax)
				else:
					x.AddColdPlasma(TotalColdPressure)
					TotalColdPressure = 0
				if TotalColdPressure <= 0:
					break
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



