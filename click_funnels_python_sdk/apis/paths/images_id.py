from click_funnels_python_sdk.paths.images_id.get import ApiForget
from click_funnels_python_sdk.paths.images_id.put import ApiForput
from click_funnels_python_sdk.paths.images_id.delete import ApiFordelete


class ImagesId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
