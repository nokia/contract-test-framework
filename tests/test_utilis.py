import os
import sys

from grpc import services

from fellowship.utilis import get_service_descriptor_name


def test_get_service_descriptor_name(protobuf_path):
    path_for_proto_import = os.path.dirname(os.path.abspath(protobuf_path))
    sys.path.append(path_for_proto_import)
    grpc_services = services(os.path.basename(protobuf_path))
    assert get_service_descriptor_name(grpc_services) == "test__pb2"
