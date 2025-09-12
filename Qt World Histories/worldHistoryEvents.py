from core import WorldEvent, WorldSpan

#### Events ####

#Astrological / Geological / Early Life
WorldEvent("The Big Bang",-13500000000,["Astrological", "Pre Earth"])
WorldEvent("Earth Formed", -4500000000,["Astrological","Early Earth"])
WorldSpan("Life emerges on Earth","-4500000000,-3500000000",["Geological","Life","Early Life"])
WorldSpan("Cambrian Explosion","-540000000,-515000000",["Geological","Life","Early Life"])
WorldSpan("Carboniferous Period", "-360000000,-300000000",["Geological","Life","Early Life"])
WorldSpan("Most Recent Ice Age (LGP)","-115000,-9700",["Geological","Prehistory"])
WorldEvent("The Holocene begins", -9700,["Geological", "Antiquity"], desc="This is the current geological epoch.")

#Early Humans
WorldEvent("Earliest known use of stone tools, by early hominins",  
           -3300000, 
           ["Prehistory", "Life", "Invention", "Scientific", "Africa"], 
           desc="This marks the beginning of the Paleolithic")
WorldEvent("Earliest record of the Homo genus (Ethiopia)",          
           -2800000, 
           ["Prehistory", "Life", "People", "Africa"])
WorldEvent("Homo sapiens emerge",                                   
           -300000, 
           ["Prehistory", "Life", "People", "Africa"])
WorldEvent("First humans arrive in the Americas",                   
           -13000, 
           ["Prehistory", "People", "North America", "South America", "Central America"])
WorldEvent("Neolithic (Agricultural Revolution) begins",            
           -10000, 
           ["Prehistory", "People"], 
           desc= "This marks transition away from hunting and gathering.")
WorldEvent("Oldest recovered wooden boat made",                     
           -8000, 
           ["Prehistory", "Scientific", "Invention", "People"], 
           desc= "(Pesse canoe)")
WorldEvent("Earliest known copper smelting",                        
           -5000, 
           ["Prehistory", "Scientific", "Invention", "People", "Eastern Europe"], 
           desc= "(Serbia)")
WorldEvent("Potter's wheel invented",                               
           -4500, 
           ["Prehistory", "Scientific", "Invention", "People"])
WorldEvent("Oldest surviving wooden wheel with an axle",            
           -3130, 
           ["Prehistory", "Scientific", "Invention", "People"], 
           desc= "(Ljubljana Marshes)")
WorldSpan("Stonehenge constructed",                                 
           "-3000,-2000", 
           ["Prehistory", "Construction", "Scientific", "People", "Western Europe"])
WorldSpan("Standing stones (menhir) erected",                       
           "-2800,-1800", 
           ["Prehistory", "Construction", "Scientific", "People"], 
           desc= "(Bell Beaker peoples?)")
WorldEvent("Earliest evidence of iron-making",                      
           -2200, 
           ["Prehistory", "Scientific", "Invention", "People", "Eastern Europe", "Mediterranean"], 
           desc= "(Turkey)")


#Classical Antiquity
WorldEvent("Ancient Egyptian civilization founded",  
           -3100, 
           ["Antiquity", "People", "Africa", "Mediterranean"])
WorldEvent("First writing appears (cuneiform)",  
           -3000, 
           ["Antiquity", "Invention", "People", "Africa", "Mediterranean"],
           desc="(Mesopotamia)")
WorldSpan("Trojan War (speculative)", 
          "-1194,-1184",
          ["Antiquity", "War", "Greek", "Mediterranean"],
          desc="speculative dates via Eratosthenes")
WorldEvent("Rome founded (canonically)",  
           -753, 
           ["Antiquity", "People", "Roman", "Western Europe", "Mediterranean"])
WorldEvent("Hannibal crosses the Alps",  
           -218, 
           ["Antiquity", "War", "Roman", "Western Europe", "Mediterranean"])
WorldSpan("Warring States Period", 
          "-475,-221",
          ["People","War","Antiquity","Chinese","Asia"])

#Middle Ages
WorldEvent("Western Roman Empire Falls", 
           476, 
           ["War", "Antiquity", "Middle Ages", "Roman", "Mediterranean", "Western Europe"],
           desc="This marks the beginning of the Middle Ages")
WorldEvent("Papermaking spreads to the Islamic world", 
           751, 
           ["War", "Invention", "Middle Ages"],
           desc="Following the Battle of Talas")
WorldEvent("New Zealand First Settled by humans", 
           1280, 
           ["People", "Middle Ages", "Polynesian", "Oceania"],
           desc="(Polynesian peoples)")
WorldEvent("Eastern Roman Empire Falls", 
           1453, 
           ["War", "Middle Ages", "Roman", "Mediterranean", "Eastern Europe"],
           desc="This follows the Siege of Constantinople")

#Renaissance
WorldSpan("Golden Age of Piracy", 
          "1650,1730",
          ["People", "War", "Renaissance"])
WorldSpan("Napoleonic Wars", 
          "1803,1815",
          ["War", "Renaissance", "Western Europe"])

#Modern