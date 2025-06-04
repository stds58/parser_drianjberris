import pstats
from pstats import SortKey

p = pstats.Stats("C:\Users\SAVOST~1.VA\AppData\Local\Temp\watch_reload_profile.prof")
p.sort_stats(SortKey.CUMULATIVE).print_stats(20)


# snakeviz output.prof
# snakeviz C:\Users\SAVOST~1.VA\AppData\Local\Temp\watch_reload_profile.prof


