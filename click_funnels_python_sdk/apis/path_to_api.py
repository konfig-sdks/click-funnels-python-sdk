import typing_extensions

from click_funnels_python_sdk.paths import PathValues
from click_funnels_python_sdk.apis.paths.teams import Teams
from click_funnels_python_sdk.apis.paths.teams_id import TeamsId
from click_funnels_python_sdk.apis.paths.users import Users
from click_funnels_python_sdk.apis.paths.users_id import UsersId
from click_funnels_python_sdk.apis.paths.teams_team_id_workspaces import TeamsTeamIdWorkspaces
from click_funnels_python_sdk.apis.paths.workspaces_id import WorkspacesId
from click_funnels_python_sdk.apis.paths.workspaces_workspace_id_contacts import WorkspacesWorkspaceIdContacts
from click_funnels_python_sdk.apis.paths.contacts_id import ContactsId
from click_funnels_python_sdk.apis.paths.contacts_id_gdpr_destroy import ContactsIdGdprDestroy
from click_funnels_python_sdk.apis.paths.workspaces_workspace_id_contacts_upsert import WorkspacesWorkspaceIdContactsUpsert
from click_funnels_python_sdk.apis.paths.contacts_contact_id_applied_tags import ContactsContactIdAppliedTags
from click_funnels_python_sdk.apis.paths.contacts_applied_tags_id import ContactsAppliedTagsId
from click_funnels_python_sdk.apis.paths.workspaces_workspace_id_contacts_tags import WorkspacesWorkspaceIdContactsTags
from click_funnels_python_sdk.apis.paths.contacts_tags_id import ContactsTagsId
from click_funnels_python_sdk.apis.paths.workspaces_workspace_id_courses import WorkspacesWorkspaceIdCourses
from click_funnels_python_sdk.apis.paths.courses_id import CoursesId
from click_funnels_python_sdk.apis.paths.courses_course_id_enrollments import CoursesCourseIdEnrollments
from click_funnels_python_sdk.apis.paths.courses_enrollments_id import CoursesEnrollmentsId
from click_funnels_python_sdk.apis.paths.courses_course_id_sections import CoursesCourseIdSections
from click_funnels_python_sdk.apis.paths.courses_sections_id import CoursesSectionsId
from click_funnels_python_sdk.apis.paths.courses_sections_section_id_lessons import CoursesSectionsSectionIdLessons
from click_funnels_python_sdk.apis.paths.courses_lessons_id import CoursesLessonsId
from click_funnels_python_sdk.apis.paths.workspaces_workspace_id_forms import WorkspacesWorkspaceIdForms
from click_funnels_python_sdk.apis.paths.forms_id import FormsId
from click_funnels_python_sdk.apis.paths.forms_form_id_field_sets import FormsFormIdFieldSets
from click_funnels_python_sdk.apis.paths.forms_field_sets_id import FormsFieldSetsId
from click_funnels_python_sdk.apis.paths.forms_field_sets_field_set_id_fields import FormsFieldSetsFieldSetIdFields
from click_funnels_python_sdk.apis.paths.forms_fields_id import FormsFieldsId
from click_funnels_python_sdk.apis.paths.forms_fields_field_id_options import FormsFieldsFieldIdOptions
from click_funnels_python_sdk.apis.paths.forms_fields_options_id import FormsFieldsOptionsId
from click_funnels_python_sdk.apis.paths.forms_form_id_submissions import FormsFormIdSubmissions
from click_funnels_python_sdk.apis.paths.forms_submissions_id import FormsSubmissionsId
from click_funnels_python_sdk.apis.paths.forms_submissions_submission_id_answers import FormsSubmissionsSubmissionIdAnswers
from click_funnels_python_sdk.apis.paths.forms_submissions_answers_id import FormsSubmissionsAnswersId
from click_funnels_python_sdk.apis.paths.workspaces_workspace_id_fulfillments import WorkspacesWorkspaceIdFulfillments
from click_funnels_python_sdk.apis.paths.fulfillments_id import FulfillmentsId
from click_funnels_python_sdk.apis.paths.fulfillments_id_cancel import FulfillmentsIdCancel
from click_funnels_python_sdk.apis.paths.workspaces_workspace_id_fulfillments_locations import WorkspacesWorkspaceIdFulfillmentsLocations
from click_funnels_python_sdk.apis.paths.fulfillments_locations_id import FulfillmentsLocationsId
from click_funnels_python_sdk.apis.paths.workspaces_workspace_id_images import WorkspacesWorkspaceIdImages
from click_funnels_python_sdk.apis.paths.images_id import ImagesId
from click_funnels_python_sdk.apis.paths.workspaces_workspace_id_orders import WorkspacesWorkspaceIdOrders
from click_funnels_python_sdk.apis.paths.orders_id import OrdersId
from click_funnels_python_sdk.apis.paths.workspaces_workspace_id_orders_invoices_restocks import WorkspacesWorkspaceIdOrdersInvoicesRestocks
from click_funnels_python_sdk.apis.paths.orders_invoices_restocks_id import OrdersInvoicesRestocksId
from click_funnels_python_sdk.apis.paths.orders_order_id_applied_tags import OrdersOrderIdAppliedTags
from click_funnels_python_sdk.apis.paths.orders_applied_tags_id import OrdersAppliedTagsId
from click_funnels_python_sdk.apis.paths.orders_order_id_invoices import OrdersOrderIdInvoices
from click_funnels_python_sdk.apis.paths.orders_invoices_id import OrdersInvoicesId
from click_funnels_python_sdk.apis.paths.orders_order_id_transactions import OrdersOrderIdTransactions
from click_funnels_python_sdk.apis.paths.orders_transactions_id import OrdersTransactionsId
from click_funnels_python_sdk.apis.paths.workspaces_workspace_id_orders_tags import WorkspacesWorkspaceIdOrdersTags
from click_funnels_python_sdk.apis.paths.orders_tags_id import OrdersTagsId
from click_funnels_python_sdk.apis.paths.workspaces_workspace_id_products import WorkspacesWorkspaceIdProducts
from click_funnels_python_sdk.apis.paths.products_id import ProductsId
from click_funnels_python_sdk.apis.paths.products_id_archive import ProductsIdArchive
from click_funnels_python_sdk.apis.paths.products_id_unarchive import ProductsIdUnarchive
from click_funnels_python_sdk.apis.paths.products_product_id_prices import ProductsProductIdPrices
from click_funnels_python_sdk.apis.paths.products_prices_id import ProductsPricesId
from click_funnels_python_sdk.apis.paths.products_product_id_variants import ProductsProductIdVariants
from click_funnels_python_sdk.apis.paths.products_variants_id import ProductsVariantsId
from click_funnels_python_sdk.apis.paths.workspaces_workspace_id_products_tags import WorkspacesWorkspaceIdProductsTags
from click_funnels_python_sdk.apis.paths.products_tags_id import ProductsTagsId
from click_funnels_python_sdk.apis.paths.shipping_profiles_profile_id_location_groups import ShippingProfilesProfileIdLocationGroups
from click_funnels_python_sdk.apis.paths.shipping_location_groups_id import ShippingLocationGroupsId
from click_funnels_python_sdk.apis.paths.workspaces_workspace_id_shipping_packages import WorkspacesWorkspaceIdShippingPackages
from click_funnels_python_sdk.apis.paths.shipping_packages_id import ShippingPackagesId
from click_funnels_python_sdk.apis.paths.workspaces_workspace_id_shipping_profiles import WorkspacesWorkspaceIdShippingProfiles
from click_funnels_python_sdk.apis.paths.shipping_profiles_id import ShippingProfilesId
from click_funnels_python_sdk.apis.paths.shipping_zones_zone_id_rates import ShippingZonesZoneIdRates
from click_funnels_python_sdk.apis.paths.shipping_rates_id import ShippingRatesId
from click_funnels_python_sdk.apis.paths.shipping_location_groups_location_group_id_zones import ShippingLocationGroupsLocationGroupIdZones
from click_funnels_python_sdk.apis.paths.shipping_zones_id import ShippingZonesId
from click_funnels_python_sdk.apis.paths.workspaces_workspace_id_shipping_rates_names import WorkspacesWorkspaceIdShippingRatesNames
from click_funnels_python_sdk.apis.paths.shipping_rates_names_id import ShippingRatesNamesId
from click_funnels_python_sdk.apis.paths.workspaces_workspace_id_webhooks_outgoing_endpoints import WorkspacesWorkspaceIdWebhooksOutgoingEndpoints
from click_funnels_python_sdk.apis.paths.webhooks_outgoing_endpoints_id import WebhooksOutgoingEndpointsId
from click_funnels_python_sdk.apis.paths.workspaces_workspace_id_webhooks_outgoing_events import WorkspacesWorkspaceIdWebhooksOutgoingEvents
from click_funnels_python_sdk.apis.paths.webhooks_outgoing_events_id import WebhooksOutgoingEventsId

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.TEAMS: Teams,
        PathValues.TEAMS_ID: TeamsId,
        PathValues.USERS: Users,
        PathValues.USERS_ID: UsersId,
        PathValues.TEAMS_TEAM_ID_WORKSPACES: TeamsTeamIdWorkspaces,
        PathValues.WORKSPACES_ID: WorkspacesId,
        PathValues.WORKSPACES_WORKSPACE_ID_CONTACTS: WorkspacesWorkspaceIdContacts,
        PathValues.CONTACTS_ID: ContactsId,
        PathValues.CONTACTS_ID_GDPR_DESTROY: ContactsIdGdprDestroy,
        PathValues.WORKSPACES_WORKSPACE_ID_CONTACTS_UPSERT: WorkspacesWorkspaceIdContactsUpsert,
        PathValues.CONTACTS_CONTACT_ID_APPLIED_TAGS: ContactsContactIdAppliedTags,
        PathValues.CONTACTS_APPLIED_TAGS_ID: ContactsAppliedTagsId,
        PathValues.WORKSPACES_WORKSPACE_ID_CONTACTS_TAGS: WorkspacesWorkspaceIdContactsTags,
        PathValues.CONTACTS_TAGS_ID: ContactsTagsId,
        PathValues.WORKSPACES_WORKSPACE_ID_COURSES: WorkspacesWorkspaceIdCourses,
        PathValues.COURSES_ID: CoursesId,
        PathValues.COURSES_COURSE_ID_ENROLLMENTS: CoursesCourseIdEnrollments,
        PathValues.COURSES_ENROLLMENTS_ID: CoursesEnrollmentsId,
        PathValues.COURSES_COURSE_ID_SECTIONS: CoursesCourseIdSections,
        PathValues.COURSES_SECTIONS_ID: CoursesSectionsId,
        PathValues.COURSES_SECTIONS_SECTION_ID_LESSONS: CoursesSectionsSectionIdLessons,
        PathValues.COURSES_LESSONS_ID: CoursesLessonsId,
        PathValues.WORKSPACES_WORKSPACE_ID_FORMS: WorkspacesWorkspaceIdForms,
        PathValues.FORMS_ID: FormsId,
        PathValues.FORMS_FORM_ID_FIELD_SETS: FormsFormIdFieldSets,
        PathValues.FORMS_FIELD_SETS_ID: FormsFieldSetsId,
        PathValues.FORMS_FIELD_SETS_FIELD_SET_ID_FIELDS: FormsFieldSetsFieldSetIdFields,
        PathValues.FORMS_FIELDS_ID: FormsFieldsId,
        PathValues.FORMS_FIELDS_FIELD_ID_OPTIONS: FormsFieldsFieldIdOptions,
        PathValues.FORMS_FIELDS_OPTIONS_ID: FormsFieldsOptionsId,
        PathValues.FORMS_FORM_ID_SUBMISSIONS: FormsFormIdSubmissions,
        PathValues.FORMS_SUBMISSIONS_ID: FormsSubmissionsId,
        PathValues.FORMS_SUBMISSIONS_SUBMISSION_ID_ANSWERS: FormsSubmissionsSubmissionIdAnswers,
        PathValues.FORMS_SUBMISSIONS_ANSWERS_ID: FormsSubmissionsAnswersId,
        PathValues.WORKSPACES_WORKSPACE_ID_FULFILLMENTS: WorkspacesWorkspaceIdFulfillments,
        PathValues.FULFILLMENTS_ID: FulfillmentsId,
        PathValues.FULFILLMENTS_ID_CANCEL: FulfillmentsIdCancel,
        PathValues.WORKSPACES_WORKSPACE_ID_FULFILLMENTS_LOCATIONS: WorkspacesWorkspaceIdFulfillmentsLocations,
        PathValues.FULFILLMENTS_LOCATIONS_ID: FulfillmentsLocationsId,
        PathValues.WORKSPACES_WORKSPACE_ID_IMAGES: WorkspacesWorkspaceIdImages,
        PathValues.IMAGES_ID: ImagesId,
        PathValues.WORKSPACES_WORKSPACE_ID_ORDERS: WorkspacesWorkspaceIdOrders,
        PathValues.ORDERS_ID: OrdersId,
        PathValues.WORKSPACES_WORKSPACE_ID_ORDERS_INVOICES_RESTOCKS: WorkspacesWorkspaceIdOrdersInvoicesRestocks,
        PathValues.ORDERS_INVOICES_RESTOCKS_ID: OrdersInvoicesRestocksId,
        PathValues.ORDERS_ORDER_ID_APPLIED_TAGS: OrdersOrderIdAppliedTags,
        PathValues.ORDERS_APPLIED_TAGS_ID: OrdersAppliedTagsId,
        PathValues.ORDERS_ORDER_ID_INVOICES: OrdersOrderIdInvoices,
        PathValues.ORDERS_INVOICES_ID: OrdersInvoicesId,
        PathValues.ORDERS_ORDER_ID_TRANSACTIONS: OrdersOrderIdTransactions,
        PathValues.ORDERS_TRANSACTIONS_ID: OrdersTransactionsId,
        PathValues.WORKSPACES_WORKSPACE_ID_ORDERS_TAGS: WorkspacesWorkspaceIdOrdersTags,
        PathValues.ORDERS_TAGS_ID: OrdersTagsId,
        PathValues.WORKSPACES_WORKSPACE_ID_PRODUCTS: WorkspacesWorkspaceIdProducts,
        PathValues.PRODUCTS_ID: ProductsId,
        PathValues.PRODUCTS_ID_ARCHIVE: ProductsIdArchive,
        PathValues.PRODUCTS_ID_UNARCHIVE: ProductsIdUnarchive,
        PathValues.PRODUCTS_PRODUCT_ID_PRICES: ProductsProductIdPrices,
        PathValues.PRODUCTS_PRICES_ID: ProductsPricesId,
        PathValues.PRODUCTS_PRODUCT_ID_VARIANTS: ProductsProductIdVariants,
        PathValues.PRODUCTS_VARIANTS_ID: ProductsVariantsId,
        PathValues.WORKSPACES_WORKSPACE_ID_PRODUCTS_TAGS: WorkspacesWorkspaceIdProductsTags,
        PathValues.PRODUCTS_TAGS_ID: ProductsTagsId,
        PathValues.SHIPPING_PROFILES_PROFILE_ID_LOCATION_GROUPS: ShippingProfilesProfileIdLocationGroups,
        PathValues.SHIPPING_LOCATION_GROUPS_ID: ShippingLocationGroupsId,
        PathValues.WORKSPACES_WORKSPACE_ID_SHIPPING_PACKAGES: WorkspacesWorkspaceIdShippingPackages,
        PathValues.SHIPPING_PACKAGES_ID: ShippingPackagesId,
        PathValues.WORKSPACES_WORKSPACE_ID_SHIPPING_PROFILES: WorkspacesWorkspaceIdShippingProfiles,
        PathValues.SHIPPING_PROFILES_ID: ShippingProfilesId,
        PathValues.SHIPPING_ZONES_ZONE_ID_RATES: ShippingZonesZoneIdRates,
        PathValues.SHIPPING_RATES_ID: ShippingRatesId,
        PathValues.SHIPPING_LOCATION_GROUPS_LOCATION_GROUP_ID_ZONES: ShippingLocationGroupsLocationGroupIdZones,
        PathValues.SHIPPING_ZONES_ID: ShippingZonesId,
        PathValues.WORKSPACES_WORKSPACE_ID_SHIPPING_RATES_NAMES: WorkspacesWorkspaceIdShippingRatesNames,
        PathValues.SHIPPING_RATES_NAMES_ID: ShippingRatesNamesId,
        PathValues.WORKSPACES_WORKSPACE_ID_WEBHOOKS_OUTGOING_ENDPOINTS: WorkspacesWorkspaceIdWebhooksOutgoingEndpoints,
        PathValues.WEBHOOKS_OUTGOING_ENDPOINTS_ID: WebhooksOutgoingEndpointsId,
        PathValues.WORKSPACES_WORKSPACE_ID_WEBHOOKS_OUTGOING_EVENTS: WorkspacesWorkspaceIdWebhooksOutgoingEvents,
        PathValues.WEBHOOKS_OUTGOING_EVENTS_ID: WebhooksOutgoingEventsId,
    }
)

