#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Landing script for Python 2.7 calls to FreeCAD."""


import os
import sys
import pickle

import qmt.geometry.freecad as cad

def main():
    """Fetch input data and dispatch instructions.

    WARNING: you must use send_back() to return data to the parent process.
    """

    instruction = sys.argv[1]
    data = pickle.loads(''.join(sys.stdin.readlines()))

    if instruction == 'build3d':
        activate_doc_from(data['current_options'])
        new_opts = cad.objectConstruction.build3d(data['current_options'])
        send_back(new_opts)

    elif instruction == 'writeFCfile':
        pass

    elif instruction == 'regionMap':
        from qms.fem.python2.make_region_marker_wrapper import makeRegionMarkerFunctionInsideWrapper

        names_to_ids, region_marker_filename = makeRegionMarkerFunctionInsideWrapper(data["mesh_filename"], data["geo_data"])
        send_back((names_to_ids, region_marker_filename))

    else:
        raise ValueError('Not a registered FreeCAD QMT instruction')


def activate_doc_from(opts):
    """Activate a valid FreeCAD document given a QMT Geometry3D opts dict.

    Returns a FCStd doc loaded from the file_path or serialised document.
    """
    doc = cad.FreeCAD.newDocument('instance')
    cad.FreeCAD.setActiveDocument('instance')

    if 'file_path' in opts:
        doc.load(opts['file_path'])
    elif 'serial_fcdoc' in opts:
        stored_doc = pickle.loads(opts['serial_fcdoc'])
        for obj in stored_doc.Objects:
            doc.copyObject(obj, False)  # don't deep copy dependencies
    else:
        raise ValueError("No FreeCAD document available")

    return doc


def send_back(data):
    """Go away."""
    sys.stdout.write('MAGICTQMTRANSFERBYTES'+pickle.dumps(data))


if __name__ == '__main__':
    main()
