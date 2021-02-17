PROJECTNAME = loadTradegate

include ~/GCP/conf/global.conf
#include ~/GCP/conf/$(PROJECTNAME).conf

export PYTHONPATH=$(SOURCEDIR)

.PHONY: test deploy

test:
	python3 -m unittest discover test

deploy: $(TMPDIR) 
	echo "Deploy to Dataflow"
