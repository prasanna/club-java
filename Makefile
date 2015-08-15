default: ensure-unique-dependency-versions clean compile-all-domains compile-all-domain-unit-tests compile-all-cross-domain-tests


compile-all-domains:
	build/scripts/compiledomains.py ${OPTS} -d `build/scripts/listdomains.py ${OPTS}`

compile-all-domain-unit-tests:


compile-all-cross-domain-tests:


ensure-unique-dependency-versions:
	build/scripts/dieifdups.py dependency-versions.csv


clean:
	rm -rf target
