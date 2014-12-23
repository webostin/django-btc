import warnings

from django.template.base import TemplateSyntaxError
from django.template.loader import get_template
from django.test import SimpleTestCase
from django.utils.deprecation import RemovedInDjango20Warning

from ..utils import render, setup


class FirstOfTagTests(SimpleTestCase):

    @setup({'firstof01': '{% firstof a b c %}'})
    def test_firstof01(self):
        output = render('firstof01', {'a': 0, 'c': 0, 'b': 0})
        self.assertEqual(output, '')

    @setup({'firstof02': '{% firstof a b c %}'})
    def test_firstof02(self):
        output = render('firstof02', {'a': 1, 'c': 0, 'b': 0})
        self.assertEqual(output, '1')

    @setup({'firstof03': '{% firstof a b c %}'})
    def test_firstof03(self):
        output = render('firstof03', {'a': 0, 'c': 0, 'b': 2})
        self.assertEqual(output, '2')

    @setup({'firstof04': '{% firstof a b c %}'})
    def test_firstof04(self):
        output = render('firstof04', {'a': 0, 'c': 3, 'b': 0})
        self.assertEqual(output, '3')

    @setup({'firstof05': '{% firstof a b c %}'})
    def test_firstof05(self):
        output = render('firstof05', {'a': 1, 'c': 3, 'b': 2})
        self.assertEqual(output, '1')

    @setup({'firstof06': '{% firstof a b c %}'})
    def test_firstof06(self):
        output = render('firstof06', {'c': 3, 'b': 0})
        self.assertEqual(output, '3')

    @setup({'firstof07': '{% firstof a b "c" %}'})
    def test_firstof07(self):
        output = render('firstof07', {'a': 0})
        self.assertEqual(output, 'c')

    @setup({'firstof08': '{% firstof a b "c and d" %}'})
    def test_firstof08(self):
        output = render('firstof08', {'a': 0, 'b': 0})
        self.assertEqual(output, 'c and d')

    @setup({'firstof09': '{% firstof %}'})
    def test_firstof09(self):
        with self.assertRaises(TemplateSyntaxError):
            get_template('firstof09')

    @setup({'firstof10': '{% firstof a %}'})
    def test_firstof10(self):
        output = render('firstof10', {'a': '<'})
        self.assertEqual(output, '&lt;')

    @setup({'firstof11': '{% load firstof from future %}{% firstof a b %}'})
    def test_firstof11(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RemovedInDjango20Warning)
            output = render('firstof11', {'a': '<', 'b': '>'})
        self.assertEqual(output, '&lt;')

    @setup({'firstof12': '{% load firstof from future %}{% firstof a b %}'})
    def test_firstof12(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RemovedInDjango20Warning)
            output = render('firstof12', {'a': '', 'b': '>'})
        self.assertEqual(output, '&gt;')

    @setup({'firstof13': '{% load firstof from future %}'
                         '{% autoescape off %}{% firstof a %}{% endautoescape %}'})
    def test_firstof13(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RemovedInDjango20Warning)
            output = render('firstof13', {'a': '<'})
        self.assertEqual(output, '<')

    @setup({'firstof14': '{% load firstof from future %}{% firstof a|safe b %}'})
    def test_firstof14(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RemovedInDjango20Warning)
            output = render('firstof14', {'a': '<'})
        self.assertEqual(output, '<')
