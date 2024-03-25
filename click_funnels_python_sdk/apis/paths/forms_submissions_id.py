from click_funnels_python_sdk.paths.forms_submissions_id.get import ApiForget
from click_funnels_python_sdk.paths.forms_submissions_id.put import ApiForput
from click_funnels_python_sdk.paths.forms_submissions_id.delete import ApiFordelete


class FormsSubmissionsId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
