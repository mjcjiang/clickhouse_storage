# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import DataPlatForm.service_pb2 as service__pb2


class DACStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AddUser = channel.unary_unary(
                '/jgproto.DAC/AddUser',
                request_serializer=service__pb2.UserRequest.SerializeToString,
                response_deserializer=service__pb2.CommonResult.FromString,
                )
        self.ModifyUser = channel.unary_unary(
                '/jgproto.DAC/ModifyUser',
                request_serializer=service__pb2.UserRequest.SerializeToString,
                response_deserializer=service__pb2.CommonResult.FromString,
                )
        self.DeleteUser = channel.unary_unary(
                '/jgproto.DAC/DeleteUser',
                request_serializer=service__pb2.CommonStringRequest.SerializeToString,
                response_deserializer=service__pb2.CommonResult.FromString,
                )
        self.ListUser = channel.unary_unary(
                '/jgproto.DAC/ListUser',
                request_serializer=service__pb2.LoginInfo.SerializeToString,
                response_deserializer=service__pb2.UserInfos.FromString,
                )
        self.CreateAlphaFactor = channel.unary_unary(
                '/jgproto.DAC/CreateAlphaFactor',
                request_serializer=service__pb2.FactorRequest.SerializeToString,
                response_deserializer=service__pb2.FcAclResult.FromString,
                )
        self.ModifyAlphaFactor = channel.unary_unary(
                '/jgproto.DAC/ModifyAlphaFactor',
                request_serializer=service__pb2.FactorRequest.SerializeToString,
                response_deserializer=service__pb2.CommonResult.FromString,
                )
        self.DeleteAlphaFactor = channel.unary_unary(
                '/jgproto.DAC/DeleteAlphaFactor',
                request_serializer=service__pb2.FactorRequest.SerializeToString,
                response_deserializer=service__pb2.FcAclResult.FromString,
                )
        self.ListAlphaFactor = channel.unary_unary(
                '/jgproto.DAC/ListAlphaFactor',
                request_serializer=service__pb2.LoginInfo.SerializeToString,
                response_deserializer=service__pb2.FactorList.FromString,
                )
        self.GetAlphaFactor = channel.unary_unary(
                '/jgproto.DAC/GetAlphaFactor',
                request_serializer=service__pb2.FactorRequest.SerializeToString,
                response_deserializer=service__pb2.FactorResult.FromString,
                )
        self.CreateFcGroup = channel.unary_unary(
                '/jgproto.DAC/CreateFcGroup',
                request_serializer=service__pb2.GroupRequest.SerializeToString,
                response_deserializer=service__pb2.CommonResult.FromString,
                )
        self.ModifyFcGroup = channel.unary_unary(
                '/jgproto.DAC/ModifyFcGroup',
                request_serializer=service__pb2.GroupRequest.SerializeToString,
                response_deserializer=service__pb2.CommonResult.FromString,
                )
        self.ModifyFcGroupContent = channel.unary_unary(
                '/jgproto.DAC/ModifyFcGroupContent',
                request_serializer=service__pb2.GroupFcsRequest.SerializeToString,
                response_deserializer=service__pb2.CommonResult.FromString,
                )
        self.DeleteFcGroup = channel.unary_unary(
                '/jgproto.DAC/DeleteFcGroup',
                request_serializer=service__pb2.CommonStringRequest.SerializeToString,
                response_deserializer=service__pb2.CommonResult.FromString,
                )
        self.ListFcGroup = channel.unary_unary(
                '/jgproto.DAC/ListFcGroup',
                request_serializer=service__pb2.LoginInfo.SerializeToString,
                response_deserializer=service__pb2.FcGroups.FromString,
                )
        self.CheckFcAcl = channel.unary_unary(
                '/jgproto.DAC/CheckFcAcl',
                request_serializer=service__pb2.FcAclRequest.SerializeToString,
                response_deserializer=service__pb2.FcAclResult.FromString,
                )
        self.CreateNewData = channel.unary_unary(
                '/jgproto.DAC/CreateNewData',
                request_serializer=service__pb2.DataRequest.SerializeToString,
                response_deserializer=service__pb2.AclResult.FromString,
                )
        self.DeleteData = channel.unary_unary(
                '/jgproto.DAC/DeleteData',
                request_serializer=service__pb2.DataRequest.SerializeToString,
                response_deserializer=service__pb2.AclResult.FromString,
                )
        self.CheckAcl = channel.unary_unary(
                '/jgproto.DAC/CheckAcl',
                request_serializer=service__pb2.AclRequest.SerializeToString,
                response_deserializer=service__pb2.AclResult.FromString,
                )


