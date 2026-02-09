instance:
	make bin/instance

fg: instance
	bin/instance fg

omelette:
	make parts/omelette
	echo "cd parts/omelette"


