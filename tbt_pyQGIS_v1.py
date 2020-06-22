from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Tblt1(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('class', 'Class', types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('classfield', 'Class field', type=QgsProcessingParameterField.Any, parentLayerParameterName='class', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('zone', 'Zone', types=[QgsProcessing.TypeVector], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('zonefield', 'Zone field', type=QgsProcessingParameterField.Any, parentLayerParameterName='zone', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Result', 'Result', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}

        # Intersection
        alg_params = {
            'INPUT': parameters['class'],
            'INPUT_FIELDS': parameters['classfield'],
            'OVERLAY': parameters['zone'],
            'OVERLAY_FIELDS': parameters['zonefield'],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Intersection'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Add geometry attributes
        alg_params = {
            'CALC_METHOD': 0,
            'INPUT': outputs['Intersection']['OUTPUT'],
            'OUTPUT': parameters['Result']
        }
        outputs['AddGeometryAttributes'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Result'] = outputs['AddGeometryAttributes']['OUTPUT']
        return results

    def name(self):
        return 'tblt1'

    def displayName(self):
        return 'tblt1'

    def createInstance(self):
        return Tblt1()
