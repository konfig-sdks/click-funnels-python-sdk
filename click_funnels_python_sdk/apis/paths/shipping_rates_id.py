from click_funnels_python_sdk.paths.shipping_rates_id.get import ApiForget
from click_funnels_python_sdk.paths.shipping_rates_id.put import ApiForput
from click_funnels_python_sdk.paths.shipping_rates_id.delete import ApiFordelete


class ShippingRatesId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
