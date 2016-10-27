import sys

try:
	highestNumber = int(sys.argv[1])
	lowestNumber = int(sys.argv[2])
	url = sys.argv[3]
except:
	print "Usage: " + sys.argv[0] + " <highest number> <lowest number> <url>"
	print "\nNote: you *must* include trailing slash in URL; Numbers are inclusive"
	sys.exit()

for i in range(lowestNumber, highestNumber+1):
	print url + str(i);