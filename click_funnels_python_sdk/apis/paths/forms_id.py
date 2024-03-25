from click_funnels_python_sdk.paths.forms_id.get import ApiForget
from click_funnels_python_sdk.paths.forms_id.put import ApiForput
from click_funnels_python_sdk.paths.forms_id.delete import ApiFordelete


class FormsId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
