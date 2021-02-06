PROJECTNAME = extractTradegate

include ~/GCP/conf/global.conf
include ~/GCP/conf/$(PROJECTNAME).conf

TMPDIR:=$(DEPLOYDIR)/$(shell date +%s)$(PROJECTNAME)

export PYTHONPATH=$(SOURCEDIR)

.PHONY: test deploy

test:
	python3 -m unittest discover test

libFiles = gcp/Engines.py gcp/SqlSources.py gcp/Storage.py
mainFile = scrapeTradegate.py

zipName = $(shell date +%y%m%d_%H%M)scrapeTradegate.zip

$(TMPDIR) : $(addprefix $(SOURCEDIR)/, $(libFiles)) requirements.txt
	mkdir $(TMPDIR)
	cp $(mainFile) $(TMPDIR)/main.py
	mkdir $(TMPDIR)/gcp
	cp $(addprefix $(SOURCEDIR)/, $(libFiles)) $(TMPDIR)/gcp
	cp requirements.txt $(TMPDIR)

deploy: $(TMPDIR) 
	gcloud functions deploy $(PROJECTNAME) --region=$(REGION) --entry-point=pubsubEntryPoint --ingress-settings=internal-only --memory=128MB --runtime=python38 --service-account=$(SERVICEACCOUNT) --source=$(TMPDIR) --stage-bucket=$(STAGEBUCKET) --timeout=30s --set-env-vars=[$(ENVVAR)] --max-instances=1 --trigger-topic=$(TOPIC)
