from click_funnels_python_sdk.paths.forms_fields_id.get import ApiForget
from click_funnels_python_sdk.paths.forms_fields_id.put import ApiForput
from click_funnels_python_sdk.paths.forms_fields_id.delete import ApiFordelete


class FormsFieldsId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
