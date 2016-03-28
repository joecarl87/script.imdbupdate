################
# IMDB Update  #
# by Jandalf   #
################

import urllib2, socket, json, util

RATING_DIFF = 0.000
ENABLE_DIFF = util.settingBool("enableDiff")
SEPARATOR = util.setting("separator").strip()

class imdbMovie(object):
    
    def __init__(self, imdbID):
        self.__rating = ""
        self.__votes = ""
        self.__error = False
        self.__imdbID = imdbID
        
        self.getData()

    def getData(self):
        try:
            url="http://omdbapi.com/?i=%s" % self.__imdbID
            request = urllib2.Request(url)
            req = urllib2.urlopen(request)
        except:
            log('error response from github')
            self.__error = True
        else:
            try:
                data = json.loads(req.read().decode('utf8'))
                if "error" in data or data["Response"] == "False":
                    self.__error = True
                else:
                    self.__rating = data["imdbRating"]
                    self.__votes = int(data["imdbVotes"].replace(",", ""))
            except:
                self.__error = True

    def shouldUpdate(self, old):
        oldVotes = 0 if old["votes"] == '' else util.stringToFloat(old["votes"])
        newVotes = self.__votes

        votesChange = (oldVotes != newVotes) if not ENABLE_DIFF else (oldVotes > newVotes or round(oldVotes * (1 + RATING_DIFF)) < newVotes)

        oldRating = round(float(old["rating"]), 1)
        newRating = round(float(self.__rating), 1)

        return (oldRating != newRating) or votesChange
    
    def rating(self):   return self.__rating
    def votes(self):    return self.intWithCommas(self.__votes).replace(",", SEPARATOR)
    def error(self):    return self.__error
    def imdbID(self):   return self.__imdbID

    def intWithCommas(self, x):
        if type(x) not in [type(0), type(0L)]:
            raise TypeError("Parameter must be an integer.")
        if x < 0:
            return '-' + intWithCommas(-x)
        result = ''
        while x >= 1000:
            x, r = divmod(x, 1000)
            result = ",%03d%s" % (r, result)
        return "%d%s" % (x, result)
