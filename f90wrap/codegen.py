# HF XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# HF X
# HF X   f90wrap: F90 to Python interface generator with derived type support
# HF X
# HF X   Copyright James Kermode 2011
# HF X
# HF X   These portions of the source code are released under the GNU General
# HF X   Public License, version 2, http://www.gnu.org/copyleft/gpl.html
# HF X
# HF X   If you would like to license the source code under different terms,
# HF X   please contact James Kermode, james.kermode@gmail.com
# HF X
# HF X   When using this software, please cite the following reference:
# HF X
# HF X   http://www.jrkermode.co.uk/f90wrap
# HF X
# HF XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

class CodeGenerator(object):
    """
    Simple class to handle code generation.
    
    Handles simple tasks such as indent/dedent and continuation symbols.
    
    Parameters
    ----------
    indent : `str`
        Specification of the indent size/type. Typical choices may be ``" "*4``
        or ``"\t"``.
        
    max_length : `int`
        Maximum length of a code line.
        
    continuation : `str`
        Symbol to represent continuation in the desired language (eg. '&' in 
        Fortran)
    """

    def __init__(self, indent, max_length, continuation):
        self._indent = indent
        self.max_length = max_length
        self.continuation = continuation
        self.level = 0
        self.code = []

    def indent(self):
        """Indent code level"""
        self.level += 1

    def dedent(self):
        """Dedent code level"""
        self.level -= 1

    def write(self, *args):
        """
        Write arbitrary string arguments to the instance's code, split by
        newline characters and implied newline after last arg.
        """
        if args is ():
            args = ('\n',)
        args = ' '.join(args).rstrip() + '\n'
        lines = args.splitlines(True)
        self.code.extend([self._indent * self.level + line for line in lines])

    def writelines(self, items):
        """
        Write the given code lines to the instance's code. 
        
        Parameters
        ----------
        items : list of strings
            A list of code lines to be appended to the instance's code.
            Newline characters with strings will automatically be propagated
            into the code.
        """
        lines = []
        for item in items:
            lines.extend(item.splitlines(True))
        self.code.extend([self._indent * self.level + line for line in lines])

    def split_long_lines(self):
        """Split lines longer than `max_length` using `continuation`"""
        out = []
        for line in self.code:
            if len(line) > self.max_length:
                indent = line[:len(line) - len(line.lstrip())]
                tokens = line.split()
                split_lines = [[]]
                while tokens:
                    token = tokens.pop(0)
                    current_line = ' '.join(split_lines[-1])
                    if len(current_line) + len(token) < self.max_length:
                        split_lines[-1].append(token)
                    else:
                        split_lines[-1].append(self.continuation)
                        split_lines.append([self._indent + token])
                out.extend([indent + ' '.join(line) + '\n' for line in split_lines])
            else:
                out.append(line)
        return out

    def __str__(self):
        return "".join(self.split_long_lines())
