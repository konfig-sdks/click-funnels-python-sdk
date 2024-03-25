from click_funnels_python_sdk.paths.orders_tags_id.get import ApiForget
from click_funnels_python_sdk.paths.orders_tags_id.put import ApiForput
from click_funnels_python_sdk.paths.orders_tags_id.delete import ApiFordelete


class OrdersTagsId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
