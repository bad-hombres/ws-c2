
def banner():
    print Colour.red("""
                                    ,;;::;,,                                    
                                ,clllcccccccccc:'                               
                              ,odol'          ,coc'                             
                             :xoldc'            'od'                            
                            ckclko:'             'xx'                           
                           ;Oolko:;               c0l                           
                '',;:cclllo0Olxxcc:               ,O0:''''''                    
     ';:clllllcccccllodxxdkNkdOdll;                dNOddolccccc::::::cc:;,      
   'coxdl:;,,'        :looOWkdOoll;                lXOllc:;'     ''',,;:ldxo'   
   :lclooooolc;,'   ':lood0WkxOolc;                lNOllccc:,'''',;;::::;'ok,   
   ;ooxdoc;oOkodddodxkkkkxKWNXXKOOxooooooodxxxxkkOOKXkdoooolllcccol:;,cxl;oc    
    ,lxdoolcod:  'cxkxoccclookKkodooooxkkdooollcoxo;,,''';o:    lxol;,odlxd     
      ;clll:ccoocddclllo;   cdoo:    ,dxxo,    cxxdo;   :xkdo: cdcolcollxd,     
         ;cloloOOc ;oc';odoxd::cdo' ldlccod: ,do:clcll:locdl;cddccxolool;       
            ',:cccccodl:;cdo',lc;lxxl';lc;,lodc ,loc;lO0doxxolddllcc;,          
                   ',;:clllcccloookOdoxxdxookxooooooooollc::,'                  
                                ',,;;;;;;;;;;;,'                                

                                HombresC2 v0.1 (c) Bad Hombres 2018
    """, bold = True)

class Colour(object):
    colours = {
        "red": "31",
        "blue": "34",
        "green": "32",
        "cyan": "36",
        "yellow": "33"
    }

    @staticmethod
    def __getColourString__(colour, message, bold, underline):
        tmp = Colour.colours[colour]
        if bold: tmp = tmp + ";1"
        if underline: tmp = tmp + ";4"

        return u"\u001b[{}m{}\u001b[0m".format(tmp, message)

    @staticmethod
    def red(message, bold=False, underline=False):
        return Colour. __getColourString__("red", message, bold, underline)

    @staticmethod
    def blue(message, bold=False, underline=False):
        return Colour.__getColourString__("blue", message, bold, underline)

    @staticmethod
    def green(message, bold=False, underline=False):
        return Colour.__getColourString__("green", message, bold, underline)
    
    @staticmethod
    def yellow(message, bold=False, underline=False):
        return Colour.__getColourString__("yellow", message, bold, underline)

    @staticmethod
    def cyan(message, bold=False, underline=False):
        return Colour.__getColourString__("cyan", message, bold, underline)
