#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# Votre nom ou pseudo
from resources.lib.gui.hoster import cHosterGui #systeme de recherche pour l'hote
from resources.lib.gui.gui import cGui #systeme d'affichage pour xbmc
from resources.lib.handler.inputParameterHandler import cInputParameterHandler #entree des parametres
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler #sortie des parametres
from resources.lib.handler.requestHandler import cRequestHandler #requete url
from resources.lib.parser import cParser #recherche de code
from resources.lib.util import cUtil
from resources.lib.comaddon import progress, VSlog #import du dialog progress
import re
#from resources.lib.util import cUtil #outils pouvant etre utiles

#Si vous créez une source et la deposez dans le dossier "sites" elle sera directement visible sous xbmc

SITE_IDENTIFIER = 'hds_stream' #identifant (nom de votre fichier) remplacez les espaces et les . par _ AUCUN CARACTERE SPECIAL
SITE_NAME = 'hds-stream' #nom que xbmc affiche
SITE_DESC = 'Film streaming HD complet en vf. Des films et séries pour les fan de streaming hds.' #description courte de votre source

URL_MAIN = 'https://ww6.hds-stream.to/' #url de votre source

#definis les url pour les catégories principale, ceci est automatique, si la definition est présente elle sera affichee.
#LA RECHERCHE GLOBAL N'UTILE PAS showSearch MAIS DIRECTEMENT LA FONCTION INSCRITE DANS LA VARIABLE URL_SEARCH_*
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
#recherche global films
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
#recherche global serie, manga
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
#recherche global divers
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
#
FUNCTION_SEARCH = 'showMovies'

# menu films existant dans l'acceuil (Home)
MOVIE_NEWS = (URL_MAIN + 'films', 'showMovies') #films (derniers ajouts = trie par date)
#MOVIE_MOVIE = ('http://', 'load') #films (load source)
MOVIE_VIEWS = (URL_MAIN + 'tendance/?get=movies', 'showMovies') #films (les plus vus = populaire)
MOVIE_GENRES = (True, 'showGenres') #films genres
MOVIE_ANNEES = (True, 'showMovieYears') #films (par années)
#menu supplementaire non gerer par l'acceuil



# menu serie existant dans l'acceuil (Home)
#SERIE_SERIES = ('http://', 'load') #séries (load source)
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies') #news.png ou series.png | séries (derniers ajouts = trie par date)
SERIE_GENRES = (True, 'showGenres') #séries genres



def load(): #fonction chargee automatiquement par l'addon l'index de votre navigation.
    oGui = cGui() #ouvre l'affichage

    oOutputParameterHandler = cOutputParameterHandler() #appelle la fonction pour sortir un parametre
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') # sortie du parametres siteUrl n'oubliez pas la Majuscule
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    #Ajoute lien dossier (identifant, function a attendre, nom, icone, parametre de sortie)
    #Puisque nous ne voulons pas atteindre une url on peut mettre ce qu'on veut dans le parametre siteUrl

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)
    #ici la function showMovies a besoin d'une url ici le racourci MOVIE_NEWS

    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    #oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)
    #showGenres n'a pas besoin d'une url pour cette methode

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par Années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Tendances)', 'views.png', oOutputParameterHandler)

    
        
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    #oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    

        
    oGui.setEndOfDirectory() #ferme l'affichage

def showSearch(): #fonction de recherche
    oGui = cGui()

    sSearchText = oGui.showKeyBoard() #appelle le clavier xbmc
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText #modifie l'url de recherche
        showMovies(sUrl) #appelle la fonction qui pourra lire la page de resultats
        oGui.setEndOfDirectory()
        return


