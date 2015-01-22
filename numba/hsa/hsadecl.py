from __future__ import print_function, division, absolute_import
from numba import types
from numba.typing.templates import (AttributeTemplate, ConcreteTemplate,
                                    MacroTemplate, signature, Registry)
from numba import hsa


registry = Registry()
intrinsic = registry.register
intrinsic_attr = registry.register_attr
intrinsic_global = registry.register_global

# =============================== NOTE ===============================
# Even though the following functions return size_t in the OpenCL standard,
# It should be rare (and unrealistic) to have 2**63 number of work items.
# We are choosing to use intp (signed 64-bit in large model) due to potential
# loss of precision in coerce(intp, uintp) that results in double.


@intrinsic
class Hsa_get_global_id(ConcreteTemplate):
    key = hsa.get_global_id
    cases = [signature(types.intp, types.uint32)]


@intrinsic
class Hsa_get_local_id(ConcreteTemplate):
    key = hsa.get_local_id
    cases = [signature(types.intp, types.uint32)]


@intrinsic
class Hsa_get_global_size(ConcreteTemplate):
    key = hsa.get_global_size
    cases = [signature(types.intp, types.uint32)]


@intrinsic
class Hsa_get_local_size(ConcreteTemplate):
    key = hsa.get_local_size
    cases = [signature(types.intp, types.uint32)]


@intrinsic
class Hsa_barrier(ConcreteTemplate):
    key = hsa.barrier
    cases = [signature(types.void, types.uint32)]


class Hsa_shared_array(MacroTemplate):
    key = hsa.shared.array


@intrinsic_attr
class HsaSharedModuleTemplate(AttributeTemplate):
    key = types.Module(hsa.shared)

    def resolve_array(self, mod):
        return types.Macro(Hsa_shared_array)


@intrinsic_attr
class HsaModuleTemplate(AttributeTemplate):
    key = types.Module(hsa)

    def resolve_get_global_id(self, mod):
        return types.Function(Hsa_get_global_id)

    def resolve_get_local_id(self, mod):
        return types.Function(Hsa_get_local_id)

    def resolve_get_global_size(self, mod):
        return types.Function(Hsa_get_global_size)

    def resolve_get_local_size(self, mod):
        return types.Function(Hsa_get_local_size)

    def resolve_barrier(self, mod):
        return types.Function(Hsa_barrier)

    def resolve_shared(self, mod):
        return types.Module(hsa.shared)


intrinsic_global(hsa, types.Module(hsa))