path_to_api = PathToApi(
    {
        PathValues.TEAMS: Teams,
        PathValues.TEAMS_ID: TeamsId,
        PathValues.USERS: Users,
        PathValues.USERS_ID: UsersId,
        PathValues.TEAMS_TEAM_ID_WORKSPACES: TeamsTeamIdWorkspaces,
        PathValues.WORKSPACES_ID: WorkspacesId,
        PathValues.WORKSPACES_WORKSPACE_ID_CONTACTS: WorkspacesWorkspaceIdContacts,
        PathValues.CONTACTS_ID: ContactsId,
        PathValues.CONTACTS_ID_GDPR_DESTROY: ContactsIdGdprDestroy,
        PathValues.WORKSPACES_WORKSPACE_ID_CONTACTS_UPSERT: WorkspacesWorkspaceIdContactsUpsert,
        PathValues.CONTACTS_CONTACT_ID_APPLIED_TAGS: ContactsContactIdAppliedTags,
        PathValues.CONTACTS_APPLIED_TAGS_ID: ContactsAppliedTagsId,
        PathValues.WORKSPACES_WORKSPACE_ID_CONTACTS_TAGS: WorkspacesWorkspaceIdContactsTags,
        PathValues.CONTACTS_TAGS_ID: ContactsTagsId,
        PathValues.WORKSPACES_WORKSPACE_ID_COURSES: WorkspacesWorkspaceIdCourses,
        PathValues.COURSES_ID: CoursesId,
        PathValues.COURSES_COURSE_ID_ENROLLMENTS: CoursesCourseIdEnrollments,
        PathValues.COURSES_ENROLLMENTS_ID: CoursesEnrollmentsId,
        PathValues.COURSES_COURSE_ID_SECTIONS: CoursesCourseIdSections,
        PathValues.COURSES_SECTIONS_ID: CoursesSectionsId,
        PathValues.COURSES_SECTIONS_SECTION_ID_LESSONS: CoursesSectionsSectionIdLessons,
        PathValues.COURSES_LESSONS_ID: CoursesLessonsId,
        PathValues.WORKSPACES_WORKSPACE_ID_FORMS: WorkspacesWorkspaceIdForms,
        PathValues.FORMS_ID: FormsId,
        PathValues.FORMS_FORM_ID_FIELD_SETS: FormsFormIdFieldSets,
        PathValues.FORMS_FIELD_SETS_ID: FormsFieldSetsId,
        PathValues.FORMS_FIELD_SETS_FIELD_SET_ID_FIELDS: FormsFieldSetsFieldSetIdFields,
        PathValues.FORMS_FIELDS_ID: FormsFieldsId,
        PathValues.FORMS_FIELDS_FIELD_ID_OPTIONS: FormsFieldsFieldIdOptions,
        PathValues.FORMS_FIELDS_OPTIONS_ID: FormsFieldsOptionsId,
        PathValues.FORMS_FORM_ID_SUBMISSIONS: FormsFormIdSubmissions,
        PathValues.FORMS_SUBMISSIONS_ID: FormsSubmissionsId,
        PathValues.FORMS_SUBMISSIONS_SUBMISSION_ID_ANSWERS: FormsSubmissionsSubmissionIdAnswers,
        PathValues.FORMS_SUBMISSIONS_ANSWERS_ID: FormsSubmissionsAnswersId,
        PathValues.WORKSPACES_WORKSPACE_ID_FULFILLMENTS: WorkspacesWorkspaceIdFulfillments,
        PathValues.FULFILLMENTS_ID: FulfillmentsId,
        PathValues.FULFILLMENTS_ID_CANCEL: FulfillmentsIdCancel,
        PathValues.WORKSPACES_WORKSPACE_ID_FULFILLMENTS_LOCATIONS: WorkspacesWorkspaceIdFulfillmentsLocations,
        PathValues.FULFILLMENTS_LOCATIONS_ID: FulfillmentsLocationsId,
        PathValues.WORKSPACES_WORKSPACE_ID_IMAGES: WorkspacesWorkspaceIdImages,
        PathValues.IMAGES_ID: ImagesId,
        PathValues.WORKSPACES_WORKSPACE_ID_ORDERS: WorkspacesWorkspaceIdOrders,
        PathValues.ORDERS_ID: OrdersId,
        PathValues.WORKSPACES_WORKSPACE_ID_ORDERS_INVOICES_RESTOCKS: WorkspacesWorkspaceIdOrdersInvoicesRestocks,
        PathValues.ORDERS_INVOICES_RESTOCKS_ID: OrdersInvoicesRestocksId,
        PathValues.ORDERS_ORDER_ID_APPLIED_TAGS: OrdersOrderIdAppliedTags,
        PathValues.ORDERS_APPLIED_TAGS_ID: OrdersAppliedTagsId,
        PathValues.ORDERS_ORDER_ID_INVOICES: OrdersOrderIdInvoices,
        PathValues.ORDERS_INVOICES_ID: OrdersInvoicesId,
        PathValues.ORDERS_ORDER_ID_TRANSACTIONS: OrdersOrderIdTransactions,
        PathValues.ORDERS_TRANSACTIONS_ID: OrdersTransactionsId,
        PathValues.WORKSPACES_WORKSPACE_ID_ORDERS_TAGS: WorkspacesWorkspaceIdOrdersTags,
        PathValues.ORDERS_TAGS_ID: OrdersTagsId,
        PathValues.WORKSPACES_WORKSPACE_ID_PRODUCTS: WorkspacesWorkspaceIdProducts,
        PathValues.PRODUCTS_ID: ProductsId,
        PathValues.PRODUCTS_ID_ARCHIVE: ProductsIdArchive,
        PathValues.PRODUCTS_ID_UNARCHIVE: ProductsIdUnarchive,
        PathValues.PRODUCTS_PRODUCT_ID_PRICES: ProductsProductIdPrices,
        PathValues.PRODUCTS_PRICES_ID: ProductsPricesId,
        PathValues.PRODUCTS_PRODUCT_ID_VARIANTS: ProductsProductIdVariants,
        PathValues.PRODUCTS_VARIANTS_ID: ProductsVariantsId,
        PathValues.WORKSPACES_WORKSPACE_ID_PRODUCTS_TAGS: WorkspacesWorkspaceIdProductsTags,
        PathValues.PRODUCTS_TAGS_ID: ProductsTagsId,
        PathValues.SHIPPING_PROFILES_PROFILE_ID_LOCATION_GROUPS: ShippingProfilesProfileIdLocationGroups,
        PathValues.SHIPPING_LOCATION_GROUPS_ID: ShippingLocationGroupsId,
        PathValues.WORKSPACES_WORKSPACE_ID_SHIPPING_PACKAGES: WorkspacesWorkspaceIdShippingPackages,
        PathValues.SHIPPING_PACKAGES_ID: ShippingPackagesId,
        PathValues.WORKSPACES_WORKSPACE_ID_SHIPPING_PROFILES: WorkspacesWorkspaceIdShippingProfiles,
        PathValues.SHIPPING_PROFILES_ID: ShippingProfilesId,
        PathValues.SHIPPING_ZONES_ZONE_ID_RATES: ShippingZonesZoneIdRates,
        PathValues.SHIPPING_RATES_ID: ShippingRatesId,
        PathValues.SHIPPING_LOCATION_GROUPS_LOCATION_GROUP_ID_ZONES: ShippingLocationGroupsLocationGroupIdZones,
        PathValues.SHIPPING_ZONES_ID: ShippingZonesId,
        PathValues.WORKSPACES_WORKSPACE_ID_SHIPPING_RATES_NAMES: WorkspacesWorkspaceIdShippingRatesNames,
        PathValues.SHIPPING_RATES_NAMES_ID: ShippingRatesNamesId,
        PathValues.WORKSPACES_WORKSPACE_ID_WEBHOOKS_OUTGOING_ENDPOINTS: WorkspacesWorkspaceIdWebhooksOutgoingEndpoints,
        PathValues.WEBHOOKS_OUTGOING_ENDPOINTS_ID: WebhooksOutgoingEndpointsId,
        PathValues.WORKSPACES_WORKSPACE_ID_WEBHOOKS_OUTGOING_EVENTS: WorkspacesWorkspaceIdWebhooksOutgoingEvents,
        PathValues.WEBHOOKS_OUTGOING_EVENTS_ID: WebhooksOutgoingEventsId,
    }
)
