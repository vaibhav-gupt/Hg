leiten_sources = leiten.sla ../Quelldateien/1w6-qr-flattr-flyer-outer.png ../Quelldateien/1w6.org-qrcode-flyerbuecher-raw.png ../Quelldateien/Gertrud_Wenzel/Dragons_original_EWS_Logo.png ../Quelldateien/Gertrud_Wenzel/draketo_siuit_klein.png ../Quelldateien/Gertrud_Wenzel/rogBa_gr_transparent.png ../Quelldateien/Gertrud_Wenzel/sawwar.png ../Quelldateien/Gertrud_Wenzel/Flyer-Hinterlegt-ohne-logo.png ../Quelldateien/Gertrud_Wenzel/Flyer-Hinterlegt.png ../Quelldateien/Hintergründe/karte_trekk-v0.8.png ../Quelldateien/Free_Software_Foundation/gpl-v3-300x149.png ../Quelldateien/mediawiki/Giulio-cesare-enhanced_1-800x1450_art2.png 

fonts = ../Quelldateien/Schriften/Hattori-Hanzo/*.ttf ../Quelldateien/Schriften/Fanwood/Fanwood.ttf

hattori_hanzo_license = ../Quelldateien/Schriften/Hattori-Hanzo/Creative*.txt
fanwood_license = ../Quelldateien/Schriften/Fanwood/COPYING 

source : $(leiten_sources) $(fonts)
	mkdir -p flyer-src
	cp $(leiten_sources) $(fonts) flyer-src/
	sed -i s/PFILE=.*Quelldateien\\//PFILE=\"/g flyer-src/*sla
	sed -i s/PFILE=.[a-zA-Z\_ü]*\\//PFILE=\"/g flyer-src/*sla
	mkdir -p flyer-src/font_licenses
	cp $(fanwood_license) flyer-src/font_licenses/fanwood.txt
	cp $(hattori_hanzo_license) flyer-src/font_licenses/hattori_hanzo.txt
	echo "Sources of the fonts are available in our revision tracking system at http://bitbucket.org/ArneBab/1w6 - if that should no longer exist, a new location should be named on http://1w6.org" > flyer-src/font_licenses/sources.txt
	zip -r -9 flyer-src.zip flyer-src









