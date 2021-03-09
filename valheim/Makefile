PROJECTNAME = controlValheim

include ~/GCP/conf/global.conf
include ~/GCP/conf/$(PROJECTNAME).conf

TMPDIR:=$(DEPLOYDIR)/$(shell date +%s)$(PROJECTNAME)

export PYTHONPATH=$(SOURCEDIR)

.PHONY: deploy

mainFile = controlValheim.py

$(TMPDIR) : $(mainFile) requirements.txt
	mkdir $(TMPDIR)
	cp $(mainFile) $(TMPDIR)/main.py
	cp requirements.txt $(TMPDIR)

deploy: $(TMPDIR) 
	gcloud functions deploy $(PROJECTNAME) --region=$(REGION) --entry-point=pubsubEntryPoint --ingress-settings=internal-only --memory=128MB --runtime=python38 --service-account=$(SERVICEACCOUNT) --source=$(TMPDIR) --stage-bucket=$(STAGEBUCKET) --timeout=60s --set-env-vars=$(ENVVAR) --max-instances=1 --trigger-topic=$(TOPIC)
