import typing_extensions

from click_funnels_python_sdk.apis.tags import TagValues
from click_funnels_python_sdk.apis.tags.contact_api import ContactApi
from click_funnels_python_sdk.apis.tags.product_api import ProductApi
from click_funnels_python_sdk.apis.tags.contacts_tag_api import ContactsTagApi
from click_funnels_python_sdk.apis.tags.form_api import FormApi
from click_funnels_python_sdk.apis.tags.forms_field_set_api import FormsFieldSetApi
from click_funnels_python_sdk.apis.tags.forms_field_api import FormsFieldApi
from click_funnels_python_sdk.apis.tags.forms_fields_option_api import FormsFieldsOptionApi
from click_funnels_python_sdk.apis.tags.forms_submission_api import FormsSubmissionApi
from click_funnels_python_sdk.apis.tags.forms_submissions_answer_api import FormsSubmissionsAnswerApi
from click_funnels_python_sdk.apis.tags.image_api import ImageApi
from click_funnels_python_sdk.apis.tags.fulfillment_api import FulfillmentApi
from click_funnels_python_sdk.apis.tags.fulfillments_location_api import FulfillmentsLocationApi
from click_funnels_python_sdk.apis.tags.orders_tag_api import OrdersTagApi
from click_funnels_python_sdk.apis.tags.products_tag_api import ProductsTagApi
from click_funnels_python_sdk.apis.tags.shipping_package_api import ShippingPackageApi
from click_funnels_python_sdk.apis.tags.shipping_profile_api import ShippingProfileApi
from click_funnels_python_sdk.apis.tags.shipping_rate_api import ShippingRateApi
from click_funnels_python_sdk.apis.tags.shipping_zone_api import ShippingZoneApi
from click_funnels_python_sdk.apis.tags.shipping_rates_name_api import ShippingRatesNameApi
from click_funnels_python_sdk.apis.tags.workspace_api import WorkspaceApi
from click_funnels_python_sdk.apis.tags.contacts_applied_tag_api import ContactsAppliedTagApi
from click_funnels_python_sdk.apis.tags.courses_enrollment_api import CoursesEnrollmentApi
from click_funnels_python_sdk.apis.tags.orders_applied_tag_api import OrdersAppliedTagApi
from click_funnels_python_sdk.apis.tags.products_price_api import ProductsPriceApi
from click_funnels_python_sdk.apis.tags.products_variant_api import ProductsVariantApi
from click_funnels_python_sdk.apis.tags.webhooks_outgoing_endpoint_api import WebhooksOutgoingEndpointApi
from click_funnels_python_sdk.apis.tags.team_api import TeamApi
from click_funnels_python_sdk.apis.tags.user_api import UserApi
from click_funnels_python_sdk.apis.tags.courses_section_api import CoursesSectionApi
from click_funnels_python_sdk.apis.tags.courses_lesson_api import CoursesLessonApi
from click_funnels_python_sdk.apis.tags.order_api import OrderApi
from click_funnels_python_sdk.apis.tags.course_api import CourseApi
from click_funnels_python_sdk.apis.tags.orders_invoice_api import OrdersInvoiceApi
from click_funnels_python_sdk.apis.tags.orders_invoices_restock_api import OrdersInvoicesRestockApi
from click_funnels_python_sdk.apis.tags.orders_transaction_api import OrdersTransactionApi
from click_funnels_python_sdk.apis.tags.shipping_location_group_api import ShippingLocationGroupApi
from click_funnels_python_sdk.apis.tags.webhooks_outgoing_event_api import WebhooksOutgoingEventApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.CONTACT: ContactApi,
        TagValues.PRODUCT: ProductApi,
        TagValues.CONTACTSTAG: ContactsTagApi,
        TagValues.FORM: FormApi,
        TagValues.FORMSFIELD_SET: FormsFieldSetApi,
        TagValues.FORMSFIELD: FormsFieldApi,
        TagValues.FORMSFIELDSOPTION: FormsFieldsOptionApi,
        TagValues.FORMSSUBMISSION: FormsSubmissionApi,
        TagValues.FORMSSUBMISSIONSANSWER: FormsSubmissionsAnswerApi,
        TagValues.IMAGE: ImageApi,
        TagValues.FULFILLMENT: FulfillmentApi,
        TagValues.FULFILLMENTSLOCATION: FulfillmentsLocationApi,
        TagValues.ORDERSTAG: OrdersTagApi,
        TagValues.PRODUCTSTAG: ProductsTagApi,
        TagValues.SHIPPINGPACKAGE: ShippingPackageApi,
        TagValues.SHIPPINGPROFILE: ShippingProfileApi,
        TagValues.SHIPPINGRATE: ShippingRateApi,
        TagValues.SHIPPINGZONE: ShippingZoneApi,
        TagValues.SHIPPINGRATESNAME: ShippingRatesNameApi,
        TagValues.WORKSPACE: WorkspaceApi,
        TagValues.CONTACTSAPPLIED_TAG: ContactsAppliedTagApi,
        TagValues.COURSESENROLLMENT: CoursesEnrollmentApi,
        TagValues.ORDERSAPPLIED_TAG: OrdersAppliedTagApi,
        TagValues.PRODUCTSPRICE: ProductsPriceApi,
        TagValues.PRODUCTSVARIANT: ProductsVariantApi,
        TagValues.WEBHOOKSOUTGOINGENDPOINT: WebhooksOutgoingEndpointApi,
        TagValues.TEAM: TeamApi,
        TagValues.USER: UserApi,
        TagValues.COURSESSECTION: CoursesSectionApi,
        TagValues.COURSESLESSON: CoursesLessonApi,
        TagValues.ORDER: OrderApi,
        TagValues.COURSE: CourseApi,
        TagValues.ORDERSINVOICE: OrdersInvoiceApi,
        TagValues.ORDERSINVOICESRESTOCK: OrdersInvoicesRestockApi,
        TagValues.ORDERSTRANSACTION: OrdersTransactionApi,
        TagValues.SHIPPINGLOCATION_GROUP: ShippingLocationGroupApi,
        TagValues.WEBHOOKSOUTGOINGEVENT: WebhooksOutgoingEventApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.CONTACT: ContactApi,
        TagValues.PRODUCT: ProductApi,
        TagValues.CONTACTSTAG: ContactsTagApi,
        TagValues.FORM: FormApi,
        TagValues.FORMSFIELD_SET: FormsFieldSetApi,
        TagValues.FORMSFIELD: FormsFieldApi,
        TagValues.FORMSFIELDSOPTION: FormsFieldsOptionApi,
        TagValues.FORMSSUBMISSION: FormsSubmissionApi,
        TagValues.FORMSSUBMISSIONSANSWER: FormsSubmissionsAnswerApi,
        TagValues.IMAGE: ImageApi,
        TagValues.FULFILLMENT: FulfillmentApi,
        TagValues.FULFILLMENTSLOCATION: FulfillmentsLocationApi,
        TagValues.ORDERSTAG: OrdersTagApi,
        TagValues.PRODUCTSTAG: ProductsTagApi,
        TagValues.SHIPPINGPACKAGE: ShippingPackageApi,
        TagValues.SHIPPINGPROFILE: ShippingProfileApi,
        TagValues.SHIPPINGRATE: ShippingRateApi,
        TagValues.SHIPPINGZONE: ShippingZoneApi,
        TagValues.SHIPPINGRATESNAME: ShippingRatesNameApi,
        TagValues.WORKSPACE: WorkspaceApi,
        TagValues.CONTACTSAPPLIED_TAG: ContactsAppliedTagApi,
        TagValues.COURSESENROLLMENT: CoursesEnrollmentApi,
        TagValues.ORDERSAPPLIED_TAG: OrdersAppliedTagApi,
        TagValues.PRODUCTSPRICE: ProductsPriceApi,
        TagValues.PRODUCTSVARIANT: ProductsVariantApi,
        TagValues.WEBHOOKSOUTGOINGENDPOINT: WebhooksOutgoingEndpointApi,
        TagValues.TEAM: TeamApi,
        TagValues.USER: UserApi,
        TagValues.COURSESSECTION: CoursesSectionApi,
        TagValues.COURSESLESSON: CoursesLessonApi,
        TagValues.ORDER: OrderApi,
        TagValues.COURSE: CourseApi,
        TagValues.ORDERSINVOICE: OrdersInvoiceApi,
        TagValues.ORDERSINVOICESRESTOCK: OrdersInvoicesRestockApi,
        TagValues.ORDERSTRANSACTION: OrdersTransactionApi,
        TagValues.SHIPPINGLOCATION_GROUP: ShippingLocationGroupApi,
        TagValues.WEBHOOKSOUTGOINGEVENT: WebhooksOutgoingEventApi,
    }
)
