default: ensure-unique-dependency-versions clean compile-all-domains compile-all-cross-domain-tests


compile-all-domains:
	build/scripts/compiledomains.py ${OPTS} -d `build/scripts/listdomains.py ${OPTS}` -f ./dependency-versions.csv

compile-all-cross-domain-tests:


ensure-unique-dependency-versions:
	./build/scripts/dependencies.py -f ./dependency-versions.csv

clean:
	rm -rf target
