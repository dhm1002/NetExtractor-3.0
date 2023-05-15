# -*- coding: utf-8 -*-
import os
from flask import render_template, Flask, request, url_for, redirect, json, send_file, make_response, g, session, send_from_directory
from src.Modelo import Modelo as mod
from src import config as cfg
from src.PersistenciaSesiones import TempBD
from flask_babel import Babel, gettext
import shutil


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = cfg.upload_folder
app.config['BABEL_TRANSLATION_DIRECTORIES'] = cfg.translations_folder
app.config['SECRET_KEY'] = cfg.secretkey
babel = Babel(app)
frames=5
apariciones=None
epub=False
sesion=0
tbd = TempBD.TempBD.getInstance()

@babel.localeselector
def get_locale():
    if('lang' not in session):
        session['lang'] = request.accept_languages.best_match(cfg.LANGUAGES.keys())
    return session['lang']

@app.before_request
def before_request():
    g.locale = get_locale()

@app.route('/' , methods=["GET","POST"])
def home():
    return render_template('home.html')

@app.route('/Inicio/' , methods=["GET","POST"])
def inicio():
    return render_template('seleccion.html')
	
@app.route('/Formato-Incorrecto/' , methods=["GET","POST"])
def formatoIncorrecto():
    return render_template('formatoIncorrecto.html')
    
@app.route('/Dicts-Pelicula/' , methods=["GET","POST"])
def diccionarioPelicula():
    m = mod.Modelo()
    if request.method == "POST":
        if('usuario' not in session or session['usuario'] not in tbd.getSesiones().keys()):
            session['usuario'] = tbd.addSesion(m)
            dirName = os.path.join(app.config['UPLOAD_FOLDER'], str(session['usuario']))
            if(not os.path.exists(dirName)):
                os.makedirs(dirName)
        #APUNTAR EN LA DOCUMENTACION
        tbd.replaceObject(session['usuario'],m)
        session['configVis'] = {'Path to file (csv or json)': 'https://gist.githubusercontent.com/ulfaslak/6be66de1ac3288d5c1d9452570cbba5a/raw/0b9595c09b9f70a77ee05ca16d5a8b42a9130c9e/miserables.json', 'Apply heat (wiggle)': False, 'Charge strength': -50, 'Center gravity': 0.1, 'Link distance': 10, 'Link width': 5, 'Link alpha': 0.5, 'Node size': 10, 'Node stroke size': 0.5, 'Node size exponent': 0.5, 'Link width exponent': 0.5, 'Collision': False, 'Node fill': '#16a085', 'Node stroke': '#000000', 'Link stroke': '#7c7c7c', 'Label stroke': '#000000', 'Show labels': True, 'Show singleton nodes': False, 'Node size by strength': True, 'Zoom': 1.5, 'Min. link weight %': 0, 'Max. link weight %': 100}   
        url = request.form['txt txt-url1']
        m = tbd.getObject(session['usuario'])
        formato = m.scrapeWikiPelicula(url)
        url = url.split('/')
        prov = url[4]
        prov = prov.split('.')
        ficheroNombre = prov[0]
        session['fichero'] = ficheroNombre
        if (formato == 1):
            m.cambiarPantallas(0)
            return redirect(url_for('moddict'))
        else:
            return redirect(url_for('formatoIncorrecto'))
    return render_template('dictpelicula.html', perso = m.hayPersonajes(), formato = m.getFormato())
	
