* Encoding: UTF-8.

T-TEST GROUPS=elitepeople(0 1)
  /MISSING=ANALYSIS
  /VARIABLES=comments
  /ES DISPLAY(TRUE)
  /CRITERIA=CI(.95).

GRAPH 
  /ERRORBAR(CI 95)=comments BY elitepeople.