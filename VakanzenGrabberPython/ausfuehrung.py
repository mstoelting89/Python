import VakanzenGrabber

##############################################################################################################################################
#
#   Aufrufen der Funktion VarkanzenGrabben
#
##############################################################################################################################################

vakanzenGrabben = VakanzenGrabber.VakanzenGrabber("https://www.freelance.de","Test Manager","Projekte und Aufträge für Freelancer, Freiberufler und Selbstständige")

if vakanzenGrabben.vakanzenGrabbenHauptseite() == True:
    vakanzenGrabben.vakanzenGrabbenSuchseite()