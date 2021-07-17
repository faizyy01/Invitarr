from plexapi.myplex import MyPlexAccount
import re

def plexadd(plex, plexname):
    try:
        plex.myPlexAccount().inviteFriend(user=plexname, server=plex, sections=Plex_LIBS, allowSync=False,
                                              allowCameraUpload=False, allowChannels=False, filterMovies=None,
                                              filterTelevision=None, filterMusic=None)

    except Exception as e:
        print(e)
        return False
    else:
        print(plexname +' has been added to plex (☞ຈل͜ຈ)☞')
        return True


def plexremove(plex, plexname):
    try:
        plex.myPlexAccount().removeFriend(user=plexname)
    except Exception as e:
        print(e)
        return False
    else:
        print(plexname +' has been removed from plex (☞ຈل͜ຈ)☞')
        return True

def verifyemail(addressToVerify):
    regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'
    match = re.match(regex, addressToVerify)
    if match == None:
	    return False
    else:
        return True