@app.route('/Sel-Epub/', methods=["GET","POST"])
def index():
    error = ''
    if request.method == "POST":
        fich = request.files["btn btn-selepub"]
        m = mod.Modelo()
        if('usuario' not in session or session['usuario'] not in tbd.getSesiones().keys()):
            session['usuario'] = tbd.addSesion(m)
            dirName = os.path.join(app.config['UPLOAD_FOLDER'], str(session['usuario']))
            if(not os.path.exists(dirName)):
                os.makedirs(dirName)
        fullpath = os.path.join(app.config['UPLOAD_FOLDER'], str(session['usuario']), fich.filename)
        fich.save(fullpath)
        if(mod.Modelo.esEpub(fullpath)):
            session['fichero'] = fich.filename
            m.obtTextoEpub(fullpath)
            os.remove(fullpath)
            tbd.replaceObject(session['usuario'],m)
            m.cambiarPantallas(1)
            session['configVis'] = {'Path to file (csv or json)': 'https://gist.githubusercontent.com/ulfaslak/6be66de1ac3288d5c1d9452570cbba5a/raw/0b9595c09b9f70a77ee05ca16d5a8b42a9130c9e/miserables.json', 'Apply heat (wiggle)': False, 'Charge strength': -50, 'Center gravity': 0.1, 'Link distance': 10, 'Link width': 5, 'Link alpha': 0.5, 'Node size': 10, 'Node stroke size': 0.5, 'Node size exponent': 0.5, 'Link width exponent': 0.5, 'Collision': False, 'Node fill': '#16a085', 'Node stroke': '#000000', 'Link stroke': '#7c7c7c', 'Label stroke': '#000000', 'Show labels': True, 'Show singleton nodes': False, 'Node size by strength': True, 'Zoom': 1.5, 'Min. link weight %': 0, 'Max. link weight %': 100}
            return redirect(url_for('dictaut'))
        else: 
            error = gettext("La ruta indicada no contiene un fichero epub")
            return render_template('index.html', error = error)
    return render_template('index.html')

'''
Método que permite seleccionar el corpus y redirecciona a la pantalla de obras
'''
@app.route('/Sel-Corpus/', methods=["GET","POST"])
def selCorpus():
    error = ''
    m = mod.Modelo()
    if request.method == "POST":
        
        if('usuario' not in session or session['usuario'] not in tbd.getSesiones().keys()):
            session['usuario'] = tbd.addSesion(m)
            dirName = os.path.join(app.config['UPLOAD_FOLDER'], str(session['usuario']))
            if(not os.path.exists(dirName)):
                os.makedirs(dirName)
        tbd.replaceObject(session['usuario'],m)
        session['corpus'] = request.form['obras']
        session['fichero'] = request.form['obras']
        m.cambiarPantallas(2)
        return redirect(url_for('obras'))
    return render_template('corpus.html', corpus = m.getCorpus(), contador = 0 )

