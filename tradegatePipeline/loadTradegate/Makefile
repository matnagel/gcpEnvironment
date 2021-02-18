PROJECTNAME = loadTradegate

include ~/GCP/conf/global.conf
include ~/GCP/conf/$(PROJECTNAME).conf

export PYTHONPATH=$(SOURCEDIR)

.PHONY: test deploy

test:
	python3 -m unittest discover test

deploy:
	python3 -m loadTradegate \
		--runner DataflowRunner \
		--project $(PROJECTID) \
		--staging_location gs://$(DEPLOYBUCKET)/staging \
		--temp_location gs://$(DEPLOYBUCKET)/temp \
		--template_location gs://$(DEPLOYBUCKET)/templates/$(TEMPLATENAME) \
		--region $(REGION) \
		--save_main_session True \
		--bucketName $(TRADEGATEBUCKET) \
		--cutOffDate $(CUTOFFDATE)
