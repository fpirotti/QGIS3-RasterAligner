# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RasterAligner
                                 A QGIS plugin
 Aligns Rasters by detecting features aligning via different methods
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-08-04
        copyright            : (C) 2021 by Francesco Pirotti - CIRGEO Interdepartmental Research Center in Geomatics
        email                : francesco.pirotti@unipd.it
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'Francesco Pirotti - CIRGEO Interdepartmental Research Center in Geomatics'
__date__ = '2021-08-04'
__copyright__ = '(C) 2021 by Francesco Pirotti - CIRGEO Interdepartmental Research Center in Geomatics'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load RasterAligner class from file RasterAligner.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .raster_aligner import RasterAlignerPlugin
    return RasterAlignerPlugin()
