default: ensure-unique-dependency-versions clean compile-all-domains compile-all-cross-domain-tests run-all-domain-unit-tests hello


compile-all-domains:
	build/scripts/compiledomains.py ${OPTS} -d `build/scripts/listdomains.py` -f ./dependency-versions.csv

compile-all-cross-domain-tests:

run-all-domain-unit-tests:
	build/scripts/runtests.py ${OPTS} -d `build/scripts/listdomains.py` -f ./dependency-versions.csv -s unit-tests

ensure-unique-dependency-versions:
	./build/scripts/dependencies.py -f ./dependency-versions.csv

clean:
	rm -rf target

hello:
	./build/scripts/run.py -f dependency-versions.csv -d apply -s main com.clubjava.hello.Hello