'''
Método que permite seleccionar la obra y redirecciona a la pantalla de personajes
'''
@app.route('/Sel-Obra/', methods=["GET","POST"])
def obras():
    if('corpus' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if request.method == "POST":
        obra = request.form['obra']
        corpus = session['corpus']
        m.diccionarioObras(corpus,obra)
        # Debido al formato de los grafos en las obras de teatro, la configuración inicial es un poco diferente
        session['configVis'] = {'Path to file (csv or json)': 'https://gist.githubusercontent.com/ulfaslak/6be66de1ac3288d5c1d9452570cbba5a/raw/0b9595c09b9f70a77ee05ca16d5a8b42a9130c9e/miserables.json', 'Apply heat (wiggle)': False, 'Charge strength': -100, 'Center gravity': 0.1, 'Link distance': 25, 'Link width': 2, 'Link alpha': 0.5, 'Node size': 5, 'Node stroke size': 0.5, 'Node size exponent': 0.5, 'Link width exponent': 0.5, 'Collision': False, 'Node fill': '#16a085', 'Node stroke': '#000000', 'Link stroke': '#7c7c7c', 'Label stroke': '#000000', 'Show labels': True, 'Show singleton nodes': False, 'Node size by strength': True, 'Zoom': 2, 'Min. link weight %': 0, 'Max. link weight %': 100}   
        return redirect(url_for('moddict'))
    return render_template('obras.html', obras = m.getPlays(session['corpus']))

@app.route('/Acerca', methods=["GET","POST"])
def about():
    return render_template('about.html')

@app.route('/Dicts-Automaticos/', methods=["GET", "POST"])
def dictaut():
    msg = ''
    if('fichero' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if request.method == "POST":
        if("btn btn-vacdict"  in request.form):
            m.vaciarDiccionario()
        if("btn btn-creadict" in request.form):
            m.cambiarPantallas(1)
            m.crearDict()
            msg = gettext("Diccionario creado con éxito")
        elif("btn btn-impdict" in request.form):
            return redirect(url_for('impdict'))
        elif("btn btn-obtdict" in request.form):
            return redirect(url_for('obtdict'))
    return render_template('dictaut.html',perso = m.hayPersonajes(), msg = msg)
	
@app.route('/Dicts-Automaticos/Importar-Dict/', methods=["GET","POST"])
def impdict():
    if('fichero' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if request.method == "POST":
        fich = request.files["btn btn-selcsv"]
        fullpath = os.path.join(app.config['UPLOAD_FOLDER'], str(session['usuario']), fich.filename)
        fich.save(fullpath)
        m.cambiarPantallas(1)
        m.importDict(fullpath)
    return render_template('impdict.html', perso = m.hayPersonajes())
	
@app.route('/Dicts-Automaticos/Obtener-Dict/', methods=["GET","POST"])
def obtdict():
    if('fichero' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if request.method == "POST":
        url = request.form['txt txt-url']
        m.cambiarPantallas(1)
        m.scrapeWiki(url)
    return render_template('obtdict.html', perso = m.hayPersonajes())

@app.route('/Modificar-Diccionario/', methods=["GET", "POST"])   
def moddict():
    if('fichero' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if request.method == "POST":

        ## modificado
        ajax = request.get_json(silent=True)
        if(ajax != None):
            if(ajax == 'todos'):
                m.prepararRed()
                m.obtenerEthnea(flag = (m.devolverCambio() == 2))
                return json.dumps("True")
            if(ajax == 'etniaSexo'):
                m.obtenerEthnea(flag = (m.devolverCambio() == 2))
                return json.dumps("True")
            if(ajax == 'posiciones'):
                m.prepararRed()
                return json.dumps("True")
        if("btn btn-newpers" in request.form):
            return redirect(url_for('newpers'))
        elif("btn btn-delpers" in request.form):
            return redirect(url_for('delpers'))
        elif("btn btn-joinpers" in request.form):
            return redirect(url_for('joinpers'))
        elif("btn btn-newrefpers" in request.form):
            return redirect(url_for('newrefpers'))
        elif("btn btn-delrefpers" in request.form):
            return redirect(url_for('delrefpers'))
        elif("btn btn-modid" in request.form):
            return redirect(url_for('modidpers'))
        elif("btn btn-modet" in request.form):
            return redirect(url_for('etniapers'))
        elif("btn btn-modse" in request.form):
            return redirect(url_for('sexopers'))
        elif("btn btn-expdict" in request.form):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], str(session['usuario']), session['fichero'] + ".csv")
            m.exportDict(filename)
            return send_file(filename, mimetype='text/csv', download_name=session['fichero'] + ".csv", as_attachment=True)
    return render_template('moddict.html', pers = m.getPersonajes(), cambiarPantalla = m.devolverCambio())

@app.route('/Modificar-Diccionario/Anadir-Personaje/', methods=["GET", "POST"])    
def newpers():
    if('fichero' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if (m.hayPersonajes() == 0):
        return redirect(url_for('home'))
    if request.method == "POST":
        idperso = request.form['txt txt-idpers']
        perso = request.form['txt txt-nombrepers']
        m.anadirPersonaje(idperso,perso)
    return render_template('newpers.html', pers = m.getPersonajes())

@app.route('/Modificar-Diccionario/Etnia-Personaje/', methods=["GET", "POST"])    
def etniapers():
    if('fichero' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if (m.hayPersonajes() == 0):
        return redirect(url_for('home'))
    if request.method == "POST":
        idperso = request.form['txt txt-idpers']
        etnia = request.form['txt txt-etniapers']
        m.cambiarEtnia(etnia,idperso)
    return render_template('modetnia.html', pers = m.getPersonajes())

@app.route('/Modificar-Diccionario/Sexo-Personaje/', methods=["GET", "POST"])    
def sexopers():
    if('fichero' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if (m.hayPersonajes() == 0):
        return redirect(url_for('home'))
    if request.method == "POST":
        idperso = request.form['txt txt-idpers']
        sexo = request.form['sexelection']
        m.cambiarSexo(sexo,idperso)
    return render_template('modsexo.html', pers = m.getPersonajes())

@app.route('/Modificar-Diccionario/Eliminar-Personaje/', methods=["GET", "POST"])    
def delpers():
    if('fichero' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if (m.hayPersonajes() == 0):
        return redirect(url_for('home'))
    if request.method == "POST":
        ajax = request.get_json()
        if(ajax != None):
            m.eliminarListPersonajes(ajax)
    return render_template('delpers.html', pers = m.getPersonajes())

@app.route('/Modificar-Diccionario/Juntar-Personajes/', methods=["GET", "POST"])    
def joinpers():
    if('fichero' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if (m.hayPersonajes() == 0):
        return redirect(url_for('home'))
    if request.method == "POST":
        ajax = request.get_json()
        if(ajax != None):
            m.juntarListPersonajes(ajax)
    return render_template('joinpers.html', pers = m.getPersonajes())
   
@app.route('/Modificar-Diccionario/Nueva-Referencia/', methods=["GET", "POST"])    
def newrefpers():
    if('fichero' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if (m.hayPersonajes() == 0):
        return redirect(url_for('home'))
    if request.method == "POST":
        idp = request.form['txt txt-idpers']
        ref = request.form['txt txt-refpers']
        m.anadirReferenciaPersonaje(idp,ref)
    return render_template('newrefpers.html', pers = m.getPersonajes())

@app.route('/Modificar-Diccionario/Eliminar-Referencia/', methods=["GET", "POST"])    
def delrefpers():
    if('fichero' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if (m.hayPersonajes() == 0):
        return redirect(url_for('home'))
    if request.method == "POST":
        ajax = request.get_json()
        if(ajax != None):
            m.eliminarListRefs(ajax)
    return render_template('delrefpers.html', pers = m.getPersonajes())

@app.route('/Modificar-Diccionario/Cambiar-Identificador/', methods=["GET", "POST"])
def modidpers():
    if('fichero' not in session ):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if (m.hayPersonajes() == 0):
        return redirect(url_for('home'))
    if request.method == "POST":
        idact = request.form['txt txt-idact']
        newid = request.form['txt txt-newid']
        m.modificarIdPersonaje(idact,newid)
    return render_template('modidpers.html', pers = m.getPersonajes())
    
@app.route('/Parametros/', methods=["GET", "POST"])
def params():
    global epub
    global sesion
    epub=True
    sesion=0
    if('fichero' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if (m.hayPersonajes() == 0):
        return redirect(url_for('home'))
    if request.method == "POST":
        apar = request.form['txt txt-apar']
        dist = request.form['txt txt-dist']
        caps = False
        if("cbx cbx-capitulos"  in request.form):
            caps = True
        m.generarGrafo(int(dist),int(apar),caps)          
        return redirect(url_for('red'))
    return render_template('params.html', pers = {k: v for k, v in sorted(m.getPersonajes().items(), key=lambda x: x[1].getNumApariciones(), reverse=True)})

@app.route('/Parametros-Peliculas/', methods=["GET", "POST"])
def paramsPeliculas():
    global apariciones
    global epub
    global sesion
    epub=False
    sesion=0
    if('fichero' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if (m.hayPersonajes() == 0):
        return redirect(url_for('home'))
    if request.method == "POST":
        apar = request.form['txt txt-apar']
        apariciones=apar
        m.obtenerRed(int(apar))          
        return redirect(url_for('red'))
    return render_template('paramsPeliculas.html', pers = {k: v for k, v in sorted(m.getPersonajes().items(), key=lambda x: x[1].getNumApariciones(), reverse=True)},cambiarPantalla = m.devolverCambio())

@app.route('/Red/', methods=["GET", "POST"])
def red():
    global apariciones
    if('fichero' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if (m.hayPersonajes() == 0):
        return redirect(url_for('home'))
    jsonred = m.visualizar()
    if request.method == "POST":
        if("btn btn-expgml" in request.form):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], str(session['usuario']), session['fichero'] + ".gml")
            m.exportGML(filename)
            return send_file(filename, mimetype='text/gml', download_name=session['fichero'] + ".gml", as_attachment=True)
        elif("btn btn-expgexf" in request.form):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], str(session['usuario']), session['fichero'] + ".gexf")
            m.exportGEXF(filename)
            return send_file(filename, mimetype='text/gexf', download_name=session['fichero'] + ".gexf", as_attachment=True)
        elif("btn btn-expnet" in request.form):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], str(session['usuario']), session['fichero'] + ".net")
            m.exportPajek(filename)
            return send_file(filename, mimetype='text/net', download_name=session['fichero'] + ".net", as_attachment=True)
    return render_template('red.html', jsonred = jsonred, config = session['configVis'], cambiarPantalla = m.devolverCambio())

@app.route('/redDinamica/' , methods=["GET","POST"])
def redDinamica():
    global frames
    global epub
    global sesion
    if('fichero' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if (m.hayPersonajes() == 0):
        return redirect(url_for('home'))
    tiempoMasAlto = m.ordenarRedDinamica(epub)
    slider = tiempoMasAlto[2]
    if request.method == "POST":
        # REPRODUCCIÓN AUTOMÁTICA
        ajax = request.get_json(silent=True)
        if(ajax != None):
            if(ajax == 'detener'):
                m.auto = 0
                return json.dumps("True")
            if(ajax == 'empezar'):
                if(frames+1 > slider):
                    m.auto = 0
                else:
                    frames = frames + 1
                if(frames == slider):
                    m.auto = 0
                else:
                    m.auto = 1
                return json.dumps("True")
            if(ajax == 'continuar'):
                if(frames+1 > slider):
                    m.auto = 0
                else:
                    frames = frames + 1
                if(frames == slider):
                    m.auto = 0
                return json.dumps("True")
        if("btn btn-expgml" in request.form):
            ## Desactivamos el modo automático para el resto de acciones
            m.auto = 0
            filename = os.path.join(app.config['UPLOAD_FOLDER'], str(session['usuario']), session['fichero'] + ".gml")
            m.exportGML(filename)
            return send_file(filename, mimetype='text/gml', download_name=session['fichero'] + ".gml", as_attachment=True)
        elif("btn btn-expgexf" in request.form):
            m.auto = 0
            filename = os.path.join(app.config['UPLOAD_FOLDER'], str(session['usuario']), session['fichero'] + ".gexf")
            m.exportGEXFdinamica(filename,frames,epub)
            return send_file(filename, mimetype='text/gexf', download_name=session['fichero'] + ".gexf", as_attachment=True)
        elif("btn btn-expnet" in request.form):
            m.auto = 0
            filename = os.path.join(app.config['UPLOAD_FOLDER'], str(session['usuario']), session['fichero'] + ".net")
            m.exportPajek(filename)
            return send_file(filename, mimetype='text/net', download_name=session['fichero'] + ".net", as_attachment=True)
        elif("btn btn-des" in request.form):
            m.auto = 0
            filename = os.path.join(app.config['UPLOAD_FOLDER'], str(session['usuario']), session['fichero'] + ".mp4")
            m.descargarRed(tiempoMasAlto[2],filename,epub)
            return send_file(filename, mimetype='text/mp4', download_name=session['fichero'] + ".mp4", as_attachment=True)
        elif("btn btn-desact" in request.form):
            m.auto = 0
            filename = os.path.join(app.config['UPLOAD_FOLDER'], str(session['usuario']), session['fichero'] + ".mp4")
            m.descargarRed(frames,filename,epub)
            return send_file(filename, mimetype='text/mp4', download_name=session['fichero'] + ".mp4", as_attachment=True)
        elif("btn btn-anterior" in request.form):
            m.auto = 0
            frames = frames-1
            jsonred = m.vistaDinamica(int(frames),epub)
            return render_template('redDinamica.html', jsonred = jsonred, config = session['configVis'], cambiarPantalla = m.devolverCambio(),value=frames, slider=slider , auto=m.auto)
        elif("btn btn-siguiente" in request.form):
            m.auto = 0
            frames = frames+1
            jsonred = m.vistaDinamica(int(frames),epub)
            return render_template('redDinamica.html', jsonred = jsonred, config = session['configVis'], cambiarPantalla = m.devolverCambio(), value=frames, slider=slider, auto=m.auto )
        elif("btn btn-buscar" in request.form):
            m.auto = 0
            frames=int(request.form['txt txt-inter'])
            jsonred = m.vistaDinamica(int(frames),epub)
            return render_template('redDinamica.html', jsonred = jsonred, config = session['configVis'], cambiarPantalla = m.devolverCambio(), value=frames, slider=slider, auto=m.auto )   
    elif sesion == 0:
        tiempoMasAlto = m.ordenarRedDinamica(epub)
        frames = tiempoMasAlto[2]
        jsonred = m.vistaDinamica(int(frames),epub)   
        sesion=1
    else:
        jsonred = m.vistaDinamica(int(frames),epub) 

    return render_template('redDinamica.html', jsonred = jsonred, config = session['configVis'], cambiarPantalla = m.devolverCambio(), value=frames, slider=slider, auto=m.auto )


@app.route('/Informe/', methods=["GET", "POST"])
def informe():
    if('fichero' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if (m.hayPersonajes() == 0):
        return redirect(url_for('home'))
    if request.method == "POST":
        x = dict(request.form)
        direc = os.path.join(app.config['UPLOAD_FOLDER'], str(session['usuario']))
        m.generarInforme(x,direc)
        return redirect(url_for('visinforme'))
    return render_template('informe.html')

@app.route('/Informe/Visualizar/', methods=["GET", "POST"])
def visinforme():
    if('fichero' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if (m.hayPersonajes() == 0):
        return redirect(url_for('home'))
    return render_template('visinforme.html', informe = m.informe)

@app.route('/InformeDinamica/', methods=["GET", "POST"])
def informeDinamico():
    if('fichero' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if (m.hayPersonajes() == 0):
        return redirect(url_for('home'))
    if request.method == "POST":
        x = dict(request.form)
        direc = os.path.join(app.config['UPLOAD_FOLDER'], str(session['usuario']))
        m.generarInforme(x,direc)
        return redirect(url_for('visinformeDinamica'))
    return render_template('informedinamico.html')

@app.route('/InformeDinamicaConf/', methods=["GET", "POST"])
def informeDinamicoconf():
    global epub
    if('fichero' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if (m.hayPersonajes() == 0):
        return redirect(url_for('home'))
    if request.method == "POST":
        x = dict(request.form)
        direc = os.path.join(app.config['UPLOAD_FOLDER'], str(session['usuario']))
        m.generarInformeDinamico(x,direc,epub)
        return redirect(url_for('visinformeDinamicaconf'))
    return render_template('informedinamicoconf.html')

@app.route('/InformeDinamicaConf/Visualizar/', methods=["GET", "POST"])
def visinformeDinamicaconf():
    global frames
    if('fichero' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if (m.hayPersonajes() == 0):
        return redirect(url_for('home'))
    lista=m.generarValoresDescargaInforme()
    personajes=m.elementosRed()
    return render_template('visinformedinamicaconf.html', informe = m.informeDina, intervalos=frames, personajes=personajes, lista=str(lista))

@app.route('/InformeDinamica/Visualizar/', methods=["GET", "POST"])
def visinformeDinamica():
    if('fichero' not in session or session['usuario'] not in tbd.getSesiones().keys()):
        return redirect(url_for('home'))
    g.usuario = session['usuario']
    m = tbd.getObject(session['usuario'])
    if (m.hayPersonajes() == 0):
        return redirect(url_for('home'))
    return render_template('visinformedinamica.html', informe = m.informe)

@app.route('/Informe/Visualizar/<path:filename>')
def download_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], str(session['usuario'])), filename, as_attachment=True)

@app.route('/Idioma/', methods=["GET", "POST"])
def idioma():
    if request.method == "POST":
        ajax = request.get_json()
        session['lang'] = ajax
        return "true"
    
@app.route('/Guardar-Config/', methods=["GET", "POST"])
def guardarConfig():
    if request.method == "POST":
        config = request.get_json()
        session['configVis'] = config
        return "true"
        
@app.route('/Fin-Sesion', methods=["GET", "POST"])
def finSesion():
    if request.method == "POST":
        ajax = request.get_json()
        tbd.delSesion(int(ajax))
        shutil.rmtree(os.path.join(app.config['UPLOAD_FOLDER'], str(session['usuario'])))
        session['fichero'] = "null"
        session['usuario'] = "null"
        session['corpus'] = "null"
        session['obra'] = "null"
        return "true"