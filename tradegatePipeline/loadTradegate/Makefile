PROJECTNAME = loadTradegate

include ~/GCP/conf/global.conf
include ~/GCP/conf/$(PROJECTNAME).conf

TMPDIR:=$(DEPLOYDIR)/$(shell date +%s)$(PROJECTNAME)

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
	cp $(addprefix $(SOURCEDIR)/, $(libFiles)) $(TMPDIR)/gcp
	cp setup.py $(TMPDIR)/

deploy: $(TMPDIR)
	cd $(TMPDIR); \
	python3 main.py \
		--runner DataflowRunner \
		--project $(PROJECTID) \
		--staging_location gs://$(DEPLOYBUCKET)/staging \
		--temp_location gs://$(DEPLOYBUCKET)/temp \
		--template_location gs://$(DEPLOYBUCKET)/templates/$(TEMPLATENAME) \
		--region $(REGION) \
		--save_main_session True \
		--setup_file ./setup.py \
		--dbuser $(DB_USER) \
		--dbpass $(DB_PASS) \
		--dbname $(DB_NAME) \
		--cloudsqlconnectionname $(CLOUD_SQL_CONNECTION_NAME) \
		--bucketName $(TRADEGATEBUCKET) \
		--cutOffDate $(CUTOFFDATE)
