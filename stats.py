import pstats

p = pstats.Stats('results.txt')
p.sort_stats('cumulative').print_stats(10)