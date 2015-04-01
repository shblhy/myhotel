from ..djex.admin import BaseListManager as OriBaseListManager
from .table_amu import OurTable


class BaseListManager(OriBaseListManager):
    paginator_by = 30
    table_class = OurTable
