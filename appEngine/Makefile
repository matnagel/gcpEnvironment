PROJECTNAME = appEngine

include ~/GCP/conf/global.conf
include ~/GCP/conf/$(PROJECTNAME).conf

TMPDIR:=$(DEPLOYDIR)/$(shell date +%s)$(PROJECTNAME)

export PYTHONPATH=$(SOURCEDIR)

.PHONY: test deploy

test:
	python3 -m unittest discover test


mainFiles = app.yaml main.py requirements.txt

$(TMPDIR) : $(CONTENTPATH) $(mainFiles)
	mkdir $(TMPDIR)
	cp $(mainFiles) $(TMPDIR)
	mkdir $(TMPDIR)/content
	cp -r $(CONTENTPATH) $(TMPDIR)/content

deploy: $(TMPDIR) 
	echo "Ready to deploy"