class DACServicer(object):
    """Missing associated documentation comment in .proto file."""

    def AddUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ModifyUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateAlphaFactor(self, request, context):
        """创建高级因子
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ModifyAlphaFactor(self, request, context):
        """改level、改信息等
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteAlphaFactor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListAlphaFactor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAlphaFactor(self, request, context):
        """获取高级因子信息
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateFcGroup(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ModifyFcGroup(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ModifyFcGroupContent(self, request, context):
        """增删改
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteFcGroup(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListFcGroup(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CheckFcAcl(self, request, context):
        """rpc SetFcAcl (FcAclRequest) returns (CommonResult); // 授权/回收 组、单个因子
        检查是否具有操作因子的权限
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateNewData(self, request, context):
        """创建新的其他数据类型
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CheckAcl(self, request, context):
        """检查是否具有操作数据的权限
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DACServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AddUser': grpc.unary_unary_rpc_method_handler(
                    servicer.AddUser,
                    request_deserializer=service__pb2.UserRequest.FromString,
                    response_serializer=service__pb2.CommonResult.SerializeToString,
            ),
            'ModifyUser': grpc.unary_unary_rpc_method_handler(
                    servicer.ModifyUser,
                    request_deserializer=service__pb2.UserRequest.FromString,
                    response_serializer=service__pb2.CommonResult.SerializeToString,
            ),
            'DeleteUser': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteUser,
                    request_deserializer=service__pb2.CommonStringRequest.FromString,
                    response_serializer=service__pb2.CommonResult.SerializeToString,
            ),
            'ListUser': grpc.unary_unary_rpc_method_handler(
                    servicer.ListUser,
                    request_deserializer=service__pb2.LoginInfo.FromString,
                    response_serializer=service__pb2.UserInfos.SerializeToString,
            ),
            'CreateAlphaFactor': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateAlphaFactor,
                    request_deserializer=service__pb2.FactorRequest.FromString,
                    response_serializer=service__pb2.FcAclResult.SerializeToString,
            ),
            'ModifyAlphaFactor': grpc.unary_unary_rpc_method_handler(
                    servicer.ModifyAlphaFactor,
                    request_deserializer=service__pb2.FactorRequest.FromString,
                    response_serializer=service__pb2.CommonResult.SerializeToString,
            ),
            'DeleteAlphaFactor': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteAlphaFactor,
                    request_deserializer=service__pb2.FactorRequest.FromString,
                    response_serializer=service__pb2.FcAclResult.SerializeToString,
            ),
            'ListAlphaFactor': grpc.unary_unary_rpc_method_handler(
                    servicer.ListAlphaFactor,
                    request_deserializer=service__pb2.LoginInfo.FromString,
                    response_serializer=service__pb2.FactorList.SerializeToString,
            ),
            'GetAlphaFactor': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAlphaFactor,
                    request_deserializer=service__pb2.FactorRequest.FromString,
                    response_serializer=service__pb2.FactorResult.SerializeToString,
            ),
            'CreateFcGroup': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateFcGroup,
                    request_deserializer=service__pb2.GroupRequest.FromString,
                    response_serializer=service__pb2.CommonResult.SerializeToString,
            ),
            'ModifyFcGroup': grpc.unary_unary_rpc_method_handler(
                    servicer.ModifyFcGroup,
                    request_deserializer=service__pb2.GroupRequest.FromString,
                    response_serializer=service__pb2.CommonResult.SerializeToString,
            ),
            'ModifyFcGroupContent': grpc.unary_unary_rpc_method_handler(
                    servicer.ModifyFcGroupContent,
                    request_deserializer=service__pb2.GroupFcsRequest.FromString,
                    response_serializer=service__pb2.CommonResult.SerializeToString,
            ),
            'DeleteFcGroup': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteFcGroup,
                    request_deserializer=service__pb2.CommonStringRequest.FromString,
                    response_serializer=service__pb2.CommonResult.SerializeToString,
            ),
            'ListFcGroup': grpc.unary_unary_rpc_method_handler(
                    servicer.ListFcGroup,
                    request_deserializer=service__pb2.LoginInfo.FromString,
                    response_serializer=service__pb2.FcGroups.SerializeToString,
            ),
            'CheckFcAcl': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckFcAcl,
                    request_deserializer=service__pb2.FcAclRequest.FromString,
                    response_serializer=service__pb2.FcAclResult.SerializeToString,
            ),
            'CreateNewData': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateNewData,
                    request_deserializer=service__pb2.DataRequest.FromString,
                    response_serializer=service__pb2.AclResult.SerializeToString,
            ),
            'DeleteData': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteData,
                    request_deserializer=service__pb2.DataRequest.FromString,
                    response_serializer=service__pb2.AclResult.SerializeToString,
            ),
            'CheckAcl': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckAcl,
                    request_deserializer=service__pb2.AclRequest.FromString,
                    response_serializer=service__pb2.AclResult.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'jgproto.DAC', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DAC(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def AddUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jgproto.DAC/AddUser',
            service__pb2.UserRequest.SerializeToString,
            service__pb2.CommonResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ModifyUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jgproto.DAC/ModifyUser',
            service__pb2.UserRequest.SerializeToString,
            service__pb2.CommonResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jgproto.DAC/DeleteUser',
            service__pb2.CommonStringRequest.SerializeToString,
            service__pb2.CommonResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jgproto.DAC/ListUser',
            service__pb2.LoginInfo.SerializeToString,
            service__pb2.UserInfos.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateAlphaFactor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jgproto.DAC/CreateAlphaFactor',
            service__pb2.FactorRequest.SerializeToString,
            service__pb2.FcAclResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ModifyAlphaFactor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jgproto.DAC/ModifyAlphaFactor',
            service__pb2.FactorRequest.SerializeToString,
            service__pb2.CommonResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteAlphaFactor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jgproto.DAC/DeleteAlphaFactor',
            service__pb2.FactorRequest.SerializeToString,
            service__pb2.FcAclResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListAlphaFactor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jgproto.DAC/ListAlphaFactor',
            service__pb2.LoginInfo.SerializeToString,
            service__pb2.FactorList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAlphaFactor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jgproto.DAC/GetAlphaFactor',
            service__pb2.FactorRequest.SerializeToString,
            service__pb2.FactorResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateFcGroup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jgproto.DAC/CreateFcGroup',
            service__pb2.GroupRequest.SerializeToString,
            service__pb2.CommonResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ModifyFcGroup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jgproto.DAC/ModifyFcGroup',
            service__pb2.GroupRequest.SerializeToString,
            service__pb2.CommonResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ModifyFcGroupContent(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jgproto.DAC/ModifyFcGroupContent',
            service__pb2.GroupFcsRequest.SerializeToString,
            service__pb2.CommonResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteFcGroup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jgproto.DAC/DeleteFcGroup',
            service__pb2.CommonStringRequest.SerializeToString,
            service__pb2.CommonResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListFcGroup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jgproto.DAC/ListFcGroup',
            service__pb2.LoginInfo.SerializeToString,
            service__pb2.FcGroups.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CheckFcAcl(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jgproto.DAC/CheckFcAcl',
            service__pb2.FcAclRequest.SerializeToString,
            service__pb2.FcAclResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateNewData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jgproto.DAC/CreateNewData',
            service__pb2.DataRequest.SerializeToString,
            service__pb2.AclResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jgproto.DAC/DeleteData',
            service__pb2.DataRequest.SerializeToString,
            service__pb2.AclResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CheckAcl(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jgproto.DAC/CheckAcl',
            service__pb2.AclRequest.SerializeToString,
            service__pb2.AclResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
