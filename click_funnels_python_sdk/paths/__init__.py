# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from click_funnels_python_sdk.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    TEAMS = "/teams"
    TEAMS_ID = "/teams/{id}"
    USERS = "/users"
    USERS_ID = "/users/{id}"
    TEAMS_TEAM_ID_WORKSPACES = "/teams/{team_id}/workspaces"
    WORKSPACES_ID = "/workspaces/{id}"
    WORKSPACES_WORKSPACE_ID_CONTACTS = "/workspaces/{workspace_id}/contacts"
    CONTACTS_ID = "/contacts/{id}"
    CONTACTS_ID_GDPR_DESTROY = "/contacts/{id}/gdpr_destroy"
    WORKSPACES_WORKSPACE_ID_CONTACTS_UPSERT = "/workspaces/{workspace_id}/contacts/upsert"
    CONTACTS_CONTACT_ID_APPLIED_TAGS = "/contacts/{contact_id}/applied_tags"
    CONTACTS_APPLIED_TAGS_ID = "/contacts/applied_tags/{id}"
    WORKSPACES_WORKSPACE_ID_CONTACTS_TAGS = "/workspaces/{workspace_id}/contacts/tags"
    CONTACTS_TAGS_ID = "/contacts/tags/{id}"
    WORKSPACES_WORKSPACE_ID_COURSES = "/workspaces/{workspace_id}/courses"
    COURSES_ID = "/courses/{id}"
    COURSES_COURSE_ID_ENROLLMENTS = "/courses/{course_id}/enrollments"
    COURSES_ENROLLMENTS_ID = "/courses/enrollments/{id}"
    COURSES_COURSE_ID_SECTIONS = "/courses/{course_id}/sections"
    COURSES_SECTIONS_ID = "/courses/sections/{id}"
    COURSES_SECTIONS_SECTION_ID_LESSONS = "/courses/sections/{section_id}/lessons"
    COURSES_LESSONS_ID = "/courses/lessons/{id}"
    WORKSPACES_WORKSPACE_ID_FORMS = "/workspaces/{workspace_id}/forms"
    FORMS_ID = "/forms/{id}"
    FORMS_FORM_ID_FIELD_SETS = "/forms/{form_id}/field_sets"
    FORMS_FIELD_SETS_ID = "/forms/field_sets/{id}"
    FORMS_FIELD_SETS_FIELD_SET_ID_FIELDS = "/forms/field_sets/{field_set_id}/fields"
    FORMS_FIELDS_ID = "/forms/fields/{id}"
    FORMS_FIELDS_FIELD_ID_OPTIONS = "/forms/fields/{field_id}/options"
    FORMS_FIELDS_OPTIONS_ID = "/forms/fields/options/{id}"
    FORMS_FORM_ID_SUBMISSIONS = "/forms/{form_id}/submissions"
    FORMS_SUBMISSIONS_ID = "/forms/submissions/{id}"
    FORMS_SUBMISSIONS_SUBMISSION_ID_ANSWERS = "/forms/submissions/{submission_id}/answers"
    FORMS_SUBMISSIONS_ANSWERS_ID = "/forms/submissions/answers/{id}"
    WORKSPACES_WORKSPACE_ID_FULFILLMENTS = "/workspaces/{workspace_id}/fulfillments"
    FULFILLMENTS_ID = "/fulfillments/{id}"
    FULFILLMENTS_ID_CANCEL = "/fulfillments/{id}/cancel"
    WORKSPACES_WORKSPACE_ID_FULFILLMENTS_LOCATIONS = "/workspaces/{workspace_id}/fulfillments/locations"
    FULFILLMENTS_LOCATIONS_ID = "/fulfillments/locations/{id}"
    WORKSPACES_WORKSPACE_ID_IMAGES = "/workspaces/{workspace_id}/images"
    IMAGES_ID = "/images/{id}"
    WORKSPACES_WORKSPACE_ID_ORDERS = "/workspaces/{workspace_id}/orders"
    ORDERS_ID = "/orders/{id}"
    WORKSPACES_WORKSPACE_ID_ORDERS_INVOICES_RESTOCKS = "/workspaces/{workspace_id}/orders/invoices/restocks"
    ORDERS_INVOICES_RESTOCKS_ID = "/orders/invoices/restocks/{id}"
    ORDERS_ORDER_ID_APPLIED_TAGS = "/orders/{order_id}/applied_tags"
    ORDERS_APPLIED_TAGS_ID = "/orders/applied_tags/{id}"
    ORDERS_ORDER_ID_INVOICES = "/orders/{order_id}/invoices"
    ORDERS_INVOICES_ID = "/orders/invoices/{id}"
    ORDERS_ORDER_ID_TRANSACTIONS = "/orders/{order_id}/transactions"
    ORDERS_TRANSACTIONS_ID = "/orders/transactions/{id}"
    WORKSPACES_WORKSPACE_ID_ORDERS_TAGS = "/workspaces/{workspace_id}/orders/tags"
    ORDERS_TAGS_ID = "/orders/tags/{id}"
    WORKSPACES_WORKSPACE_ID_PRODUCTS = "/workspaces/{workspace_id}/products"
    PRODUCTS_ID = "/products/{id}"
    PRODUCTS_ID_ARCHIVE = "/products/{id}/archive"
    PRODUCTS_ID_UNARCHIVE = "/products/{id}/unarchive"
    PRODUCTS_PRODUCT_ID_PRICES = "/products/{product_id}/prices"
    PRODUCTS_PRICES_ID = "/products/prices/{id}"
    PRODUCTS_PRODUCT_ID_VARIANTS = "/products/{product_id}/variants"
    PRODUCTS_VARIANTS_ID = "/products/variants/{id}"
    WORKSPACES_WORKSPACE_ID_PRODUCTS_TAGS = "/workspaces/{workspace_id}/products/tags"
    PRODUCTS_TAGS_ID = "/products/tags/{id}"
    SHIPPING_PROFILES_PROFILE_ID_LOCATION_GROUPS = "/shipping/profiles/{profile_id}/location_groups"
    SHIPPING_LOCATION_GROUPS_ID = "/shipping/location_groups/{id}"
    WORKSPACES_WORKSPACE_ID_SHIPPING_PACKAGES = "/workspaces/{workspace_id}/shipping/packages"
    SHIPPING_PACKAGES_ID = "/shipping/packages/{id}"
    WORKSPACES_WORKSPACE_ID_SHIPPING_PROFILES = "/workspaces/{workspace_id}/shipping/profiles"
    SHIPPING_PROFILES_ID = "/shipping/profiles/{id}"
    SHIPPING_ZONES_ZONE_ID_RATES = "/shipping/zones/{zone_id}/rates"
    SHIPPING_RATES_ID = "/shipping/rates/{id}"
    SHIPPING_LOCATION_GROUPS_LOCATION_GROUP_ID_ZONES = "/shipping/location_groups/{location_group_id}/zones"
    SHIPPING_ZONES_ID = "/shipping/zones/{id}"
    WORKSPACES_WORKSPACE_ID_SHIPPING_RATES_NAMES = "/workspaces/{workspace_id}/shipping/rates/names"
    SHIPPING_RATES_NAMES_ID = "/shipping/rates/names/{id}"
    WORKSPACES_WORKSPACE_ID_WEBHOOKS_OUTGOING_ENDPOINTS = "/workspaces/{workspace_id}/webhooks/outgoing/endpoints"
    WEBHOOKS_OUTGOING_ENDPOINTS_ID = "/webhooks/outgoing/endpoints/{id}"
    WORKSPACES_WORKSPACE_ID_WEBHOOKS_OUTGOING_EVENTS = "/workspaces/{workspace_id}/webhooks/outgoing/events"
    WEBHOOKS_OUTGOING_EVENTS_ID = "/webhooks/outgoing/events/{id}"
