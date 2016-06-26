FONTSOURCES = \
	Purisa.sfd \
	Purisa-Bold.sfd \
	Purisa-Oblique.sfd \
	Purisa-BoldOblique.sfd

EXTRA_DIST = $(FONTSOURCES) CREDITS README.tlwgmono

include scripts/gen.mk.am

if INCLUDE_LATEX

purisa.afm:      Purisa.afm
	[ -f $@ ] || $(LN_S) $< $@
purisa_b.afm:    Purisa-Bold.afm
	[ -f $@ ] || $(LN_S) $< $@
purisa_o.afm:    Purisa-Oblique.afm
	[ -f $@ ] || $(LN_S) $< $@
purisa_bo.afm:   Purisa-BoldOblique.afm
	[ -f $@ ] || $(LN_S) $< $@


FONTS = \
	purisa \
	purisa_b \
	purisa_o \
	purisa_bo

MAP = tlwg.map

include latex/texfont.mk.am

endif # INCLUDE_LATEX
