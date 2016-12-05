SUBDIRS=vypyr

bin_SCRIPTS = launchvypyr
CLEANFILES = $(bin_SCRIPTS)
EXTRA_DIST = launchvypyr.in

do_substitution = sed -e 's,[@]pythondir[@],$(pythondir),g' \
	-e 's,[@]PACKAGE[@],$(PACKAGE),g' \
	-e 's,[@]VERSION[@],$(VERSION),g' 

launchvypyr: launchvypyr.in Makefile
	$(do_substitution) < $(srcdir)/launchvypyr.in > launchvypyr
	chmod +x launchvypyr

