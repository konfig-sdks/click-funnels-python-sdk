from click_funnels_python_sdk.paths.forms_field_sets_id.get import ApiForget
from click_funnels_python_sdk.paths.forms_field_sets_id.put import ApiForput
from click_funnels_python_sdk.paths.forms_field_sets_id.delete import ApiFordelete


class FormsFieldSetsId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
