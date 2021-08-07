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
"""

__author__ = 'Francesco Pirotti - CIRGEO Interdepartmental Research Center in Geomatics'
__date__ = '2021-08-04'
__copyright__ = '(C) 2021 by Francesco Pirotti - CIRGEO Interdepartmental Research Center in Geomatics'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'




import inspect
import cv2 as cv
import gdal
from qgis.PyQt.QtGui import QIcon
from qgis.core import *
from qgis.utils import *


class RasterAlignerAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    OUTPUT = 'OUTPUT'
    INPUTmaster = 'INPUTmaster'
    INPUTslaves = 'INPUTslaves'
    gdal.AllRegister()
    # this allows GDAL to throw Python Exceptions
    gdal.UseExceptions()
    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector features source. It can have any kind of
        # geometry.
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUTmaster,
                self.tr('Master Raster')
            )
        )

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUTslaves,
                self.tr('Slave Rasters'),
                QgsProcessing.TypeRaster
            )
        )
        # We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output layer')
            )
        )

    def layerAsArray(self, layer, feedback):
        """ read the data from a single-band layer into a numpy/Numeric array.
        Only works for gdal layers!
        """
        feedback.pushInfo(layer)
        gd = gdal.Open(str(layer), gdal.GA_ReadOnly)
        array = gd.ReadAsArray()
        return array

    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(cmd_folder, 'logo.png')))
        return icon

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        source = self.parameterAsSource(parameters, self.INPUTmaster, context)
        if source is not None:
            (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT,
                                                   context, source.fields(), source.wkbType(), source.sourceCrs())

        # Compute the number of steps to display within the progress bar and
        # get features from source
        #total = 100.0 / source.featureCount() if source.featureCount() else 0
        #features = source.getFeatures()

        dest_id="...."
        #lyr = self.parameterAsFile(parameters, self.INPUTmaster, context)
        lyr = self.parameterDefinition('INPUTmaster').valueAsPythonString(parameters['INPUTmaster'], context).strip("'")
        feedback.pushInfo(".............")
        feedback.pushInfo(lyr)

        if lyr is not None and lyr is not None:
            feedback.pushInfo(".............")
            gray = self.layerAsArray(lyr, feedback)

            if gray is None:
                feedback.pushInfo("Not able to read "+lyr+" file")
                return

            if gray.size == 3:
                feedback.pushInfo("Converting to gray scale for SIFT")
                gray = cv.cvtColor(gray, cv.COLOR_BGR2GRAY)

            sift = cv.SIFT_create()

            surf = cv.xfeatures2d.SURF_create(400)
            surf.setUpright(True) # faster ignores orientation
            surf.setExtended(True)
            kp, des = surf.detectAndCompute(img, None)
            surf.setHessianThreshold(500)

            feedback.pushInfo("Detecting and computing SIFT")
            kp, des = sift.detectAndCompute(gray, None)
            feedback.pushInfo(kp.size)
        # fett = []
        # nmealayer = QgsVectorLayer("Point", layername, "memory")
        # for a, point in enumerate(kp):
        #     fet = QgsFeature()
        #     fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(point[0], point[1])))
        #     attributess = []
        #     for aa in att:
        #         attributess.append(aa[a])
        #     fet.setAttributes(attributess)
        #     fett.append(fet)


        else:
            print("You have to select a RASTER layer")

        #for current, feature in enumerate(features):
        # Stop the algorithm if cancel button has been clicked
        #    if feedback.isCanceled():
        #        break

        # Add a feature in the sink
        #    sink.addFeature(feature, QgsFeatureSink.FastInsert)

        # Update the progress bar
        #    feedback.setProgress(int(current * total))

        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        return {self.OUTPUT: dest_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Find and match features'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Raster'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return RasterAlignerAlgorithm()

    def normalize(self, imgnp, t_min, t_max):
        norm_arr = []
        diff = t_max - t_min
        diff_arr = arr.max() - arr.min()
        min = arr.min()

        for i in arr:
            temp = (((i - min) * diff) / diff_arr) + t_min
            norm_arr.append(temp)
        return norm_arr


import numpy as np
ff="C:\\Users\\FrancescoAdmin\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\RasterAligner\\Landsat8Padova.tif"
gd = gdal.Open(ff, gdal.GA_ReadOnly)
arr = gd.ReadAsArray()
normIm = np.array( normalize(None, arr, 0, 255), np.uint8)

surf = cv.xfeatures2d.SURF_create(400)
surf.setUpright(True)  # faster ignores orientation
surf.setExtended(True)
kp, des = surf.detectAndCompute(img, None)

window_name = 'image'
cv.imshow(window_name, normIm)
cv.waitKey(0)
cv.destroyAllWindows()

