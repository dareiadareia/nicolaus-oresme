__author__ = 'dareia'
import re


latex = open('/Users/dareia/nicolaus-oresme/quaestio1.4-latex.txt', 'r')
target = open('/Users/dareia/nicolaus-oresme/txt.txt', 'w')
test = open('/Users/dareia/nicolaus-oresme/smallpart.txt', 'r')

lines = latex.readlines() #choose a file from above to run the program on
output = []

# this is a function that makes the <app><lem><rdg> stuff; it will be referred to later a variant_encoding
def variant_encoding(line):
    m = re.search('{\\edtext{(.*)}{\\Afootnote{(.*)\\emph{(.*)}{4}', line)
    lem = m.group(1)
    rdg = m.group(2)[:-1]
    wit = m.group(3).strip('\n')
    print lem, rdg, wit
    if rdg == '':
        newline = line.replace(m.group(0), """\n<app>\n<lem wit='%s'>%s</lem>\n</app>\n""" % (wit, lem))
        return newline
    else:
        newline = line.replace(m.group(0), """\n<app>\n<lem>%s</lem>\n<rdg wit='%s'>%s</rdg>\n</app>\n""" % (lem, wit, rdg))
        return newline

for line in lines:
    print '---' #just to see where new analysis begins and ends
    print line
    line = line.replace("\pstart", "\n<p>\n")
    line = line.replace("\pend", "\n</p>\n")
    line = line.replace("\\begin{center}", "\n<center>\n")
    line = line.replace("\\end{center}", "\n</center>\n")
    if re.search('numbering', line):
        line = ''
    print line.count("edtext")
    if line.count("edtext") > 0:
        if line.count("edtext") == 1:
            m = re.search('{.edtext{(.*)}{.Afootnote{(.*).emph{.(.*)}{4}', line)
            lem = m.group(1)
            rdg = m.group(2)[:-1]
            wit = m.group(3)
            print lem, rdg, wit
            if rdg == '':
                newline = line.replace(m.group(0), """\n<app>\n<lem wit='%s'>%s</lem>\n</app>\n""" % (wit, lem))
                line = newline
            else:
                newline = line.replace(m.group(0), """\n<app>\n<lem>%s</lem>\n<rdg wit='%s'>%s</rdg>\n</app>\n""" % (lem, wit, rdg))
                line = newline
        else:
            counter = line.count("edtext")
            while counter >= 1:
                k = line
                i = k.find("\edtext")
                j = k.find("}}}}")
                l = k[i-1:j+4]
                m = re.search('{.edtext{(.*)}{.Afootnote{(.*).emph{(.*)}{4}', l) #the same function with lemmata and readings
                lem = m.group(1)
                rdg = m.group(2)
                wit = m.group(3)
                print lem, rdg, wit
                if rdg == '':
                    newl = l.replace(m.group(0), """\n<app>\n<lem wit='%s'>%s</lem>\n</app>\n""" % (wit, lem))
                else:
                    newl = l.replace(m.group(0), """\n<app>\n<lem>%s</lem>\n<rdg wit='%s'>%s</rdg>\n</app>\n""" % (lem, wit, rdg))
                line = line.replace(l, newl)
                print "NEW LINE IS", newl
                print line
                counter -= 1
    n = re.search('{.*guilsinglleft(.*)guilsinglright}', line) #paragraph numbers
    if n:
        newline = line.replace(n.group(0), '<pnr>%s</pnr>' % n.group(1).rstrip('\\'))
        line = newline
    o = re.search('.emph{(.*)}.footnote{(.*)}', line)
    if o: # if there is something in italics with a footnote following (=Quellenangabe)
        title = o.group(1)
        full = o.group(2).replace('\\emph{', '').replace('\\textsc{', '').replace('}', '')
        print full
        newline = line.replace(o.group(0), """<title type='short'>%s<note>%s</note></title>""" % (title, full))
        line = newline
        p = re.search('.emph{(.*)}', line)
        if p: #if there is just an italicized word (=Terminus)
            newline = line.replace(p.group(0), """<rs type="term">%s</rs>""" % p.group(1))
            line = newline
    else: #keine Quellenangabe > direkt zu den Termini
        p = re.search('.emph{(.*)}', line)
        if p:
            newline = line.replace(p.group(0), """<rs type="term">%s</rs>""" % p.group(1))
            line = newline
    print line
    output.append(line)


newlines = [x.rstrip('\n') for x in output if x != '\n' and x != '']


target.writelines(newlines)
