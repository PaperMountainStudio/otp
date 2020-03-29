PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin

all:

install:
	install -D -m 755 $(DESTDIR)$(BINDIR)/otp

uninstall:
	rm $(DESTDIR)$(BINDIR)/otp

.PHONY: all install uninstall
