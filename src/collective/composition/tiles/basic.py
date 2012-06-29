# -*- coding: utf-8 -*-

# Basic implementation taken from
# http://davisagli.com/blog/using-tiles-to-provide-more-flexible-plone-layouts

import time
from datetime import datetime
from logging import exception
from Acquisition import aq_base
from ZODB.POSException import ConflictError
from persistent.dict import PersistentDict
from AccessControl.ZopeGuards import guarded_getattr
from zope import schema
from zope.annotation import IAnnotations
from zope.interface import implements
from zope.component import adapts

from zope.publisher.browser import BrowserView

from plone.namedfile.interfaces import HAVE_BLOBS
from plone.namedfile.field import NamedImage
if HAVE_BLOBS:
    from plone.namedfile.field import NamedBlobImage as NamedImage

from plone.tiles.interfaces import ITileDataManager
from plone.tiles.data import PersistentTileDataManager

from plone.app.textfield.interfaces import ITransformer

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.composition import _
from collective.composition.tiles.base import IPersistentCompositionTile
from collective.composition.tiles.base import PersistentCompositionTile


class IBasicTileData(IPersistentCompositionTile):

    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
        )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
        )

    image = NamedImage(
        title=_(u'Image'),
        required=False,
        )

    def get_title():
        """
        A method to return the title stored in the tile
        """

    def get_description():
        """
        A method to return the description stored in the tile
        """

    def get_image():
        """
        A method to return the image stored in the tile
        """

    def populate_with_object(obj):
        """
        This method will take a CT object as parameter, and it will store the
        content of the 'text' field into the tile.
        """

    def delete():
        """
        This method removes the persistent data created for this tile
        """


class BasicTile(PersistentCompositionTile):

    implements(IPersistentCompositionTile)

    index = ViewPageTemplateFile("templates/basic.pt")

    is_configurable = True

    def get_title(self):
        return self.data['title']

    def get_description(self):
        return self.data['description']

    def get_image(self):
        return self.data['image']

    def is_empty(self):
        return not(self.data['title'] or \
                   self.data['description'] or \
                   self.data['image'])

    def populate_with_object(self, obj):
        super(BasicTile, self).populate_with_object(obj)

        data_mgr = ITileDataManager(self)

        data_mgr.set({'title': obj.Title(),
                      'description': obj.Description(),
                      })

    def delete(self):
        data_mgr = ITileDataManager(self)
        data_mgr.delete()

    def accepted_ct(self):
        valid_ct = ['Document', 'File', 'Image', 'Link', 'News Item']
        return valid_ct
