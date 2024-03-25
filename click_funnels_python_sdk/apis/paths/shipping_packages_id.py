from click_funnels_python_sdk.paths.shipping_packages_id.get import ApiForget
from click_funnels_python_sdk.paths.shipping_packages_id.put import ApiForput
from click_funnels_python_sdk.paths.shipping_packages_id.delete import ApiFordelete


class ShippingPackagesId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
