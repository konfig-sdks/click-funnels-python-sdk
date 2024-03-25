from click_funnels_python_sdk.paths.contacts_id.get import ApiForget
from click_funnels_python_sdk.paths.contacts_id.put import ApiForput
from click_funnels_python_sdk.paths.contacts_id.delete import ApiFordelete


class ContactsId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
