# coding: utf-8

"""
    ClickFunnels API

    # Introduction  The ClickFunnels v2 API lets you:  - import data from other apps and sources into ClickFunnels and export data that you need somewhere else - extend the ClickFunnels platform to your own needs and embed it in your own applications - act on behalf of other ClickFunnels users via OAuth to offer extended services to other fellow ClickFunnels entrepreneurs  We are starting with exposing a given set of resources but the goal is to converge in terms of functionality with what the actual app is offering and also offering functionality on top.  For any feedback, please drop us a line at:  - https://feedback.myclickfunnels.com/feature-requests?category=api  For issues and support you can currently go here:  - https://help.clickfunnels.com/hc/en-us  # Authentication  Making your first request is easiest with a Bearer token:  ```shell $ curl 'https://myteam.myclickfunnels.com/api/v2/teams' \\ --header 'Authorization: Bearer AVJrj0ZMJ-xoraUk1xxVM6UuL9KXmsWmnJvvSosUO6X' [{\"id\":3,\"name\":\"My Team\", # ... more output...}] ```  How to get your API key step by step:  https://developers.myclickfunnels.com/docs/getting-started  # Rate limiting  The rate limit is currently set per IP address.  The actual rate limit and the approach on how this is handled is subject to change in future releases. Please let us know if you have special request limit needs.  # Pagination and Ordering  In order to paginate through a large list response, you can use our cursor-based pagination using the `id` field of a given object in the list.  There is a limit of 20 objects per list response ordered ascending by ID. So, you can get to items after the last one in the list, by taking the last item's ID and submitting it in a list request as the value of an `after` URL parameter. For example:  ```shell # The first 20 contacts are returned without any pagination nor ordering params: $ curl 'https://myteam.myclickfunnels.com/api/v2/workspaces/3/contacts' --header 'Authorization: Bearer ...' [{\"id\": 1, \"email_address\": \"first@contact.com\" ...}, {\"id\": 4, ...} ... {\"id\": 55, \"email_address\": \"last@contact.com\", ...}]  $ curl 'https://myteam.myclickfunnels.com/api/v2/workspaces/3/contacts?after=55' --header 'Authorization: Bearer ...' [{\"id\": 56, ...}] # There is one more record after ID 55. ```  The `after` param always acts as if you are \"turning the next page\". So if you order in a descending order, you will also use `after` to get to the next records:  ```shell $ curl 'https://myteam.myclickfunnels.com/api/v2/workspaces/3/contacts?sort_order=desc' --header 'Authorization: Bearer ...' [{\"id\": 56, ...},  {\"id\": 55, ...}, {\"id\": 4, ...}] # All contacts in descending order.  $ curl 'https://myteam.myclickfunnels.com/api/v2/workspaces/3/contacts?sort_order=desc&after=4' --header 'Authorization: Bearer ...' [{\"id\": 1, ...}] # There is one more contact on the next page after ID 55. ```  You can also use the `Pagination-Next` header to get the last ID value directly:  ```http request # Example header. Pagination-Next: 55 ```  And you can use the `Link` header to get the next page directly without needing to calculate it yourself:  ```http request # Example header. Link: <https://localteam.myclickfunnels.com/api/v2/workspaces/3/contacts?after=55>; rel=\"next\" ```  # Filtering  **Current filters**  If filtering is available for a specific endpoint, 'filter' will be listed as one of the options in the query parameters section of the Request area. Attributes by which you can filter will be listed as well.  **How it works**  There is a filter mechanism that adheres to some simple conventions. The filters provided on list endpoints, like `filter[email_address]` and `filter[id]` on the `Contacts` list endpoint, need to be \"simple\" and \"fast\". These filters are supposed to be easy to use and allow you to filter by one or more concrete values.  Here's an example of how you could use the filter to find a contact with a certain email address:  ```shell $ curl -g 'https://myteam.myclickfunnels.com/api/v2/workspaces/3/contacts?filter[email_address]=you@cf.com' --header 'Authorization: Bearer ...' [{\"email_address\": \"you@cf.com\",...}] ```  You can also filter by multiple values:  ```shell $ curl -g 'https://myteam.myclickfunnels.com/api/v2/workspaces/3/contacts?filter[email_address]=you@cf.com,u2@cf.com' --header 'Authorization: Bearer ...' [{\"email_address\": \"you@cf.com\",...}, {\"email_address\": \"u2@cf.com\",...}] ```  You can also filter by multiple attributes. Similar to filters that you might be familiar with when using GitHub (e.g.: filtering PRs by closed and assignee), those filters are `AND` filters, which give you the intersection of multiple records:  ```shell # If you@cf.com comes with an ID of 1, you will only see this record for this API call: $ curl -g 'https://myteam.myclickfunnels.com/api/v2/workspaces/3/contacts?filter[email_address]=you@cf.com,u2@cf.com&filter[id]=1' --header 'Authorization: Bearer ...' [{\"email_address\": \"you@cf.com\",...}]  # u2@cf.com is not included because it has a different ID that is not included in the filter. ```  > Please let us know your use case if you need more filter or complex search capabilities, we are  > actively improving these areas: https://feedback.myclickfunnels.com/feature-requests?category=api  # Webhooks  ClickFunnels webhooks allow you to react to many events in the ClickFunnels app on your own server,  Zapier and other similar tools.  You need to configure one or more endpoints within the ClickFunnels API by using the [Webhooks::Outgoing::Endpoints](https://apidocs.myclickfunnels.com/tag/Webhooks::Outgoing::Endpoint)  endpoint with the `event_type_ids` that you want to listen to (see below for all types).  Once configured, you will receive POST requrests from us to the configured endpoint URL with the [Webhooks::Outgoing::Event](https://apidocs.myclickfunnels.com/tag/Webhooks::Outgoing::Event#operation/getWebhooksOutgoingEvents)  payload, that will contain the subject payload in the `data` property. Like here for the `contact.identified` webhook in V2 version:  ```json {   \"id\": null,   \"public_id\": \"YVIOwX\",   \"workspace_id\": 32,   \"uuid\": \"94856650751bb2c141fc38436fd699cb\",   \"event_type_id\": \"contact.identified\",   \"subject_id\": 100,   \"subject_type\": \"Contact\",   \"data\": {     \"id\": 12,     \"public_id\": \"fdPJAZ\",     \"workspace_id\": 32,     \"anonymous\": null,     \"email_address\": \"joe.doe@example.com\",     \"first_name\": \"Joe\",     \"last_name\": \"Doe\",     \"phone_number\": \"1-241-822-5555\",     \"time_zone\": \"Pacific Time (US & Canada)\",     \"uuid\": \"26281ba2-7d3b-524d-8ea3-b01ff8414120\",     \"unsubscribed_at\": null,     \"last_notification_email_sent_at\": null,     \"fb_url\": \"https://www.facebook.com/example\",     \"twitter_url\": \"https://twitter.com/example\",     \"instagram_url\": \"https://instagram.com/example\",     \"linkedin_url\": \"https://www.linkedin.com/in/example\",     \"website_url\": \"https://example.com\",     \"created_at\": \"2023-12-31T18:57:40.871Z\",     \"updated_at\": \"2023-12-31T18:57:40.872Z\",     \"tags\": [       {         \"id\": 20,         \"public_id\": \"bRkQrc\",         \"name\": \"Example Tag\",         \"color\": \"#59b0a8\"       }     ]   },   \"created_at\": \"2023-12-31T18:57:41.872Z\" } ```  The content of the `data` property will vary depending on the event type that you are receiving.  Event types are structured like this: `subject.action`. So, for a `contact.identified` webhook, your `data` payload will contain data that you can source from [the contact response schema/example in the documentation](https://apidocs.myclickfunnels.com/tag/Contact#operation/getContacts). Similarly, for webhooks like `order.created` and `one-time-order.identified`, you will find the documentation in [the Order resource description](https://apidocs.myclickfunnels.com/tag/Order#operation/getOrders).  **Contact webhooks**  Are delivered with [the Contact data payload](https://apidocs.myclickfunnels.com/tag/Contact#operation/getContacts).  | <div style=\"width:375px;\">Event type</div>| Versions available | Description                                                            |  |--------------------------------------------------|--------------------|------------------------------------------------------------------------| | ***Contact***                                    |                    |                                                                        | | `contact.created`                                | V1, V2             | Sent when a Contact is created                                         | | `contact.updated`                                | V1, V2             | Sent when a Contact is updated                                         | | `contact.deleted`                                | V1, V2             | Sent when a Contact is deleted                                         | | `contact.identified`                             | V1, V2             | Sent when a Contact is identified by email address and/or phone number | | `contact.unsubscribed`                           | V1, V2             | Sent when a Contact unsubscribes from getting communications from the ClickFunnels workspace                         |  **Contact::AppliedTag webhooks**  Are delivered with [the Contact::AppliedTag data payload](https://apidocs.myclickfunnels.com/tag/Contacts::AppliedTag#operation/getContactsAppliedTags)  | <div style=\"width:375px;\">Event type</div>| Versions available | Description                                                            | |--------------------------------------------------|--------------------|------------------------------------------------------------------------| | ***Contacts::AppliedTag***                       |                    |                                                                        | | `contact/applied_tag.created`                    | V2                 | Sent when a Contacts::AppliedTag is created                            | | `contact/applied_tag.deleted`                    | V2                 | Sent when a Contacts::AppliedTag is deleted  **Courses webhooks**  Payloads correspond to the respective API resources:  - [Course](https://apidocs.myclickfunnels.com/tag/Course#operation/getCourses) - [Courses::Enrollment](https://apidocs.myclickfunnels.com/tag/Courses::Enrollment#operation/getCoursesEnrollments) - [Courses::Section](https://apidocs.myclickfunnels.com/tag/Courses::Section#operation/getCoursesSections) - [Courses::Lesson](https://apidocs.myclickfunnels.com/tag/Courses::Lesson#operation/getCoursesLessons)  | <div style=\"width:375px;\">Event type</div>| Versions available | Description                                                            |  |--------------------------------------------------|--------------------|------------------------------------------------------------------------| | ***Course***                                     |                    |                                                                        | | `course.created`                                 | V2             | Sent when a Course is created                                          | | `course.updated`                                 | V2             | Sent when a Course is updated                                          | | `course.deleted`                                 | V2             | Sent when a Course is deleted                                          | | `course.published`                               | V2                 | Sent when a Course has been published                                  | | ***Courses::Enrollment***                        |                    |                                                                        | | `courses/enrollment.created`                     | V2             | Sent when a Course::Enrollment is created                              | | `courses/enrollment.updated`                     | V2             | Sent when a Course::Enrollment is updated                              | | `courses/enrollment.deleted`                     | V2             | Sent when a Course::Enrollment is deleted                              | | `courses/enrollment.suspended`                   | V2                 | Sent when a Course::Enrollment has been suspended                      | | `courses/enrollment.course_completed`                   | V2                 | Sent when a Course::Enrollment completes a course                      | |  ***Courses::Section***                           |                    |                                                                        | | `courses/section.created`                        | V2             | Sent when a Courses::Section is created                                | | `courses/section.updated`                        | V2             | Sent when a Courses::Section is updated                                | | `courses/section.deleted`                        | V2             | Sent when a Courses::Section is deleted                                | | `courses/section.published`                       | V2                 | Sent when a Courses::Lesson has been published                         | |                      | ***Courses::Lesson***                            |                    |                                                                        | | `courses/lesson.created`                         | V2             | Sent when a Courses::Lesson is created                                 | | `courses/lesson.updated`                         | V2             | Sent when a Courses::Lesson is updated                                 | | `courses/lesson.deleted`                         | V2             | Sent when a Courses::Lesson is deleted                                 | | `courses/lesson.published`                       | V2                 | Sent when a Courses::Lesson has been published                         | |                      |  **Form submission webhooks**  Currently only available in V1 with the following JSON payload sample:  ```json {   \"data\": {     \"id\": \"4892034\",     \"type\": \"form_submission\",     \"attributes\": {       \"id\": 9874322,       \"data\": {         \"action\": \"submit\",         \"contact\": {           \"email\": \"joe.doe@example.com\",           \"aff_sub\": \"43242122e8c15480e9117143ce806d111\"         },         \"controller\": \"user_pages/pages\",         \"redirect_to\": \"https://www.example.com/thank-you-newsletter\"       },       \"page_id\": 2342324,       \"contact_id\": 234424,       \"created_at\": \"2023-11-14T23:25:54.070Z\",       \"updated_at\": \"2023-11-14T23:25:54.134Z\",       \"workspace_id\": 11     }   },   \"event_id\": \"bb50ab45-3da8-4532-9d7e-1c85d159ee71\",   \"event_type\": \"form_submission.created\",   \"subject_id\": 9894793,   \"subject_type\": \"FormSubmission\" } ```  | <div style=\"width:375px;\">Event type</div>| Versions available | Description                             |  |--------------------------------------------------|--------------------|-----------------------------------------| | ***Form::Submission***                           |                    |                                         | | `form/submission.created`                        | V1                 | Sent when a Form::Submission is created |  **Order webhooks**  Subscriptions and orders are all of type \"Order\" and their payload will be as in the [Order resources response payload](https://apidocs.myclickfunnels.com/tag/Order#operation/getOrders).  | <div style=\"width:375px;\">Event type</div> | Versions available | Description                                                                                               |  |--------------------------------------------|--------------------|-----------------------------------------------------------------------------------------------------------| | ***Order***                                |                    |                                                                                                           | | `order.created`                            | V1, V2             | Sent when an Order has been created                                                                       | | `order.updated`                            | V1, V2             | Sent when an Order has been updated                                                                       | | `order.deleted`                            | V1, V2             | Sent when an Order has been deleted                                                                       | | `order.completed`                          | V1, V2             | Sent when a one-time order was paid or a subscription order's service period has concluded                | | ***One-Time Order***                       |                    |                                                                                                           | | `one-time-order.completed`                 | V1, V2             | Sent when an Order of `order_type: \"one-time-order\"` has been completed                                   | | `one_time_order.refunded`                  | V1, V2             | Sent when an Order of `order_type: \"one-time-order\"` refund has been issued                               | | ***Subscription***                         |                    |                                                                                                           | | `subscription.canceled`                    | V1, V2             | Sent when an Order of `order_type: \"subscription\"` has been canceled                                      | | `subscription.reactivated`                 | V1, V2             | Sent when an Order of `order_type: \"subscription\"` that was canceled was reactivated                      | | `subscription.downgraded`                  | V1, V2             | Sent when an Order of `order_type: \"subscription\"` is changed to a product of smaller value               | | `subscription.upgraded`                    | V1, V2             | Sent when an Order of `order_type: \"subscription\"` is changed to a product of higher value                | | `subscription.churned`                     | V1, V2             | Sent when an Order of `order_type: \"subscription\"` has been churned                                       | | `subscription.modified`                    | V1, V2             | Sent when an Order of `order_type: \"subscription\"` has been modified                                      | | `subscription.activated`                   | V1, V2             | Sent when an Order of `order_type: \"subscription\"` has been activated                                     | | `subscription.completed`                   | V1, V2             | Sent when an Order of `order_type: \"subscription\"` has been completed                                     | | `subscription.first_payment_received`      | V1, V2             | Sent when an Order of `order_type: \"subscription\"` received first non-setup payment for subscription item |  **Orders::Transaction Webhooks**  Orders transactions are currently not part of our V2 API, but you can refer to this sample V2 webhook data payload:   ```json {   \"id\": 1821233,   \"arn\": null,   \"amount\": \"200.00\",   \"reason\": null,   \"result\": \"approved\",   \"status\": \"completed\",   \"currency\": \"USD\",   \"order_id\": 110030,   \"is_rebill\": false,   \"public_id\": \"asLOAY\",   \"created_at\": \"2024-01-30T06:25:06.754Z\",   \"updated_at\": \"2024-01-30T06:25:06.754Z\",   \"external_id\": \"txn_01HNCGNQE2C234PCFNERD2AVFZ\",   \"external_type\": \"sale\",   \"rebill_number\": 0,   \"adjusted_transaction_id\": null,   \"billing_payment_instruction_id\": 1333223,   \"billing_payment_instruction_type\": \"Billing::PaymentMethod\" } ```  | <div style=\"width:375px;\">Event type</div>                            | Versions available | Description                                       |  |---------------------------------------|--------------------|---------------------------------------------------| | ***Orders::Transaction***                      |                    |                                                   | | `orders/transaction.created`                   | V1, V2             | Sent when an Orders::Transaction has been created | | `orders/transaction.updated`                   | V1, V2             | Sent when an Orders::Transaction has been updated |  **Invoice webhooks**  With the [Invoice payload](https://apidocs.myclickfunnels.com/tag/Orders::Invoice).  | <div style=\"width:375px;\">Event type</div>   | Versions available   | Description                                                                 |  |----------------------------------------------|----------------------|-----------------------------------------------------------------------------| | ***Orders::Invoice***                        |                      |                                                                             | | `orders/invoice.created`                     | V1, V2               | Sent when an Orders::Invoice has been created                               | | `orders/invoice.updated`                     | V1, V2               | Sent when an Orders::Invoice has been updated                               | | `orders/invoice.refunded`                    | V1, V2               | Sent when an Orders::Invoice has been refunded                              | | `renewal-invoice-payment-declined`           | V1, V2               | Issued when a renewal Orders::Invoice payment has been declined             | | ***OneTimeOrder::Invoice***                  |                      |                                                                             | | `one-time-order.invoice.paid`                | V1, V2               | Sent when an Order::Invoice of `order_type: \"one-time-order\"` has been paid | | ***Subscription::Invoice***                  |                      |                                                                             | | `subscription/invoice.paid`                  | V1, V2               | Sent when an Order of `order_type: \"subscription\"` has been paid            |  **Workflow-based webhooks**  These are mostly used for [the UI-based ClickFunnels Workflows functionality](https://support.myclickfunnels.com/support/solutions/articles/150000156983-using-the-webhook-step-in-a-workflow).  | <div style=\"width:375px;\">Event type</div>| Versions available | Description                                                        |  |--------------------------------------------------|--------------------|--------------------------------------------------------------------|  | ***Runs::Step***                                 |                    |                                                                    | | `runs/step.dontrunme`                            | V1                 | Issued when the `dontrunme` step has been ran on a Workflow        | | ***Workflows::Integration::Step***               |                    |                                                                    | | `workflows_integration_step.executed`            | V1                 | Sent when a Workflows::Integration::Step has been executed         | | ***Workflows::Steps::IntegrationStep***          |                    |                                                                    | | `workflows/steps/integration_step.executed`      | V1                 | Sent when a Workflows::Steps::IntegrationStep has been executed    | | ***Workflows::Steps::DeliverWebhookStep***       |                    |                                                                    | | `workflows/steps/deliver_webhook_step.executed`  | V1                 | Sent when a Workflows::Steps::DeliverWebhookStep has been executed | 

    The version of the OpenAPI document: V2
    Created by: https://developers.myclickfunnels.com
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from click_funnels_python_sdk import schemas  # noqa: F401


class OrderAttributes(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)

    Orders
    """


    class MetaOapg:
        required = {
            "workspace_id",
            "workspace",
            "contact",
            "origination_channel_id",
            "currency",
            "id",
            "contact_id",
        }
        
        class properties:
            id = schemas.IntSchema
            workspace_id = schemas.IntSchema
            contact_id = schemas.IntSchema
            currency = schemas.StrSchema
            origination_channel_id = schemas.IntSchema
        
            @staticmethod
            def contact() -> typing.Type['ContactAttributes']:
                return ContactAttributes
        
            @staticmethod
            def workspace() -> typing.Type['WorkspaceAttributes']:
                return WorkspaceAttributes
            public_id = schemas.AnyTypeSchema
            order_number = schemas.AnyTypeSchema
            total_amount = schemas.AnyTypeSchema
            origination_channel_type = schemas.AnyTypeSchema
            shipping_address_first_name = schemas.AnyTypeSchema
            shipping_address_last_name = schemas.AnyTypeSchema
            shipping_address_organization_name = schemas.AnyTypeSchema
            shipping_address_phone_number = schemas.AnyTypeSchema
            shipping_address_street_one = schemas.AnyTypeSchema
            shipping_address_street_two = schemas.AnyTypeSchema
            shipping_address_city = schemas.AnyTypeSchema
            shipping_address_region = schemas.AnyTypeSchema
            shipping_address_country = schemas.AnyTypeSchema
            shipping_address_postal_code = schemas.AnyTypeSchema
            billing_address_street_one = schemas.AnyTypeSchema
            billing_address_street_two = schemas.AnyTypeSchema
            billing_address_city = schemas.AnyTypeSchema
            billing_address_region = schemas.AnyTypeSchema
            billing_address_country = schemas.AnyTypeSchema
            billing_address_postal_code = schemas.AnyTypeSchema
            page_id = schemas.AnyTypeSchema
            notes = schemas.AnyTypeSchema
            in_trial = schemas.AnyTypeSchema
            billing_status = schemas.AnyTypeSchema
            service_status = schemas.AnyTypeSchema
            order_type = schemas.AnyTypeSchema
            next_charge_at = schemas.AnyTypeSchema
            tax_amount = schemas.AnyTypeSchema
            trial_end_at = schemas.AnyTypeSchema
            billing_payment_method_id = schemas.AnyTypeSchema
            funnel_name = schemas.AnyTypeSchema
            tag_ids = schemas.AnyTypeSchema
            discount_ids = schemas.AnyTypeSchema
            activated_at = schemas.AnyTypeSchema
            
            
            class created_at(
                schemas.DateTimeBase,
                schemas.AnyTypeSchema,
            ):
            
            
                class MetaOapg:
                    format = 'date-time'
            
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'created_at':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
            class updated_at(
                schemas.DateTimeBase,
                schemas.AnyTypeSchema,
            ):
            
            
                class MetaOapg:
                    format = 'date-time'
            
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'updated_at':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            phone_number = schemas.AnyTypeSchema
            page_name = schemas.AnyTypeSchema
            origination_channel_name = schemas.AnyTypeSchema
            
            
            class order_page(
                schemas.AnyTypeSchema,
            ):
            
            
                class MetaOapg:
                    required = {
                        "name",
                        "id",
                    }
                    
                    class properties:
                        id = schemas.IntSchema
                        public_id = schemas.AnyTypeSchema
                        name = schemas.StrSchema
                        __annotations__ = {
                            "id": id,
                            "public_id": public_id,
                            "name": name,
                        }
            
                
                name: MetaOapg.properties.name
                id: MetaOapg.properties.id
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["public_id"]) -> MetaOapg.properties.public_id: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
                
                @typing.overload
                def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                
                def __getitem__(self, name: typing.Union[typing_extensions.Literal["id", "public_id", "name", ], str]):
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["public_id"]) -> typing.Union[MetaOapg.properties.public_id, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
                
                @typing.overload
                def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                
                def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["id", "public_id", "name", ], str]):
                    return super().get_item_oapg(name)
                
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                    name: typing.Union[MetaOapg.properties.name, str, ],
                    id: typing.Union[MetaOapg.properties.id, decimal.Decimal, int, ],
                    public_id: typing.Union[MetaOapg.properties.public_id, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'order_page':
                    return super().__new__(
                        cls,
                        *args,
                        name=name,
                        id=id,
                        public_id=public_id,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
            class contact_groups(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['OrderContactGroupAttributes']:
                        return OrderContactGroupAttributes
            
                def __new__(
                    cls,
                    arg: typing.Union[typing.Tuple['OrderContactGroupAttributes'], typing.List['OrderContactGroupAttributes']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'contact_groups':
                    return super().__new__(
                        cls,
                        arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'OrderContactGroupAttributes':
                    return super().__getitem__(i)
            
            
            class segments(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['OrderSegmentAttributes']:
                        return OrderSegmentAttributes
            
                def __new__(
                    cls,
                    arg: typing.Union[typing.Tuple['OrderSegmentAttributes'], typing.List['OrderSegmentAttributes']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'segments':
                    return super().__new__(
                        cls,
                        arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'OrderSegmentAttributes':
                    return super().__getitem__(i)
            
            
            class line_items(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['OrdersLineItemAttributes']:
                        return OrdersLineItemAttributes
            
                def __new__(
                    cls,
                    arg: typing.Union[typing.Tuple['OrdersLineItemAttributes'], typing.List['OrdersLineItemAttributes']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'line_items':
                    return super().__new__(
                        cls,
                        arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'OrdersLineItemAttributes':
                    return super().__getitem__(i)
            previous_line_item = schemas.AnyTypeSchema
            __annotations__ = {
                "id": id,
                "workspace_id": workspace_id,
                "contact_id": contact_id,
                "currency": currency,
                "origination_channel_id": origination_channel_id,
                "contact": contact,
                "workspace": workspace,
                "public_id": public_id,
                "order_number": order_number,
                "total_amount": total_amount,
                "origination_channel_type": origination_channel_type,
                "shipping_address_first_name": shipping_address_first_name,
                "shipping_address_last_name": shipping_address_last_name,
                "shipping_address_organization_name": shipping_address_organization_name,
                "shipping_address_phone_number": shipping_address_phone_number,
                "shipping_address_street_one": shipping_address_street_one,
                "shipping_address_street_two": shipping_address_street_two,
                "shipping_address_city": shipping_address_city,
                "shipping_address_region": shipping_address_region,
                "shipping_address_country": shipping_address_country,
                "shipping_address_postal_code": shipping_address_postal_code,
                "billing_address_street_one": billing_address_street_one,
                "billing_address_street_two": billing_address_street_two,
                "billing_address_city": billing_address_city,
                "billing_address_region": billing_address_region,
                "billing_address_country": billing_address_country,
                "billing_address_postal_code": billing_address_postal_code,
                "page_id": page_id,
                "notes": notes,
                "in_trial": in_trial,
                "billing_status": billing_status,
                "service_status": service_status,
                "order_type": order_type,
                "next_charge_at": next_charge_at,
                "tax_amount": tax_amount,
                "trial_end_at": trial_end_at,
                "billing_payment_method_id": billing_payment_method_id,
                "funnel_name": funnel_name,
                "tag_ids": tag_ids,
                "discount_ids": discount_ids,
                "activated_at": activated_at,
                "created_at": created_at,
                "updated_at": updated_at,
                "phone_number": phone_number,
                "page_name": page_name,
                "origination_channel_name": origination_channel_name,
                "order_page": order_page,
                "contact_groups": contact_groups,
                "segments": segments,
                "line_items": line_items,
                "previous_line_item": previous_line_item,
            }
    
    workspace_id: MetaOapg.properties.workspace_id
    workspace: 'WorkspaceAttributes'
    contact: 'ContactAttributes'
    origination_channel_id: MetaOapg.properties.origination_channel_id
    currency: MetaOapg.properties.currency
    id: MetaOapg.properties.id
    contact_id: MetaOapg.properties.contact_id
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["workspace_id"]) -> MetaOapg.properties.workspace_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["contact_id"]) -> MetaOapg.properties.contact_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["currency"]) -> MetaOapg.properties.currency: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["origination_channel_id"]) -> MetaOapg.properties.origination_channel_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["contact"]) -> 'ContactAttributes': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["workspace"]) -> 'WorkspaceAttributes': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["public_id"]) -> MetaOapg.properties.public_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["order_number"]) -> MetaOapg.properties.order_number: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["total_amount"]) -> MetaOapg.properties.total_amount: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["origination_channel_type"]) -> MetaOapg.properties.origination_channel_type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["shipping_address_first_name"]) -> MetaOapg.properties.shipping_address_first_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["shipping_address_last_name"]) -> MetaOapg.properties.shipping_address_last_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["shipping_address_organization_name"]) -> MetaOapg.properties.shipping_address_organization_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["shipping_address_phone_number"]) -> MetaOapg.properties.shipping_address_phone_number: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["shipping_address_street_one"]) -> MetaOapg.properties.shipping_address_street_one: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["shipping_address_street_two"]) -> MetaOapg.properties.shipping_address_street_two: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["shipping_address_city"]) -> MetaOapg.properties.shipping_address_city: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["shipping_address_region"]) -> MetaOapg.properties.shipping_address_region: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["shipping_address_country"]) -> MetaOapg.properties.shipping_address_country: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["shipping_address_postal_code"]) -> MetaOapg.properties.shipping_address_postal_code: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["billing_address_street_one"]) -> MetaOapg.properties.billing_address_street_one: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["billing_address_street_two"]) -> MetaOapg.properties.billing_address_street_two: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["billing_address_city"]) -> MetaOapg.properties.billing_address_city: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["billing_address_region"]) -> MetaOapg.properties.billing_address_region: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["billing_address_country"]) -> MetaOapg.properties.billing_address_country: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["billing_address_postal_code"]) -> MetaOapg.properties.billing_address_postal_code: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["page_id"]) -> MetaOapg.properties.page_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["notes"]) -> MetaOapg.properties.notes: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["in_trial"]) -> MetaOapg.properties.in_trial: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["billing_status"]) -> MetaOapg.properties.billing_status: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["service_status"]) -> MetaOapg.properties.service_status: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["order_type"]) -> MetaOapg.properties.order_type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["next_charge_at"]) -> MetaOapg.properties.next_charge_at: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["tax_amount"]) -> MetaOapg.properties.tax_amount: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["trial_end_at"]) -> MetaOapg.properties.trial_end_at: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["billing_payment_method_id"]) -> MetaOapg.properties.billing_payment_method_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["funnel_name"]) -> MetaOapg.properties.funnel_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["tag_ids"]) -> MetaOapg.properties.tag_ids: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["discount_ids"]) -> MetaOapg.properties.discount_ids: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["activated_at"]) -> MetaOapg.properties.activated_at: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["created_at"]) -> MetaOapg.properties.created_at: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["updated_at"]) -> MetaOapg.properties.updated_at: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["phone_number"]) -> MetaOapg.properties.phone_number: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["page_name"]) -> MetaOapg.properties.page_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["origination_channel_name"]) -> MetaOapg.properties.origination_channel_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["order_page"]) -> MetaOapg.properties.order_page: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["contact_groups"]) -> MetaOapg.properties.contact_groups: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["segments"]) -> MetaOapg.properties.segments: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["line_items"]) -> MetaOapg.properties.line_items: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["previous_line_item"]) -> MetaOapg.properties.previous_line_item: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["id", "workspace_id", "contact_id", "currency", "origination_channel_id", "contact", "workspace", "public_id", "order_number", "total_amount", "origination_channel_type", "shipping_address_first_name", "shipping_address_last_name", "shipping_address_organization_name", "shipping_address_phone_number", "shipping_address_street_one", "shipping_address_street_two", "shipping_address_city", "shipping_address_region", "shipping_address_country", "shipping_address_postal_code", "billing_address_street_one", "billing_address_street_two", "billing_address_city", "billing_address_region", "billing_address_country", "billing_address_postal_code", "page_id", "notes", "in_trial", "billing_status", "service_status", "order_type", "next_charge_at", "tax_amount", "trial_end_at", "billing_payment_method_id", "funnel_name", "tag_ids", "discount_ids", "activated_at", "created_at", "updated_at", "phone_number", "page_name", "origination_channel_name", "order_page", "contact_groups", "segments", "line_items", "previous_line_item", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["workspace_id"]) -> MetaOapg.properties.workspace_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["contact_id"]) -> MetaOapg.properties.contact_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["currency"]) -> MetaOapg.properties.currency: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["origination_channel_id"]) -> MetaOapg.properties.origination_channel_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["contact"]) -> 'ContactAttributes': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["workspace"]) -> 'WorkspaceAttributes': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["public_id"]) -> typing.Union[MetaOapg.properties.public_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["order_number"]) -> typing.Union[MetaOapg.properties.order_number, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["total_amount"]) -> typing.Union[MetaOapg.properties.total_amount, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["origination_channel_type"]) -> typing.Union[MetaOapg.properties.origination_channel_type, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["shipping_address_first_name"]) -> typing.Union[MetaOapg.properties.shipping_address_first_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["shipping_address_last_name"]) -> typing.Union[MetaOapg.properties.shipping_address_last_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["shipping_address_organization_name"]) -> typing.Union[MetaOapg.properties.shipping_address_organization_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["shipping_address_phone_number"]) -> typing.Union[MetaOapg.properties.shipping_address_phone_number, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["shipping_address_street_one"]) -> typing.Union[MetaOapg.properties.shipping_address_street_one, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["shipping_address_street_two"]) -> typing.Union[MetaOapg.properties.shipping_address_street_two, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["shipping_address_city"]) -> typing.Union[MetaOapg.properties.shipping_address_city, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["shipping_address_region"]) -> typing.Union[MetaOapg.properties.shipping_address_region, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["shipping_address_country"]) -> typing.Union[MetaOapg.properties.shipping_address_country, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["shipping_address_postal_code"]) -> typing.Union[MetaOapg.properties.shipping_address_postal_code, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["billing_address_street_one"]) -> typing.Union[MetaOapg.properties.billing_address_street_one, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["billing_address_street_two"]) -> typing.Union[MetaOapg.properties.billing_address_street_two, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["billing_address_city"]) -> typing.Union[MetaOapg.properties.billing_address_city, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["billing_address_region"]) -> typing.Union[MetaOapg.properties.billing_address_region, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["billing_address_country"]) -> typing.Union[MetaOapg.properties.billing_address_country, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["billing_address_postal_code"]) -> typing.Union[MetaOapg.properties.billing_address_postal_code, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["page_id"]) -> typing.Union[MetaOapg.properties.page_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["notes"]) -> typing.Union[MetaOapg.properties.notes, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["in_trial"]) -> typing.Union[MetaOapg.properties.in_trial, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["billing_status"]) -> typing.Union[MetaOapg.properties.billing_status, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["service_status"]) -> typing.Union[MetaOapg.properties.service_status, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["order_type"]) -> typing.Union[MetaOapg.properties.order_type, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["next_charge_at"]) -> typing.Union[MetaOapg.properties.next_charge_at, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["tax_amount"]) -> typing.Union[MetaOapg.properties.tax_amount, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["trial_end_at"]) -> typing.Union[MetaOapg.properties.trial_end_at, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["billing_payment_method_id"]) -> typing.Union[MetaOapg.properties.billing_payment_method_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["funnel_name"]) -> typing.Union[MetaOapg.properties.funnel_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["tag_ids"]) -> typing.Union[MetaOapg.properties.tag_ids, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["discount_ids"]) -> typing.Union[MetaOapg.properties.discount_ids, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["activated_at"]) -> typing.Union[MetaOapg.properties.activated_at, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["created_at"]) -> typing.Union[MetaOapg.properties.created_at, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["updated_at"]) -> typing.Union[MetaOapg.properties.updated_at, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["phone_number"]) -> typing.Union[MetaOapg.properties.phone_number, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["page_name"]) -> typing.Union[MetaOapg.properties.page_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["origination_channel_name"]) -> typing.Union[MetaOapg.properties.origination_channel_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["order_page"]) -> typing.Union[MetaOapg.properties.order_page, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["contact_groups"]) -> typing.Union[MetaOapg.properties.contact_groups, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["segments"]) -> typing.Union[MetaOapg.properties.segments, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["line_items"]) -> typing.Union[MetaOapg.properties.line_items, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["previous_line_item"]) -> typing.Union[MetaOapg.properties.previous_line_item, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["id", "workspace_id", "contact_id", "currency", "origination_channel_id", "contact", "workspace", "public_id", "order_number", "total_amount", "origination_channel_type", "shipping_address_first_name", "shipping_address_last_name", "shipping_address_organization_name", "shipping_address_phone_number", "shipping_address_street_one", "shipping_address_street_two", "shipping_address_city", "shipping_address_region", "shipping_address_country", "shipping_address_postal_code", "billing_address_street_one", "billing_address_street_two", "billing_address_city", "billing_address_region", "billing_address_country", "billing_address_postal_code", "page_id", "notes", "in_trial", "billing_status", "service_status", "order_type", "next_charge_at", "tax_amount", "trial_end_at", "billing_payment_method_id", "funnel_name", "tag_ids", "discount_ids", "activated_at", "created_at", "updated_at", "phone_number", "page_name", "origination_channel_name", "order_page", "contact_groups", "segments", "line_items", "previous_line_item", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        workspace_id: typing.Union[MetaOapg.properties.workspace_id, decimal.Decimal, int, ],
        workspace: 'WorkspaceAttributes',
        contact: 'ContactAttributes',
        origination_channel_id: typing.Union[MetaOapg.properties.origination_channel_id, decimal.Decimal, int, ],
        currency: typing.Union[MetaOapg.properties.currency, str, ],
        id: typing.Union[MetaOapg.properties.id, decimal.Decimal, int, ],
        contact_id: typing.Union[MetaOapg.properties.contact_id, decimal.Decimal, int, ],
        public_id: typing.Union[MetaOapg.properties.public_id, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        order_number: typing.Union[MetaOapg.properties.order_number, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        total_amount: typing.Union[MetaOapg.properties.total_amount, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        origination_channel_type: typing.Union[MetaOapg.properties.origination_channel_type, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        shipping_address_first_name: typing.Union[MetaOapg.properties.shipping_address_first_name, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        shipping_address_last_name: typing.Union[MetaOapg.properties.shipping_address_last_name, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        shipping_address_organization_name: typing.Union[MetaOapg.properties.shipping_address_organization_name, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        shipping_address_phone_number: typing.Union[MetaOapg.properties.shipping_address_phone_number, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        shipping_address_street_one: typing.Union[MetaOapg.properties.shipping_address_street_one, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        shipping_address_street_two: typing.Union[MetaOapg.properties.shipping_address_street_two, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        shipping_address_city: typing.Union[MetaOapg.properties.shipping_address_city, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        shipping_address_region: typing.Union[MetaOapg.properties.shipping_address_region, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        shipping_address_country: typing.Union[MetaOapg.properties.shipping_address_country, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        shipping_address_postal_code: typing.Union[MetaOapg.properties.shipping_address_postal_code, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        billing_address_street_one: typing.Union[MetaOapg.properties.billing_address_street_one, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        billing_address_street_two: typing.Union[MetaOapg.properties.billing_address_street_two, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        billing_address_city: typing.Union[MetaOapg.properties.billing_address_city, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        billing_address_region: typing.Union[MetaOapg.properties.billing_address_region, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        billing_address_country: typing.Union[MetaOapg.properties.billing_address_country, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        billing_address_postal_code: typing.Union[MetaOapg.properties.billing_address_postal_code, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        page_id: typing.Union[MetaOapg.properties.page_id, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        notes: typing.Union[MetaOapg.properties.notes, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        in_trial: typing.Union[MetaOapg.properties.in_trial, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        billing_status: typing.Union[MetaOapg.properties.billing_status, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        service_status: typing.Union[MetaOapg.properties.service_status, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        order_type: typing.Union[MetaOapg.properties.order_type, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        next_charge_at: typing.Union[MetaOapg.properties.next_charge_at, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        tax_amount: typing.Union[MetaOapg.properties.tax_amount, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        trial_end_at: typing.Union[MetaOapg.properties.trial_end_at, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        billing_payment_method_id: typing.Union[MetaOapg.properties.billing_payment_method_id, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        funnel_name: typing.Union[MetaOapg.properties.funnel_name, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        tag_ids: typing.Union[MetaOapg.properties.tag_ids, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        discount_ids: typing.Union[MetaOapg.properties.discount_ids, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        activated_at: typing.Union[MetaOapg.properties.activated_at, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        created_at: typing.Union[MetaOapg.properties.created_at, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        updated_at: typing.Union[MetaOapg.properties.updated_at, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        phone_number: typing.Union[MetaOapg.properties.phone_number, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        page_name: typing.Union[MetaOapg.properties.page_name, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        origination_channel_name: typing.Union[MetaOapg.properties.origination_channel_name, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        order_page: typing.Union[MetaOapg.properties.order_page, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        contact_groups: typing.Union[MetaOapg.properties.contact_groups, list, tuple, schemas.Unset] = schemas.unset,
        segments: typing.Union[MetaOapg.properties.segments, list, tuple, schemas.Unset] = schemas.unset,
        line_items: typing.Union[MetaOapg.properties.line_items, list, tuple, schemas.Unset] = schemas.unset,
        previous_line_item: typing.Union[MetaOapg.properties.previous_line_item, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'OrderAttributes':
        return super().__new__(
            cls,
            *args,
            workspace_id=workspace_id,
            workspace=workspace,
            contact=contact,
            origination_channel_id=origination_channel_id,
            currency=currency,
            id=id,
            contact_id=contact_id,
            public_id=public_id,
            order_number=order_number,
            total_amount=total_amount,
            origination_channel_type=origination_channel_type,
            shipping_address_first_name=shipping_address_first_name,
            shipping_address_last_name=shipping_address_last_name,
            shipping_address_organization_name=shipping_address_organization_name,
            shipping_address_phone_number=shipping_address_phone_number,
            shipping_address_street_one=shipping_address_street_one,
            shipping_address_street_two=shipping_address_street_two,
            shipping_address_city=shipping_address_city,
            shipping_address_region=shipping_address_region,
            shipping_address_country=shipping_address_country,
            shipping_address_postal_code=shipping_address_postal_code,
            billing_address_street_one=billing_address_street_one,
            billing_address_street_two=billing_address_street_two,
            billing_address_city=billing_address_city,
            billing_address_region=billing_address_region,
            billing_address_country=billing_address_country,
            billing_address_postal_code=billing_address_postal_code,
            page_id=page_id,
            notes=notes,
            in_trial=in_trial,
            billing_status=billing_status,
            service_status=service_status,
            order_type=order_type,
            next_charge_at=next_charge_at,
            tax_amount=tax_amount,
            trial_end_at=trial_end_at,
            billing_payment_method_id=billing_payment_method_id,
            funnel_name=funnel_name,
            tag_ids=tag_ids,
            discount_ids=discount_ids,
            activated_at=activated_at,
            created_at=created_at,
            updated_at=updated_at,
            phone_number=phone_number,
            page_name=page_name,
            origination_channel_name=origination_channel_name,
            order_page=order_page,
            contact_groups=contact_groups,
            segments=segments,
            line_items=line_items,
            previous_line_item=previous_line_item,
            _configuration=_configuration,
            **kwargs,
        )

from click_funnels_python_sdk.model.contact_attributes import ContactAttributes
from click_funnels_python_sdk.model.order_contact_group_attributes import OrderContactGroupAttributes
from click_funnels_python_sdk.model.order_segment_attributes import OrderSegmentAttributes
from click_funnels_python_sdk.model.orders_line_item_attributes import OrdersLineItemAttributes
from click_funnels_python_sdk.model.workspace_attributes import WorkspaceAttributes
