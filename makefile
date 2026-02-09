bin/instance: test-6.0.x.cfg buildout-constraints.txt
	uv tool run --from zc.buildout -c buildout-constraints.txt buildout -c test-6.0.x.cfg install instance

parts/omelette: buildout.cfg buildout-constraints.txt
	uv tool run --from zc.buildout -c buildout-constraints.txt buildout -c test-6.0.x.cfg install omelette
