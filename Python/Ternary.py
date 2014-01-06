from matplotlib.mlab import csv2rec
from math import sqrt
import matplotlib.pyplot as p

class TernaryPlot:#(filename):
    """A Script Used to generate clean Ternary Phase Diagrams given a csv file of triplet pairs, Including Axis Titles."""
    
    def _toCart(self, triplet):
        '''Takes in triplet values, and recalculates them as cartesian coordinates. '''
        global type
        global sqrt
        assert (type(triplet)==type([]))
        cartxs = []
        cartys = []
        for triple in triplet:
            (b, l, r) = triple
            assert (b + l + r == 100), "3-coordinate values must sum to 100; %d, %d, %d don't" % (b, l, r)
            cartxs.append(100 - b - l / 2.0)
            cartys.append(sqrt(3) * l / 2.0)
        return (cartxs, cartys)

    def satisfies_bounds(self, point, limits):
        'point is 3 coordinates; limits is 3 pairs. Returns True or False (for closed set).'
        global True
        global False
        for i in [0, 1, 2]:
            if not (limits[i][0] <= point[i] <= limits[i][1]):
                return False
        return True

    def scatter(self, threecoords, **kwargs):
        'Scatterplots data given in triples, with the matplotlib keyword arguments'
        global p
        (xs, ys) = self._toCart(threecoords)
        p.scatter(xs, ys, **kwargs)

    def plot(self, threecoords, descriptor, **kwargs):
        'Plots data given in triples, with most of the matplotlib keyword arguments'
        global p
        (xs, ys) = self._toCart(threecoords)
        p.plot(xs, ys, descriptor, **kwargs)

    def colorbar(self, label):
        'Draws the colorbar and labels it'
        global p
        cb = p.colorbar()
        cb = cb.set_label(label)

    def line(self, begin, end, simplestyle = 'k-', **kwargs):
        global p
        (xs, ys) = self._toCart([begin, end])
        p.plot(xs, ys, simplestyle, **kwargs)

    def outline(self):
        self.line((0, 100, 0), (100, 0, 0), 'k-')
        self.line((0, 100, 0), (0, 0, 100), 'k-')
        self.line((0, 0, 100), (100, 0, 0), 'k-', label='_nolegend_')

    def grid(self, triple = ([25, 50, 100], [25, 50, 100], [25, 50, 100]), labels = ()):
        'Grid lines will be drawn for ([bottom],[left],[right]) values.'
        global p
        global str
        global len
        global sqrt
        (bs, ls, rs) = triple
        lstyle = {'color': '0.6',
         'dashes': (1, 1),
         'linewidth': 0.5}
        for b in bs:
            assert 0 <= b <= 100, 'Bottom value not in 0-100 range'
            self.line((b, 0, 100 - b), (b, 100 - b, 0), **lstyle)
            p.text(b, -5, b, rotation=300, fontsize=9)
        for l in ls:
            assert 0 <= l <= 100, 'Left value not in 0-100 range'
            self.line((0, l, 100 - l), (100 - l, l, 0), **lstyle)
            p.text(l/ 2.0 - 2 * len(str(l)), sqrt(3) * l / 2 - 1, 100 - l, fontsize=9)
        for r in rs:
            assert 0 <= r <= 100, 'Right value not in 0-100 range'
            self.line((0, 100 - r, r), (100 - r, 0, r), **lstyle)
            p.text(50 + r / 2.0, sqrt(3) * (51 - r / 2.0), 100 - r, rotation=60, fontsize=9)
        if (len(labels) > 0):
            p.text(50 - len(labels[0]) / 2, -12, labels[0], fontsize=8)
            p.text(15 - len(labels[1]) / 2, sqrt(3) * (25 - len(labels[1]) / 2), labels[1], rotation=60, fontsize=8)
            p.text(82 - len(labels[2]) / 2, 48 - len(labels[2]) / 2, labels[2], rotation=300, fontsize=8)

    def axistitles(self, sclabel = '_nolegend_', labelnames=['Cu','Sn','Zn']):
        global p
        global range
        global sqrt
        global len
        self.grid((range(10, 100, 10), range(10, 100, 10), range(10, 100, 10)))
        p.text(50 - len(labelnames[0]), 90, labelnames[0])
        p.text(len(labelnames[1]) - 10, 0, labelnames[1])
        p.text(100 + len(labelnames[2]), 0, labelnames[2])

    def patch(self,limits, **kwargs):
        '''Fill the area bounded by limits.
        Limits format: [[bmin,bmax],[lmin,lmax],[rmin,rmax]]
        Other arguments as for pylab.fill()'''
        coords = []
        bounds = [[1,-1,1],[1,0,-1],[-1,0,0],[1,-1,0],[1,1,-1],[-1,1,0],[0,-1,0],
                  [0,1,-1],[-1,1,1],[0,-1,1],[0,0,-1],[-1,0,1]]
        for pt in bounds:     #plug in values for these limits
            for i in [0,1,2]:
                if pt[i] == 1: 
                    pt[i] = limits[i][1]
                else:
                    if pt[i] == 0:pt[i] = limits[i][0]
            for i in [0,1,2]:
                if pt[i] == -1: pt[i] = 99 - sum(pt) 
            if self.satisfies_bounds(pt, limits): coords.append(pt) 
        coords.append(coords[0]) #close the loop
        xs, ys = self._toCart(coords)
        p.fill(xs, ys, **kwargs) 

    def scatter_from_csv(self, filename, sand = 'sand', silt = 'silt', clay = 'clay', diameter = '', hue = '', tags = '', **kwargs):
        """Loads data from filename (expects csv format). Needs one header row with at least the columns {sand, silt, clay}. Can also plot two more variables for each point; specify the header value for columns to be plotted as diameter, hue. Can also add a text tag offset from each point; specify the header value for those tags.
        Note! text values (header entries, tag values ) need to be quoted to be recognized as text. """
        fh = file(filename, 'rU')
        soilrec = csv2rec(fh)
        count = 0
        if (sand in soilrec.dtype.names):
            count = count + 1
        if (silt in soilrec.dtype.names):
            count = count + 1
        if (clay in soilrec.dtype.names):
            count = count + 1
        if (count < 3):
            print "ERROR: need columns for sand, silt and clay identified in ', filename"
        locargs = {'s': None, 'c': None}
        for (col, key) in ((diameter, 's'), (hue, 'c')):
            col = col.lower()
            if (col != '') and (col in soilrec.dtype.names):
                locargs[key] = soilrec.field(col)
            else:
                print 'ERROR: did not find ', col, 'in ', filename
        for k in kwargs:
            locargs[k] = kwargs[k]
        values = zip(*[soilrec.field(sand), soilrec.field(clay), soilrec.field(silt)])
        print values
        (xs, ys) = self._toCart(values)
        p.scatter(xs, ys, label='_', **locargs)
        if (tags != ''):
            tags = tags.lower()
            for (x, y, tag) in zip(*[xs, ys, soilrec.field(tags)]):
                print x,
                print y,
                print tag
                p.text(x + 1, y + 1, tag, fontsize=12)
        fh.close()

    def line_from_csv(self, filename, copper = 'Cu', zinc = 'Zn', tin = 'Sn', sulphur = 'S', **kwargs):
        """Loads data from filename (expects csv format). Needs one header row with at least the columns {sand, silt, clay}. Can also plot two more variables for each point; specify the header value for columns to be plotted as diameter, hue. Can also add a text tag offset from each point; specify the header value for those tags.
        Note! text values (header entries, tag values ) need to be quoted to be recognized as text. """
        fh = file(filename, 'rU')
        element = csv2rec(fh)
        count = 0
        if (copper in element.dtype.names):
            count = count + 1
        if (zinc in element.dtype.names):
            count = count + 1
        if (tin in element.dtype.names):
            count = count + 1
        if (sulphur in element.dtype.names):
            count = count + 1
        if (count != 3):
            print "ERROR: need exactly 3 columns for elements identified in ', filename"
        
        values = zip(*[element.field(sand), element.field(clay), element.field(silt)])
        print values
        (xs, ys) = self._toCart(values)
        p.scatter(xs, ys, label='_', **locargs)
        if (tags != ''):
            tags = tags.lower()
            for (x, y, tag) in zip(*[xs, ys, element.field(tags)]):
                print x,
                print y,
                print tag
                p.text(x + 1, y + 1, tag, fontsize=12)
        fh.close()

    def __init__(self, stitle = ''):
        global p
        global True
        p.clf()
        p.axis('off')
        p.axis('equal')
        p.hold(True)
        p.title(stitle)
        self.outline()

    def text(self, loctriple, word, **kwargs):
        global p
        (x, y) = self._toCart([loctriple])
        p.text(x[0], y[0], word, **kwargs)

    def show(self, filename = 'trianglegraph_test'):
        global p
        p.legend(loc=1)
        p.axis([-10, 110, -10, 110])
        p.ylim(-10, 100)
        p.savefig(filename)
        p.show()

    def close(self):
        global p
        p.close()
