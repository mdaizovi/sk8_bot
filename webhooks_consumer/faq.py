FAQ = {}
# questions
indoor_q = "where can you skate indoors in berlin?"
rain_q = "where can you skate in berlin when it's raining?"
skateshop_q = "where can you buy roller skates in berlin?"

# answers
FAQ[
    indoor_q
] = """
Public indoor park skating options are the Ping Pong hall at Mellow Park and the Skatehalle. 
Quads and inlines are allowed at the skatehalle unless it's a bsv session (this one is skateboard only), 
also occasional WCMX sessions 
("Skate Slot wechselnd" in the schedule).
Skatehalle has FLINTA sessions which are skateboard, quad, inline, but you need to be FLINTA.
Mellow Park is always changing when the Ping Pong hall is open and whether there are special session days, so it's best to call them. 
"""

rain_a = (
    FAQ[indoor_q]
    + """
There's also a diy with a few obstacles in Heinersdorf with roof and some diy obstacles under a bridge at Booky Bridge 
(10 mins walk from Baumschulenweg S-Bahn stop). 
Plus heidelberger platz skatepark (transitions) works if it's only softly raining.
You can flat skate at the Messe Nord ICC underpass but it's usually very dirty and sometimes people live there
so think twice about going alone.
"""
)
FAQ[rain_q] = rain_a

FAQ[skateshop_q] = """
No good local shop. Sometimes you can find good deals on Kleinanzeigen.de but the selection is small and sporadic. 
There is also a facebook group called '2nd Hand Rollschuh Börse - roller skate flea market - Deutschland & europe'. 
Decathalon and a few skateboard shops have intro skates. 
You can buy Wifas or Riedells from Michel, the guy behind Rollers, Inc.  
Typically we order from suckerpunch or rollerderbyhouse.eu
"""

