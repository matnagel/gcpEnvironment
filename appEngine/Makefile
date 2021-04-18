PROJECTNAME = appEngine

include ~/GCP/conf/global.conf
include ~/GCP/conf/$(PROJECTNAME).conf

TMPDIR:=$(DEPLOYDIR)/$(shell date +%y%m%d)$(PROJECTNAME)

export PYTHONPATH=$(SOURCEDIR)

.PHONY: test deploy

test:
	python3 -m unittest discover test

mainFiles = app.yaml main.py requirements.txt

$(TMPDIR) : $(CONTENTPATH) $(mainFiles)
	mkdir $(TMPDIR)
	cp $(mainFiles) $(TMPDIR)
	sed -i -- "s/{{ valheimsecret }}/'$(VALHEIMSECRET)'/g" $(TMPDIR)/app.yaml
	mkdir $(TMPDIR)/content
	cp -r $(CONTENTPATH)/. $(TMPDIR)/content

deploy: $(TMPDIR) 
	gcloud app deploy $(TMPDIR)
