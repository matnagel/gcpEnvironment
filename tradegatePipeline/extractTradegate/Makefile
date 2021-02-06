PROJECTNAME = extractTradegate

include ~/GCP/conf/global.conf
include ~/GCP/conf/$(PROJECTNAME).conf

TMPDIR:=$(DEPLOYDIR)/$(shell date +%s)tmpFor$(PROJECTNAME)

export PYTHONPATH=$(SOURCEDIR)

.PHONY: test deploy

test:
	python3 -m unittest discover test

libFiles = gcp/Engines.py gcp/SqlSources.py gcp/Storage.py
mainFile = scrapeTradegate.py

zipName = $(shell date +%y%m%d_%H%M)scrapeTradegate.zip

$(DEPLOYDIR)/$(zipName) : $(addprefix $(SOURCEDIR)/, $(libFiles)) requirements.txt
	mkdir $(TMPDIR)
	cp $(mainFile) $(TMPDIR)/main.py
	mkdir $(TMPDIR)/gcp
	cp $(addprefix $(SOURCEDIR)/, $(libFiles)) $(TMPDIR)/gcp
	cp requirements.txt $(TMPDIR)
	cd $(TMPDIR); zip $(DEPLOYDIR)/$(zipName) main.py requirements.txt $(libFiles)

deploy: $(DEPLOYDIR)/$(zipName)
	gcloud functions deploy $(PROJECTNAME) --entry-point=pubsubEntryPoint --ingress-settings=internal-only --memory=128MB --runtime=python38 --service-account=$(SERVICEACCOUNT) --source=$(DEPLOYDIR)/$(zipName) --stage-bucket=$(STAGEBUCKET) --timeout=30s --set-env-vars=[$(ENVVAR)] --max-instances=1 --trigger-topic=$(TOPIC)
