PROJECTNAME = loadTradegate

include ~/GCP/conf/global.conf
include ~/GCP/conf/$(PROJECTNAME).conf

TMPDIR:=$(DEPLOYDIR)/$(shell date +%y%m%d)$(PROJECTNAME)

export PYTHONPATH=$(SOURCEDIR)

.PHONY: test deploy

test:
	python3 -m unittest discover test

libFiles = gcp/Engines.py gcp/SqlSources.py gcp/Storage.py
mainFile = loadTradegate.py

$(TMPDIR) : $(addprefix $(SOURCEDIR)/, $(libFiles)) setup.py
	mkdir $(TMPDIR)
	cp $(mainFile) $(TMPDIR)/main.py
	mkdir $(TMPDIR)/gcp
	touch $(TMPDIR)/gcp/__init__.py
	cp $(addprefix $(SOURCEDIR)/, $(libFiles)) $(TMPDIR)/gcp
	cp setup.py $(TMPDIR)/
	cp README.txt $(TMPDIR)/

deploy: $(TMPDIR)
	cd $(TMPDIR); \
	python3 main.py \
		--runner DataflowRunner \
		--project $(PROJECTID) \
		--staging_location gs://$(DEPLOYBUCKET)/staging \
		--temp_location gs://$(DEPLOYBUCKET)/temp \
		--template_location gs://$(DEPLOYBUCKET)/templates/$(TEMPLATENAME) \
		--region $(REGION) \
		--setup_file ./setup.py \
		--dbuser $(DB_USER) \
		--dbpass $(DB_PASS) \
		--dbname $(DB_NAME) \
		--dbhost $(DB_HOST) \
		--dbport $(DB_PORT) \
		--bucketName $(TRADEGATEBUCKET) \
		--cutOffDate $(CUTOFFDATE)
