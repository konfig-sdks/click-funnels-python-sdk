from click_funnels_python_sdk.paths.shipping_profiles_id.get import ApiForget
from click_funnels_python_sdk.paths.shipping_profiles_id.put import ApiForput
from click_funnels_python_sdk.paths.shipping_profiles_id.delete import ApiFordelete


class ShippingProfilesId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
