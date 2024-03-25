# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from click_funnels_python_sdk.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    CONTACT = "Contact"
    PRODUCT = "Product"
    CONTACTSTAG = "Contacts::Tag"
    FORM = "Form"
    FORMSFIELD_SET = "Forms::FieldSet"
    FORMSFIELD = "Forms::Field"
    FORMSFIELDSOPTION = "Forms::Fields::Option"
    FORMSSUBMISSION = "Forms::Submission"
    FORMSSUBMISSIONSANSWER = "Forms::Submissions::Answer"
    IMAGE = "Image"
    FULFILLMENT = "Fulfillment"
    FULFILLMENTSLOCATION = "Fulfillments::Location"
    ORDERSTAG = "Orders::Tag"
    PRODUCTSTAG = "Products::Tag"
    SHIPPINGPACKAGE = "Shipping::Package"
    SHIPPINGPROFILE = "Shipping::Profile"
    SHIPPINGRATE = "Shipping::Rate"
    SHIPPINGZONE = "Shipping::Zone"
    SHIPPINGRATESNAME = "Shipping::Rates::Name"
    WORKSPACE = "Workspace"
    CONTACTSAPPLIED_TAG = "Contacts::AppliedTag"
    COURSESENROLLMENT = "Courses::Enrollment"
    ORDERSAPPLIED_TAG = "Orders::AppliedTag"
    PRODUCTSPRICE = "Products::Price"
    PRODUCTSVARIANT = "Products::Variant"
    WEBHOOKSOUTGOINGENDPOINT = "Webhooks::Outgoing::Endpoint"
    TEAM = "Team"
    USER = "User"
    COURSESSECTION = "Courses::Section"
    COURSESLESSON = "Courses::Lesson"
    ORDER = "Order"
    COURSE = "Course"
    ORDERSINVOICE = "Orders::Invoice"
    ORDERSINVOICESRESTOCK = "Orders::Invoices::Restock"
    ORDERSTRANSACTION = "Orders::Transaction"
    SHIPPINGLOCATION_GROUP = "Shipping::LocationGroup"
    WEBHOOKSOUTGOINGEVENT = "Webhooks::Outgoing::Event"