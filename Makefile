SRCDIR = eruditarticle
LOCALEDIR = $(SRCDIR)/locale
LANGS = en fr
POFILES = $(addsuffix /LC_MESSAGES/django.po, $(addprefix $(LOCALEDIR)/, $(LANGS)))
MOFILES = $(POFILES:%.po=%.mo)

.PHONY: FORCE
FORCE:

$(LOCALEDIR)/django.pot: FORCE
	cd $(SRCDIR) && find . -name "*.py" \
		| xargs xgettext -o ../$@ --force-po --from-code=utf-8 --keyword="pgettext:1c,2"

$(POFILES): $(LOCALEDIR)/django.pot FORCE
		msgmerge -o $@ --no-fuzzy-matching $@ $<
	
.PHONY: po
po: $(POFILES)

$(MOFILES): $(POFILES)
	msgfmt -o $@ $(@:%.mo=%.po)

.PHONY: mo
mo: $(MOFILES)
