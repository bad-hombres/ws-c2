
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