def showGenres(): #affiche les genres
    oGui = cGui()

    #juste a entrer les categories et les liens qui vont bien
    liste = []
    liste.append( ['Action', URL_MAIN + 'genre/action/'] )
    liste.append( ['Animation', URL_MAIN + 'genre/animation/'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'arts-martiaux/'] )
    liste.append( ['Aventure', URL_MAIN + 'genre/aventure/'] )
    liste.append( ['Biopic', URL_MAIN + 'genre/biopic/'] )
    liste.append( ['Comédie', URL_MAIN + 'genre/comedie/'] )
    liste.append( ['Comédie Musicale', URL_MAIN + 'genre/comedie-musical/'] )
    liste.append( ['Drame', URL_MAIN + 'genre/drame/'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'genre/epouvante-horreur/'] )
    liste.append( ['Espionnage', URL_MAIN + 'genre/espionnage/'] )
    liste.append( ['Fantastique', URL_MAIN + 'genre/fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'genre/guerre/'] )
    liste.append( ['Historique', URL_MAIN + 'genre/historique/'] )
    liste.append( ['Judiciaire', URL_MAIN + 'genre/judiciaire/'] )
    liste.append( ['Musical', URL_MAIN + 'genre/musical/'] )
    liste.append( ['Péplum', URL_MAIN + 'genre/peplum/'] )
    liste.append( ['Policier', URL_MAIN + 'genre/policier/'] )
    liste.append( ['Romance', URL_MAIN + 'genre/romance/'] )
    liste.append( ['Science Fiction', URL_MAIN + 'genre/science-fiction/'] )
    liste.append( ['Thriller', URL_MAIN + 'genre/thriller/'] )
    liste.append( ['Western', URL_MAIN + 'genre/western/'] )

    for sTitle, sUrl in liste: #boucle

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl) #sortie de l'url en parametre
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        

    oGui.setEndOfDirectory()


def showMovieYears():
    oGui = cGui()

    for i in reversed (xrange(1913, 2019)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieYears():
    oGui = cGui()

    for i in reversed (xrange(1936, 2019)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch = ''):
    oGui = cGui() 
    if sSearch: 
      sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl') 

    oRequestHandler = cRequestHandler(sUrl) 
    sHtmlContent = oRequestHandler.request() 

    if sSearch:
        sPattern = '<a href="([^"]+)".+?url\((.+?)\).+?<div class="title"> (.+?) </div>'
    elif 'tendance/' in sUrl :
        sPattern = 'id="post-[0-9].+?<img src="([^"]+)".+?class="data".+?href="([^"]+)">([^<]+)'
    else:   
        sPattern = 'id="post-[0-9].+?<img src="([^"]+)".+?class="data".+?href="([^"]+)">([^<]+).+?class="metadata".+?<span>([^<]+).+?class="texto">([^<]+)'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        #dialog barre de progression
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total) #dialog update
            if progress_.iscanceled():
                break

            sThumb = aEntry[0]
            if sThumb.startswith('//'):
                sThumb = 'https:' + sThumb
            sUrl2 = aEntry[1]
            sTitle = aEntry[2]
            sYear = ''
            sDesc = ''
            if len(aEntry)>3:
                sYear = aEntry[3]
                sDesc = aEntry[4]
            

            sDisplayTitle = ('%s (%s)') % (sTitle, sYear)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2) #sortie de l'url
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle) #sortie du titre
            oOutputParameterHandler.addParameter('sThumb', sThumb) #sortie du poster

            if '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSxE', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLink', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
               

            #
        progress_.VSclose(progress_) #fin du dialog

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent) #cherche la page suivante
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)
            #Ajoute une entree pour le lien Next | pas de addMisc pas de poster et de description inutile donc

        oGui.setEndOfDirectory() #ferme l'affichage


def __checkForNextPage(sHtmlContent): #cherche la page suivante
    oParser = cParser()
    sPattern = 'class="current".+?a href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showSxE():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<span class=\'title\'>([^<]+)|class=\'numerando\'>\d -([^<]+).+?class=\'episodiotitle\'><a href="([^"]+)">([^<]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR crimson]' + aEntry[0] + '[/COLOR]')

            else:
                sUrl = aEntry[2]
                EpTitle = aEntry[3]
                Ep = aEntry[1]
                sTitle = sMovieTitle + ' Episode' + Ep + EpTitle

                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()
    
def showLink():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    sPattern = "class='loader'.+?data-type='([^']+)'.+?data-post='([^']+)'.+?data-nume='([^']+)'"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sUrl2 = URL_MAIN + 'wp-admin/admin-ajax.php'
            dType = aEntry[0]
            dPost = aEntry[1]
            dNum = aEntry[2]
            sHost = 'Serveur' + dNum  
            
   
            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)
            

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('dType', dType)
            oOutputParameterHandler.addParameter('dPost', dPost)
            oOutputParameterHandler.addParameter('dNum', dNum)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def ShowSerieSaisonEpisodes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    sPattern = "id='player-option-.+?data-type='([^']+)'.+?data-post='([^']+)'.+?data-nume='([^']+)'.+?'server'>([^.]+)"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sUrl2 = URL_MAIN + 'wp-admin/admin-ajax.php'
            dType = 'movie'
            dPost = aEntry[1]
            dNum = aEntry[2]
            sHost = aEntry[3]
               
            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('dType', dType)
            oOutputParameterHandler.addParameter('dPost', dPost)
            oOutputParameterHandler.addParameter('dNum', dNum)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    referer = oInputParameterHandler.getValue('referer')
    dPost = oInputParameterHandler.getValue('dPost')
    dNum = oInputParameterHandler.getValue('dNum')
    dType = oInputParameterHandler.getValue('dType')

    pdata = 'action=doo_player_ajax&post=' + dPost + '&nume=' + dNum + '&type=' + dType
    oRequest = cRequestHandler(sUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
    oRequest.addHeaderEntry('Referer', referer)
    oRequest.addHeaderEntry('Accept', '*/*')
    oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequest.addParametersLine(pdata)

    sHtmlContent = oRequest.request()

    
    sPattern = '(?:<iframe|<IFRAME).+?(?:src|SRC)=(?:\'|")(.+?)(?:\'|")'
    aResult1 = re.findall(sPattern, sHtmlContent)

    #2
    sPattern = '<a href="([^"]+)">'
    aResult2 = re.findall(sPattern, sHtmlContent)

    #fusion
    aResult = aResult1 + aResult2
    if (aResult):
        for aEntry in aResult:


            sHosterUrl = aEntry
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()




