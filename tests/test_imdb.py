from tests import FlexGetBase
from nose.plugins.attrib import attr
import os

class TestImdbOnline(FlexGetBase):
    __yaml__ = """
        feeds:
          test:
            input_mock:
              # tests search
              - {title: 'Spirited Away', url: 'http://localhost/imdb/spirited_away'}
              # tests direct url
              - {title: 'Princess Mononoke', url: 'http://localhost/imdb/princess_mononoke', imdb_url: 'http://www.imdb.com/title/tt0119698/'}
              # generic test material, some tricky ones here :)
              - {title: 'Taken[2008]DvDrip[Eng]-FOO', url: 'http://localhost/Taken' }
            imdb:
              min_votes: 20

          year:
            input_mock:
              - {title: 'Princess Mononoke', url: 'http://localhost/imdb/princess_mononoke', imdb_url: 'http://www.imdb.com/title/tt0119698/'}
              - {title: 'Taken[2008]DvDrip[Eng]-FOO', url: 'http://localhost/Taken', imdb_url: 'http://www.imdb.com/title/tt0936501/' }
            imdb:
              min_year: 2003
    """
    @attr(online=True)
    def testMovies(self):
        self.execute_feed('test')
        assert self.feed.find_entry(imdb_name='Sen to Chihiro no kamikakushi'), 'Failed IMDB lookup (search)'
        assert self.feed.find_entry(imdb_name='Mononoke-hime'), 'Failed imdb lookup (direct)'
        assert self.feed.find_entry(imdb_name='Taken', imdb_url='http://www.imdb.com/title/tt0936501/'), 'Failed to pick correct Taken from search results'

    @attr(online=True)
    def testYear(self):
        self.execute_feed('year')
        assert self.feed.find_entry('accepted', imdb_name='Taken'), 'Taken should\'ve been accepted'
        assert self.feed.find_entry('rejected', imdb_name='Mononoke-hime'), 'Mononoke-hime should\'ve been rejected'

class TestScanImdb(FlexGetBase):
    __yaml__ = """
        feeds:
          test:
            input_mock:
              - {title: 'Scan Test 1', url: 'http://localhost/scanimdb/1', description: 'title: Foo Bar Asdf\n imdb-url: http://www.imdb.com/title/tt0330793/ more text'}
              - {title: 'Scan Test 2', url: 'http://localhost/scanimdb/2', description: '<a href="http://imdb.com/title/tt0472198/">IMDb</a>'}
              - {title: 'Scan Test 3', url: 'http://localhost/scanimdb/3', description: 'nothing here'}
    """
    def testScanImdb(self):
        self.execute_feed('test')
        assert self.feed.find_entry(imdb_url='http://www.imdb.com/title/tt0330793'), 'Failed pick url from test 1'
        assert self.feed.find_entry(imdb_url='http://imdb.com/title/tt0472198'), 'Failed pick url from test 2'
