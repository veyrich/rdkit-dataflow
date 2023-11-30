import sys
import argparse
import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from rdkit import Chem
from rdkit.Chem import Descriptors

def calc_mw(smi):
    mw = None
    try:
        m = Chem.MolFromSmiles(smi)
        mw = Descriptors.ExactMolWt(m)
    #ToDo: handle different exceptions more selectively
    except Exceptions as e:
        logging.error("caught exception {}".format(e))
    
    #ToDo: use csv module for escaping etc
    yield "{},{}".format(smi,mw)
    
def run(argv=None, save_main_session=True):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input',
        required=True,
        help='Input file to process.')

    parser.add_argument(
        '--output',
        dest='output',
        required=True,
        help='Output file to write results to.')

    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = save_main_session

    with beam.Pipeline(options=pipeline_options) as pipeline:
        lines = (
            pipeline
            | beam.io.ReadFromText(known_args.input)
            | beam.ParDo(calc_mw)
        )
        lines | 'Write' >> beam.io.WriteToText(known_args.output)

    logging.info("done processing")
        
if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()
