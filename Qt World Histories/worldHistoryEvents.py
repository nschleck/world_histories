from core import WorldEvent, WorldSpan

#### Events ####

#Astrological / Geological / Early Life
WorldEvent("The Big Bang",-13500000000,["Astrological", "Pre Earth"])
WorldEvent("Earth Formed", -4500000000,["Astrological","Early Earth"])
WorldSpan("Cambrian Explosion","-540000000,-515000000",["Geological","Life","Early Life"])
WorldSpan("Carboniferous Period", "-360000000,-300000000",["Geological","Life","Early Life"])
WorldSpan("Most Recent Ice Age (LGP)","-115000,-9700",["Geological","Prehistory"])
WorldEvent("The Holocene begins", -9700,["Geological", "Antiquity"], desc="This is the current geological epoch.")

#Early Humans

#Classical Antiquity
WorldSpan("Trojan War (speculative)", "-1194,-1184",["People","War","Antiquity","Greek","Mediterranean"],desc="speculative dates via Eratosthenes")
WorldSpan("Warring States Period", "-475,-221",["People","War","Antiquity","Chinese","Asia"])
WorldSpan("Warring States Period (Testing)", "-450,-200",["People","War","Antiquity","Chinese","Asia"])

#Middle Ages
WorldEvent("Western Roman Empire Falls", 476, ["People","War","Antiquity","Middle Ages","Roman","Mediterranean","Western Europe"],desc="This marks the beginning of the Middle Ages")
WorldEvent("New Zealand First Settled", 1280, ["People","Life","Middle Ages","Polynesian","Oceania"],desc="By Polynesian peoples")
WorldEvent("Eastern Roman Empire Falls", 1453, ["People","War","Middle Ages","Roman","Mediterranean","Eastern Europe"],desc="This follows the Siege of Constantinople")

#Modern