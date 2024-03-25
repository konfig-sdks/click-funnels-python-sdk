<div align="left">

[![Visit Clickfunnels](./header.png)](https://www.clickfunnels.com&#x2F;)

# Clickfunnels<a id="clickfunnels"></a>

# Introduction<a id="introduction"></a>

The ClickFunnels v2 API lets you:

- import data from other apps and sources into ClickFunnels and export data that you need somewhere else
- extend the ClickFunnels platform to your own needs and embed it in your own applications
- act on behalf of other ClickFunnels users via OAuth to offer extended services to other fellow ClickFunnels entrepreneurs

We are starting with exposing a given set of resources but the goal is to converge in terms of
functionality with what the actual app is offering and also offering functionality on top.

For any feedback, please drop us a line at:

- https://feedback.myclickfunnels.com/feature-requests?category=api

For issues and support you can currently go here:

- https://help.clickfunnels.com/hc/en-us

# Authentication<a id="authentication"></a>

Making your first request is easiest with a Bearer token:

```shell
$ curl 'https://myteam.myclickfunnels.com/api/v2/teams' \\
--header 'Authorization: Bearer AVJrj0ZMJ-xoraUk1xxVM6UuL9KXmsWmnJvvSosUO6X'
[{\"id\":3,\"name\":\"My Team\", # ... more output...}]
```

How to get your API key step by step:

https://developers.myclickfunnels.com/docs/getting-started

# Rate limiting<a id="rate-limiting"></a>

The rate limit is currently set per IP address.

The actual rate limit and the approach on how this is handled is subject to change in future
releases. Please let us know if you have special request limit needs.

# Pagination and Ordering<a id="pagination-and-ordering"></a>

In order to paginate through a large list response, you can use our cursor-based pagination using
the `id` field of a given object in the list.

There is a limit of 20 objects per list response ordered ascending by ID. So, you can get to items
after the last one in the list, by taking the last item's ID and submitting it in a list request
as the value of an `after` URL parameter. For example:

```shell
# The first 20 contacts are returned without any pagination nor ordering params:
$ curl 'https://myteam.myclickfunnels.com/api/v2/workspaces/3/contacts' --header 'Authorization: Bearer ...'
[{\"id\": 1, \"email_address\": \"first@contact.com\" ...}, {\"id\": 4, ...} ... {\"id\": 55, \"email_address\": \"last@contact.com\", ...}]

$ curl 'https://myteam.myclickfunnels.com/api/v2/workspaces/3/contacts?after=55' --header 'Authorization: Bearer ...'
[{\"id\": 56, ...}] # There is one more record after ID 55.
```

The `after` param always acts as if you are \"turning the next page\". So if you order in a descending
order, you will also use `after` to get to the next records:

```shell
$ curl 'https://myteam.myclickfunnels.com/api/v2/workspaces/3/contacts?sort_order=desc' --header 'Authorization: Bearer ...'
[{\"id\": 56, ...},  {\"id\": 55, ...}, {\"id\": 4, ...}] # All contacts in descending order.

$ curl 'https://myteam.myclickfunnels.com/api/v2/workspaces/3/contacts?sort_order=desc&after=4' --header 'Authorization: Bearer ...'
[{\"id\": 1, ...}] # There is one more contact on the next page after ID 55.
```

You can also use the `Pagination-Next` header to get the last ID value directly:

```http request
# Example header.
Pagination-Next: 55
```

And you can use the `Link` header to get the next page directly without needing to calculate it
yourself:

```http request
# Example header.
Link: <https://localteam.myclickfunnels.com/api/v2/workspaces/3/contacts?after=55>; rel=\"next\"
```

# Filtering<a id="filtering"></a>

**Current filters**

If filtering is available for a specific endpoint, 'filter' will be listed as one of the options in the query parameters section of the Request area. Attributes by which you can filter will be listed as well.

**How it works**

There is a filter mechanism that adheres to some simple conventions. The filters provided on
list endpoints, like `filter[email_address]` and `filter[id]` on the `Contacts` list endpoint, need
to be \"simple\" and \"fast\". These filters are supposed to be easy to use and allow you to filter by
one or more concrete values.

Here's an example of how you could use the filter to find a contact with a certain email address:

```shell
$ curl -g 'https://myteam.myclickfunnels.com/api/v2/workspaces/3/contacts?filter[email_address]=you@cf.com' --header 'Authorization: Bearer ...'
[{\"email_address\": \"you@cf.com\",...}]
```

You can also filter by multiple values:

```shell
$ curl -g 'https://myteam.myclickfunnels.com/api/v2/workspaces/3/contacts?filter[email_address]=you@cf.com,u2@cf.com' --header 'Authorization: Bearer ...'
[{\"email_address\": \"you@cf.com\",...}, {\"email_address\": \"u2@cf.com\",...}]
```

You can also filter by multiple attributes. Similar to filters that you might be familiar with when
using GitHub (e.g.: filtering PRs by closed and assignee), those filters are `AND` filters, which
give you the intersection of multiple records:

```shell
# If you@cf.com comes with an ID of 1, you will only see this record for this API call:
$ curl -g 'https://myteam.myclickfunnels.com/api/v2/workspaces/3/contacts?filter[email_address]=you@cf.com,u2@cf.com&filter[id]=1' --header 'Authorization: Bearer ...'
[{\"email_address\": \"you@cf.com\",...}] 
# u2@cf.com is not included because it has a different ID that is not included in the filter.
```

> Please let us know your use case if you need more filter or complex search capabilities, we are 
> actively improving these areas: https://feedback.myclickfunnels.com/feature-requests?category=api

# Webhooks<a id="webhooks"></a>

ClickFunnels webhooks allow you to react to many events in the ClickFunnels app on your own server, 
Zapier and other similar tools.

You need to configure one or more endpoints within the ClickFunnels API by using the [Webhooks::Outgoing::Endpoints](https://apidocs.myclickfunnels.com/tag/Webhooks::Outgoing::Endpoint) 
endpoint with the `event_type_ids` that you want to listen to (see below for all types).

Once configured, you will receive POST requrests from us to the configured endpoint URL with the
[Webhooks::Outgoing::Event](https://apidocs.myclickfunnels.com/tag/Webhooks::Outgoing::Event#operation/getWebhooksOutgoingEvents) 
payload, that will contain the subject payload in the `data` property. Like here for the
`contact.identified` webhook in V2 version:

```json
{
  \"id\": null,
  \"public_id\": \"YVIOwX\",
  \"workspace_id\": 32,
  \"uuid\": \"94856650751bb2c141fc38436fd699cb\",
  \"event_type_id\": \"contact.identified\",
  \"subject_id\": 100,
  \"subject_type\": \"Contact\",
  \"data\": {
    \"id\": 12,
    \"public_id\": \"fdPJAZ\",
    \"workspace_id\": 32,
    \"anonymous\": null,
    \"email_address\": \"joe.doe@example.com\",
    \"first_name\": \"Joe\",
    \"last_name\": \"Doe\",
    \"phone_number\": \"1-241-822-5555\",
    \"time_zone\": \"Pacific Time (US & Canada)\",
    \"uuid\": \"26281ba2-7d3b-524d-8ea3-b01ff8414120\",
    \"unsubscribed_at\": null,
    \"last_notification_email_sent_at\": null,
    \"fb_url\": \"https://www.facebook.com/example\",
    \"twitter_url\": \"https://twitter.com/example\",
    \"instagram_url\": \"https://instagram.com/example\",
    \"linkedin_url\": \"https://www.linkedin.com/in/example\",
    \"website_url\": \"https://example.com\",
    \"created_at\": \"2023-12-31T18:57:40.871Z\",
    \"updated_at\": \"2023-12-31T18:57:40.872Z\",
    \"tags\": [
      {
        \"id\": 20,
        \"public_id\": \"bRkQrc\",
        \"name\": \"Example Tag\",
        \"color\": \"#59b0a8\"
      }
    ]
  },
  \"created_at\": \"2023-12-31T18:57:41.872Z\"
}
```

The content of the `data` property will vary depending on the event type that you are receiving.

Event types are structured like this: `subject.action`. So, for a `contact.identified` webhook, your
`data` payload will contain data that you can source from [the contact response schema/example in the
documentation](https://apidocs.myclickfunnels.com/tag/Contact#operation/getContacts). Similarly, for
webhooks like `order.created` and `one-time-order.identified`, you will find the documentation in
[the Order resource description](https://apidocs.myclickfunnels.com/tag/Order#operation/getOrders).

**Contact webhooks**

Are delivered with [the Contact data payload](https://apidocs.myclickfunnels.com/tag/Contact#operation/getContacts).

| <div style=\"width:375px;\">Event type</div>| Versions available | Description                                                            | 
|--------------------------------------------------|--------------------|------------------------------------------------------------------------|
| ***Contact***                                    |                    |                                                                        |
| `contact.created`                                | V1, V2             | Sent when a Contact is created                                         |
| `contact.updated`                                | V1, V2             | Sent when a Contact is updated                                         |
| `contact.deleted`                                | V1, V2             | Sent when a Contact is deleted                                         |
| `contact.identified`                             | V1, V2             | Sent when a Contact is identified by email address and/or phone number |
| `contact.unsubscribed`                           | V1, V2             | Sent when a Contact unsubscribes from getting communications from the ClickFunnels workspace                         |

**Contact::AppliedTag webhooks**

Are delivered with [the Contact::AppliedTag data payload](https://apidocs.myclickfunnels.com/tag/Contacts::AppliedTag#operation/getContactsAppliedTags)

| <div style=\"width:375px;\">Event type</div>| Versions available | Description                                                            |
|--------------------------------------------------|--------------------|------------------------------------------------------------------------|
| ***Contacts::AppliedTag***                       |                    |                                                                        |
| `contact/applied_tag.created`                    | V2                 | Sent when a Contacts::AppliedTag is created                            |
| `contact/applied_tag.deleted`                    | V2                 | Sent when a Contacts::AppliedTag is deleted

**Courses webhooks**

Payloads correspond to the respective API resources:

- [Course](https://apidocs.myclickfunnels.com/tag/Course#operation/getCourses)
- [Courses::Enrollment](https://apidocs.myclickfunnels.com/tag/Courses::Enrollment#operation/getCoursesEnrollments)
- [Courses::Section](https://apidocs.myclickfunnels.com/tag/Courses::Section#operation/getCoursesSections)
- [Courses::Lesson](https://apidocs.myclickfunnels.com/tag/Courses::Lesson#operation/getCoursesLessons)

| <div style=\"width:375px;\">Event type</div>| Versions available | Description                                                            | 
|--------------------------------------------------|--------------------|------------------------------------------------------------------------|
| ***Course***                                     |                    |                                                                        |
| `course.created`                                 | V2             | Sent when a Course is created                                          |
| `course.updated`                                 | V2             | Sent when a Course is updated                                          |
| `course.deleted`                                 | V2             | Sent when a Course is deleted                                          |
| `course.published`                               | V2                 | Sent when a Course has been published                                  |
| ***Courses::Enrollment***                        |                    |                                                                        |
| `courses/enrollment.created`                     | V2             | Sent when a Course::Enrollment is created                              |
| `courses/enrollment.updated`                     | V2             | Sent when a Course::Enrollment is updated                              |
| `courses/enrollment.deleted`                     | V2             | Sent when a Course::Enrollment is deleted                              |
| `courses/enrollment.suspended`                   | V2                 | Sent when a Course::Enrollment has been suspended                      |
| `courses/enrollment.course_completed`                   | V2                 | Sent when a Course::Enrollment completes a course                      |
| 
***Courses::Section***                           |                    |                                                                        |
| `courses/section.created`                        | V2             | Sent when a Courses::Section is created                                |
| `courses/section.updated`                        | V2             | Sent when a Courses::Section is updated                                |
| `courses/section.deleted`                        | V2             | Sent when a Courses::Section is deleted                                |
| `courses/section.published`                       | V2                 | Sent when a Courses::Lesson has been published                         |
|                      |
***Courses::Lesson***                            |                    |                                                                        |
| `courses/lesson.created`                         | V2             | Sent when a Courses::Lesson is created                                 |
| `courses/lesson.updated`                         | V2             | Sent when a Courses::Lesson is updated                                 |
| `courses/lesson.deleted`                         | V2             | Sent when a Courses::Lesson is deleted                                 |
| `courses/lesson.published`                       | V2                 | Sent when a Courses::Lesson has been published                         |
|                      |

**Form submission webhooks**

Currently only available in V1 with the following JSON payload sample:

```json
{
  \"data\": {
    \"id\": \"4892034\",
    \"type\": \"form_submission\",
    \"attributes\": {
      \"id\": 9874322,
      \"data\": {
        \"action\": \"submit\",
        \"contact\": {
          \"email\": \"joe.doe@example.com\",
          \"aff_sub\": \"43242122e8c15480e9117143ce806d111\"
        },
        \"controller\": \"user_pages/pages\",
        \"redirect_to\": \"https://www.example.com/thank-you-newsletter\"
      },
      \"page_id\": 2342324,
      \"contact_id\": 234424,
      \"created_at\": \"2023-11-14T23:25:54.070Z\",
      \"updated_at\": \"2023-11-14T23:25:54.134Z\",
      \"workspace_id\": 11
    }
  },
  \"event_id\": \"bb50ab45-3da8-4532-9d7e-1c85d159ee71\",
  \"event_type\": \"form_submission.created\",
  \"subject_id\": 9894793,
  \"subject_type\": \"FormSubmission\"
}
```

| <div style=\"width:375px;\">Event type</div>| Versions available | Description                             | 
|--------------------------------------------------|--------------------|-----------------------------------------|
| ***Form::Submission***                           |                    |                                         |
| `form/submission.created`                        | V1                 | Sent when a Form::Submission is created |

**Order webhooks**

Subscriptions and orders are all of type \"Order\" and their payload will be as in the [Order resources
response payload](https://apidocs.myclickfunnels.com/tag/Order#operation/getOrders).

| <div style=\"width:375px;\">Event type</div> | Versions available | Description                                                                                               | 
|--------------------------------------------|--------------------|-----------------------------------------------------------------------------------------------------------|
| ***Order***                                |                    |                                                                                                           |
| `order.created`                            | V1, V2             | Sent when an Order has been created                                                                       |
| `order.updated`                            | V1, V2             | Sent when an Order has been updated                                                                       |
| `order.deleted`                            | V1, V2             | Sent when an Order has been deleted                                                                       |
| `order.completed`                          | V1, V2             | Sent when a one-time order was paid or a subscription order's service period has concluded                |
| ***One-Time Order***                       |                    |                                                                                                           |
| `one-time-order.completed`                 | V1, V2             | Sent when an Order of `order_type: \"one-time-order\"` has been completed                                   |
| `one_time_order.refunded`                  | V1, V2             | Sent when an Order of `order_type: \"one-time-order\"` refund has been issued                               |
| ***Subscription***                         |                    |                                                                                                           |
| `subscription.canceled`                    | V1, V2             | Sent when an Order of `order_type: \"subscription\"` has been canceled                                      |
| `subscription.reactivated`                 | V1, V2             | Sent when an Order of `order_type: \"subscription\"` that was canceled was reactivated                      |
| `subscription.downgraded`                  | V1, V2             | Sent when an Order of `order_type: \"subscription\"` is changed to a product of smaller value               |
| `subscription.upgraded`                    | V1, V2             | Sent when an Order of `order_type: \"subscription\"` is changed to a product of higher value                |
| `subscription.churned`                     | V1, V2             | Sent when an Order of `order_type: \"subscription\"` has been churned                                       |
| `subscription.modified`                    | V1, V2             | Sent when an Order of `order_type: \"subscription\"` has been modified                                      |
| `subscription.activated`                   | V1, V2             | Sent when an Order of `order_type: \"subscription\"` has been activated                                     |
| `subscription.completed`                   | V1, V2             | Sent when an Order of `order_type: \"subscription\"` has been completed                                     |
| `subscription.first_payment_received`      | V1, V2             | Sent when an Order of `order_type: \"subscription\"` received first non-setup payment for subscription item |

**Orders::Transaction Webhooks**

Orders transactions are currently not part of our V2 API, but you can refer to this sample V2 webhook data payload: 

```json
{
  \"id\": 1821233,
  \"arn\": null,
  \"amount\": \"200.00\",
  \"reason\": null,
  \"result\": \"approved\",
  \"status\": \"completed\",
  \"currency\": \"USD\",
  \"order_id\": 110030,
  \"is_rebill\": false,
  \"public_id\": \"asLOAY\",
  \"created_at\": \"2024-01-30T06:25:06.754Z\",
  \"updated_at\": \"2024-01-30T06:25:06.754Z\",
  \"external_id\": \"txn_01HNCGNQE2C234PCFNERD2AVFZ\",
  \"external_type\": \"sale\",
  \"rebill_number\": 0,
  \"adjusted_transaction_id\": null,
  \"billing_payment_instruction_id\": 1333223,
  \"billing_payment_instruction_type\": \"Billing::PaymentMethod\"
}
```

| <div style=\"width:375px;\">Event type</div>                            | Versions available | Description                                       | 
|---------------------------------------|--------------------|---------------------------------------------------|
| ***Orders::Transaction***                      |                    |                                                   |
| `orders/transaction.created`                   | V1, V2             | Sent when an Orders::Transaction has been created |
| `orders/transaction.updated`                   | V1, V2             | Sent when an Orders::Transaction has been updated |

**Invoice webhooks**

With the [Invoice payload](https://apidocs.myclickfunnels.com/tag/Orders::Invoice).

| <div style=\"width:375px;\">Event type</div>   | Versions available   | Description                                                                 | 
|----------------------------------------------|----------------------|-----------------------------------------------------------------------------|
| ***Orders::Invoice***                        |                      |                                                                             |
| `orders/invoice.created`                     | V1, V2               | Sent when an Orders::Invoice has been created                               |
| `orders/invoice.updated`                     | V1, V2               | Sent when an Orders::Invoice has been updated                               |
| `orders/invoice.refunded`                    | V1, V2               | Sent when an Orders::Invoice has been refunded                              |
| `renewal-invoice-payment-declined`           | V1, V2               | Issued when a renewal Orders::Invoice payment has been declined             |
| ***OneTimeOrder::Invoice***                  |                      |                                                                             |
| `one-time-order.invoice.paid`                | V1, V2               | Sent when an Order::Invoice of `order_type: \"one-time-order\"` has been paid |
| ***Subscription::Invoice***                  |                      |                                                                             |
| `subscription/invoice.paid`                  | V1, V2               | Sent when an Order of `order_type: \"subscription\"` has been paid            |

**Workflow-based webhooks**

These are mostly used for [the UI-based ClickFunnels Workflows functionality](https://support.myclickfunnels.com/support/solutions/articles/150000156983-using-the-webhook-step-in-a-workflow).

| <div style=\"width:375px;\">Event type</div>| Versions available | Description                                                        | 
|--------------------------------------------------|--------------------|--------------------------------------------------------------------| 
| ***Runs::Step***                                 |                    |                                                                    |
| `runs/step.dontrunme`                            | V1                 | Issued when the `dontrunme` step has been ran on a Workflow        |
| ***Workflows::Integration::Step***               |                    |                                                                    |
| `workflows_integration_step.executed`            | V1                 | Sent when a Workflows::Integration::Step has been executed         |
| ***Workflows::Steps::IntegrationStep***          |                    |                                                                    |
| `workflows/steps/integration_step.executed`      | V1                 | Sent when a Workflows::Steps::IntegrationStep has been executed    |
| ***Workflows::Steps::DeliverWebhookStep***       |                    |                                                                    |
| `workflows/steps/deliver_webhook_step.executed`  | V1                 | Sent when a Workflows::Steps::DeliverWebhookStep has been executed |



</div>

## Table of Contents<a id="table-of-contents"></a>

<!-- toc -->

- [Requirements](#requirements)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Async](#async)
- [Raw HTTP Response](#raw-http-response)
- [Reference](#reference)
  * [`clickfunnels.contact.create_new_contact`](#clickfunnelscontactcreate_new_contact)
  * [`clickfunnels.contact.get_contact_by_id`](#clickfunnelscontactget_contact_by_id)
  * [`clickfunnels.contact.list_for_workspace`](#clickfunnelscontactlist_for_workspace)
  * [`clickfunnels.contact.redact_personally_identifiable`](#clickfunnelscontactredact_personally_identifiable)
  * [`clickfunnels.contact.remove_by_id`](#clickfunnelscontactremove_by_id)
  * [`clickfunnels.contact.update_contact_by_id`](#clickfunnelscontactupdate_contact_by_id)
  * [`clickfunnels.contact.upsert`](#clickfunnelscontactupsert)
  * [`clickfunnels.contacts::applied_tag.create_applied_tag`](#clickfunnelscontactsapplied_tagcreate_applied_tag)
  * [`clickfunnels.contacts::applied_tag.get_for_contact`](#clickfunnelscontactsapplied_tagget_for_contact)
  * [`clickfunnels.contacts::applied_tag.list`](#clickfunnelscontactsapplied_taglist)
  * [`clickfunnels.contacts::applied_tag.remove_by_id`](#clickfunnelscontactsapplied_tagremove_by_id)
  * [`clickfunnels.contacts::tag.create_new_tag`](#clickfunnelscontactstagcreate_new_tag)
  * [`clickfunnels.contacts::tag.get_single`](#clickfunnelscontactstagget_single)
  * [`clickfunnels.contacts::tag.list`](#clickfunnelscontactstaglist)
  * [`clickfunnels.contacts::tag.remove`](#clickfunnelscontactstagremove)
  * [`clickfunnels.contacts::tag.update_specific_tag`](#clickfunnelscontactstagupdate_specific_tag)
  * [`clickfunnels.course.get_by_id`](#clickfunnelscourseget_by_id)
  * [`clickfunnels.course.list_for_workspace`](#clickfunnelscourselist_for_workspace)
  * [`clickfunnels.courses::enrollment.create_new_enrollment`](#clickfunnelscoursesenrollmentcreate_new_enrollment)
  * [`clickfunnels.courses::enrollment.get_by_id`](#clickfunnelscoursesenrollmentget_by_id)
  * [`clickfunnels.courses::enrollment.list`](#clickfunnelscoursesenrollmentlist)
  * [`clickfunnels.courses::enrollment.update_specific_enrollment`](#clickfunnelscoursesenrollmentupdate_specific_enrollment)
  * [`clickfunnels.courses::lesson.get_by_id`](#clickfunnelscourseslessonget_by_id)
  * [`clickfunnels.courses::lesson.list_lessons`](#clickfunnelscourseslessonlist_lessons)
  * [`clickfunnels.courses::lesson.update_lesson_by_id`](#clickfunnelscourseslessonupdate_lesson_by_id)
  * [`clickfunnels.courses::section.get_section`](#clickfunnelscoursessectionget_section)
  * [`clickfunnels.courses::section.list_sections`](#clickfunnelscoursessectionlist_sections)
  * [`clickfunnels.courses::section.update_section_by_id`](#clickfunnelscoursessectionupdate_section_by_id)
  * [`clickfunnels.form.create_new_form`](#clickfunnelsformcreate_new_form)
  * [`clickfunnels.form.get_form`](#clickfunnelsformget_form)
  * [`clickfunnels.form.list_workspace_forms`](#clickfunnelsformlist_workspace_forms)
  * [`clickfunnels.form.remove`](#clickfunnelsformremove)
  * [`clickfunnels.form.update_form_by_id`](#clickfunnelsformupdate_form_by_id)
  * [`clickfunnels.forms::field.add_new_field`](#clickfunnelsformsfieldadd_new_field)
  * [`clickfunnels.forms::field.get_field`](#clickfunnelsformsfieldget_field)
  * [`clickfunnels.forms::field.list_fields_for_field_set`](#clickfunnelsformsfieldlist_fields_for_field_set)
  * [`clickfunnels.forms::field.remove_field`](#clickfunnelsformsfieldremove_field)
  * [`clickfunnels.forms::field.update_field_by_id`](#clickfunnelsformsfieldupdate_field_by_id)
  * [`clickfunnels.forms::field_set.create_new_field_set`](#clickfunnelsformsfield_setcreate_new_field_set)
  * [`clickfunnels.forms::field_set.get_field_set`](#clickfunnelsformsfield_setget_field_set)
  * [`clickfunnels.forms::field_set.list`](#clickfunnelsformsfield_setlist)
  * [`clickfunnels.forms::field_set.remove`](#clickfunnelsformsfield_setremove)
  * [`clickfunnels.forms::field_set.update_field_set_by_id`](#clickfunnelsformsfield_setupdate_field_set_by_id)
  * [`clickfunnels.forms::fields::option.create_new_field_option`](#clickfunnelsformsfieldsoptioncreate_new_field_option)
  * [`clickfunnels.forms::fields::option.delete_option_for_field`](#clickfunnelsformsfieldsoptiondelete_option_for_field)
  * [`clickfunnels.forms::fields::option.get_field_option`](#clickfunnelsformsfieldsoptionget_field_option)
  * [`clickfunnels.forms::fields::option.list`](#clickfunnelsformsfieldsoptionlist)
  * [`clickfunnels.forms::fields::option.update_field_option`](#clickfunnelsformsfieldsoptionupdate_field_option)
  * [`clickfunnels.forms::submission.create_new_submission`](#clickfunnelsformssubmissioncreate_new_submission)
  * [`clickfunnels.forms::submission.get_by_id`](#clickfunnelsformssubmissionget_by_id)
  * [`clickfunnels.forms::submission.list`](#clickfunnelsformssubmissionlist)
  * [`clickfunnels.forms::submission.remove`](#clickfunnelsformssubmissionremove)
  * [`clickfunnels.forms::submission.update_submission`](#clickfunnelsformssubmissionupdate_submission)
  * [`clickfunnels.forms::submissions::answer.add_new_answer`](#clickfunnelsformssubmissionsansweradd_new_answer)
  * [`clickfunnels.forms::submissions::answer.get`](#clickfunnelsformssubmissionsanswerget)
  * [`clickfunnels.forms::submissions::answer.list`](#clickfunnelsformssubmissionsanswerlist)
  * [`clickfunnels.forms::submissions::answer.remove_by_id`](#clickfunnelsformssubmissionsanswerremove_by_id)
  * [`clickfunnels.forms::submissions::answer.update_answer`](#clickfunnelsformssubmissionsanswerupdate_answer)
  * [`clickfunnels.fulfillment.cancel_fulfillment`](#clickfunnelsfulfillmentcancel_fulfillment)
  * [`clickfunnels.fulfillment.create`](#clickfunnelsfulfillmentcreate)
  * [`clickfunnels.fulfillment.get_by_id`](#clickfunnelsfulfillmentget_by_id)
  * [`clickfunnels.fulfillment.list`](#clickfunnelsfulfillmentlist)
  * [`clickfunnels.fulfillment.update_by_id`](#clickfunnelsfulfillmentupdate_by_id)
  * [`clickfunnels.fulfillments::location.create_new_location`](#clickfunnelsfulfillmentslocationcreate_new_location)
  * [`clickfunnels.fulfillments::location.get_by_id`](#clickfunnelsfulfillmentslocationget_by_id)
  * [`clickfunnels.fulfillments::location.list`](#clickfunnelsfulfillmentslocationlist)
  * [`clickfunnels.fulfillments::location.remove_by_id`](#clickfunnelsfulfillmentslocationremove_by_id)
  * [`clickfunnels.fulfillments::location.update_by_id`](#clickfunnelsfulfillmentslocationupdate_by_id)
  * [`clickfunnels.image.create`](#clickfunnelsimagecreate)
  * [`clickfunnels.image.get_by_id`](#clickfunnelsimageget_by_id)
  * [`clickfunnels.image.list`](#clickfunnelsimagelist)
  * [`clickfunnels.image.remove_by_id`](#clickfunnelsimageremove_by_id)
  * [`clickfunnels.image.update_by_id`](#clickfunnelsimageupdate_by_id)
  * [`clickfunnels.order.get_single`](#clickfunnelsorderget_single)
  * [`clickfunnels.order.list_orders`](#clickfunnelsorderlist_orders)
  * [`clickfunnels.order.update_specific`](#clickfunnelsorderupdate_specific)
  * [`clickfunnels.orders::applied_tag.create_applied_tag`](#clickfunnelsordersapplied_tagcreate_applied_tag)
  * [`clickfunnels.orders::applied_tag.get`](#clickfunnelsordersapplied_tagget)
  * [`clickfunnels.orders::applied_tag.list`](#clickfunnelsordersapplied_taglist)
  * [`clickfunnels.orders::applied_tag.remove_by_id`](#clickfunnelsordersapplied_tagremove_by_id)
  * [`clickfunnels.orders::invoice.get_for_order`](#clickfunnelsordersinvoiceget_for_order)
  * [`clickfunnels.orders::invoice.list_for_order`](#clickfunnelsordersinvoicelist_for_order)
  * [`clickfunnels.orders::invoices::restock.get_restock`](#clickfunnelsordersinvoicesrestockget_restock)
  * [`clickfunnels.orders::invoices::restock.list_restocks`](#clickfunnelsordersinvoicesrestocklist_restocks)
  * [`clickfunnels.orders::tag.create_new_tag`](#clickfunnelsorderstagcreate_new_tag)
  * [`clickfunnels.orders::tag.get_single`](#clickfunnelsorderstagget_single)
  * [`clickfunnels.orders::tag.list`](#clickfunnelsorderstaglist)
  * [`clickfunnels.orders::tag.remove`](#clickfunnelsorderstagremove)
  * [`clickfunnels.orders::tag.update_specific_order_tag`](#clickfunnelsorderstagupdate_specific_order_tag)
  * [`clickfunnels.orders::transaction.get_by_id`](#clickfunnelsorderstransactionget_by_id)
  * [`clickfunnels.orders::transaction.get_list`](#clickfunnelsorderstransactionget_list)
  * [`clickfunnels.product.add_new_to_workspace`](#clickfunnelsproductadd_new_to_workspace)
  * [`clickfunnels.product.archive_product`](#clickfunnelsproductarchive_product)
  * [`clickfunnels.product.get_for_workspace`](#clickfunnelsproductget_for_workspace)
  * [`clickfunnels.product.list_for_workspace`](#clickfunnelsproductlist_for_workspace)
  * [`clickfunnels.product.unarchive_by_id`](#clickfunnelsproductunarchive_by_id)
  * [`clickfunnels.product.update_for_workspace`](#clickfunnelsproductupdate_for_workspace)
  * [`clickfunnels.products::price.create_variant_price`](#clickfunnelsproductspricecreate_variant_price)
  * [`clickfunnels.products::price.get_single_price`](#clickfunnelsproductspriceget_single_price)
  * [`clickfunnels.products::price.list_for_variant`](#clickfunnelsproductspricelist_for_variant)
  * [`clickfunnels.products::price.update_single_price`](#clickfunnelsproductspriceupdate_single_price)
  * [`clickfunnels.products::tag.create_new_tag`](#clickfunnelsproductstagcreate_new_tag)
  * [`clickfunnels.products::tag.delete_tag_by_id`](#clickfunnelsproductstagdelete_tag_by_id)
  * [`clickfunnels.products::tag.get_tag_by_id`](#clickfunnelsproductstagget_tag_by_id)
  * [`clickfunnels.products::tag.list`](#clickfunnelsproductstaglist)
  * [`clickfunnels.products::tag.update_tag_by_id`](#clickfunnelsproductstagupdate_tag_by_id)
  * [`clickfunnels.products::variant.create_new_variant`](#clickfunnelsproductsvariantcreate_new_variant)
  * [`clickfunnels.products::variant.get_single`](#clickfunnelsproductsvariantget_single)
  * [`clickfunnels.products::variant.list`](#clickfunnelsproductsvariantlist)
  * [`clickfunnels.products::variant.update_single`](#clickfunnelsproductsvariantupdate_single)
  * [`clickfunnels.shipping::location_group.get_profile_location_group`](#clickfunnelsshippinglocation_groupget_profile_location_group)
  * [`clickfunnels.shipping::location_group.list`](#clickfunnelsshippinglocation_grouplist)
  * [`clickfunnels.shipping::package.add_to_workspace`](#clickfunnelsshippingpackageadd_to_workspace)
  * [`clickfunnels.shipping::package.get_for_workspace`](#clickfunnelsshippingpackageget_for_workspace)
  * [`clickfunnels.shipping::package.list_for_workspace`](#clickfunnelsshippingpackagelist_for_workspace)
  * [`clickfunnels.shipping::package.remove_by_id`](#clickfunnelsshippingpackageremove_by_id)
  * [`clickfunnels.shipping::package.update_for_workspace`](#clickfunnelsshippingpackageupdate_for_workspace)
  * [`clickfunnels.shipping::profile.create_new`](#clickfunnelsshippingprofilecreate_new)
  * [`clickfunnels.shipping::profile.get_workspace_profile`](#clickfunnelsshippingprofileget_workspace_profile)
  * [`clickfunnels.shipping::profile.list`](#clickfunnelsshippingprofilelist)
  * [`clickfunnels.shipping::profile.remove`](#clickfunnelsshippingprofileremove)
  * [`clickfunnels.shipping::profile.update_for_workspace`](#clickfunnelsshippingprofileupdate_for_workspace)
  * [`clickfunnels.shipping::rate.create_rate_for_zone`](#clickfunnelsshippingratecreate_rate_for_zone)
  * [`clickfunnels.shipping::rate.get_rate_by_id`](#clickfunnelsshippingrateget_rate_by_id)
  * [`clickfunnels.shipping::rate.list_for_zone`](#clickfunnelsshippingratelist_for_zone)
  * [`clickfunnels.shipping::rate.remove_by_id`](#clickfunnelsshippingrateremove_by_id)
  * [`clickfunnels.shipping::rate.update_rate_for_zone`](#clickfunnelsshippingrateupdate_rate_for_zone)
  * [`clickfunnels.shipping::rates::name.create_new_rate_name`](#clickfunnelsshippingratesnamecreate_new_rate_name)
  * [`clickfunnels.shipping::rates::name.get_rate_name`](#clickfunnelsshippingratesnameget_rate_name)
  * [`clickfunnels.shipping::rates::name.list`](#clickfunnelsshippingratesnamelist)
  * [`clickfunnels.shipping::rates::name.remove`](#clickfunnelsshippingratesnameremove)
  * [`clickfunnels.shipping::rates::name.update_name`](#clickfunnelsshippingratesnameupdate_name)
  * [`clickfunnels.shipping::zone.add_new_zone`](#clickfunnelsshippingzoneadd_new_zone)
  * [`clickfunnels.shipping::zone.get_zone_by_id`](#clickfunnelsshippingzoneget_zone_by_id)
  * [`clickfunnels.shipping::zone.list_zones`](#clickfunnelsshippingzonelist_zones)
  * [`clickfunnels.shipping::zone.remove_by_id`](#clickfunnelsshippingzoneremove_by_id)
  * [`clickfunnels.shipping::zone.update_zone_by_id`](#clickfunnelsshippingzoneupdate_zone_by_id)
  * [`clickfunnels.team.get_all`](#clickfunnelsteamget_all)
  * [`clickfunnels.team.get_single`](#clickfunnelsteamget_single)
  * [`clickfunnels.team.update_team_by_id`](#clickfunnelsteamupdate_team_by_id)
  * [`clickfunnels.user.get_single`](#clickfunnelsuserget_single)
  * [`clickfunnels.user.list_current_account_users`](#clickfunnelsuserlist_current_account_users)
  * [`clickfunnels.user.update_single_user`](#clickfunnelsuserupdate_single_user)
  * [`clickfunnels.webhooks::outgoing::endpoint.create_new`](#clickfunnelswebhooksoutgoingendpointcreate_new)
  * [`clickfunnels.webhooks::outgoing::endpoint.get`](#clickfunnelswebhooksoutgoingendpointget)
  * [`clickfunnels.webhooks::outgoing::endpoint.list_endpoints`](#clickfunnelswebhooksoutgoingendpointlist_endpoints)
  * [`clickfunnels.webhooks::outgoing::endpoint.update_endpoint`](#clickfunnelswebhooksoutgoingendpointupdate_endpoint)
  * [`clickfunnels.webhooks::outgoing::event.get_for_workspace`](#clickfunnelswebhooksoutgoingeventget_for_workspace)
  * [`clickfunnels.webhooks::outgoing::event.list_for_workspace`](#clickfunnelswebhooksoutgoingeventlist_for_workspace)
  * [`clickfunnels.workspace.add_new`](#clickfunnelsworkspaceadd_new)
  * [`clickfunnels.workspace.get_by_id`](#clickfunnelsworkspaceget_by_id)
  * [`clickfunnels.workspace.list_workspaces`](#clickfunnelsworkspacelist_workspaces)
  * [`clickfunnels.workspace.update`](#clickfunnelsworkspaceupdate)

<!-- tocstop -->

## Requirements<a id="requirements"></a>

Python >=3.7

## Installation<a id="installation"></a>
<div align="center">
  <a href="https://konfigthis.com/sdk-sign-up?company=ClickFunnels&language=Python">
    <img src="https://raw.githubusercontent.com/konfig-dev/brand-assets/HEAD/cta-images/python-cta.png" width="70%">
  </a>
</div>

## Getting Started<a id="getting-started"></a>

```python
from pprint import pprint
from click_funnels_python_sdk import ClickFunnels, ApiException

clickfunnels = ClickFunnels(

    access_token = 'YOUR_BEARER_TOKEN'
)

try:
    # Create Contact
    create_new_contact_response = clickfunnels.contact.create_new_contact(
        workspace_id=1,
        contact={
    },
    )
    print(create_new_contact_response)
except ApiException as e:
    print("Exception when calling ContactApi.create_new_contact: %s\n" % e)
    pprint(e.body)
    if e.status == 400:
        pprint(e.body["error"])
    if e.status == 401:
        pprint(e.body["error"])
    pprint(e.headers)
    pprint(e.status)
    pprint(e.reason)
    pprint(e.round_trip_time)
```

## Async<a id="async"></a>

`async` support is available by prepending `a` to any method.

```python

import asyncio
from pprint import pprint
from click_funnels_python_sdk import ClickFunnels, ApiException

clickfunnels = ClickFunnels(

    access_token = 'YOUR_BEARER_TOKEN'
)

async def main():
    try:
        # Create Contact
        create_new_contact_response = await clickfunnels.contact.acreate_new_contact(
            workspace_id=1,
            contact={
    },
        )
        print(create_new_contact_response)
    except ApiException as e:
        print("Exception when calling ContactApi.create_new_contact: %s\n" % e)
        pprint(e.body)
        if e.status == 400:
            pprint(e.body["error"])
        if e.status == 401:
            pprint(e.body["error"])
        pprint(e.headers)
        pprint(e.status)
        pprint(e.reason)
        pprint(e.round_trip_time)

asyncio.run(main())
```

## Raw HTTP Response<a id="raw-http-response"></a>

To access raw HTTP response values, use the `.raw` namespace.

```python
from pprint import pprint
from click_funnels_python_sdk import ClickFunnels, ApiException

clickfunnels = ClickFunnels(

    access_token = 'YOUR_BEARER_TOKEN'
)

try:
    # Create Contact
    create_new_contact_response = clickfunnels.contact.raw.create_new_contact(
        workspace_id=1,
        contact={
    },
    )
    pprint(create_new_contact_response.body)
    pprint(create_new_contact_response.body["id"])
    pprint(create_new_contact_response.body["workspace_id"])
    pprint(create_new_contact_response.body["uuid"])
    pprint(create_new_contact_response.body["tags"])
    pprint(create_new_contact_response.body["public_id"])
    pprint(create_new_contact_response.body["anonymous"])
    pprint(create_new_contact_response.body["email_address"])
    pprint(create_new_contact_response.body["first_name"])
    pprint(create_new_contact_response.body["last_name"])
    pprint(create_new_contact_response.body["phone_number"])
    pprint(create_new_contact_response.body["time_zone"])
    pprint(create_new_contact_response.body["unsubscribed_at"])
    pprint(create_new_contact_response.body["last_notification_email_sent_at"])
    pprint(create_new_contact_response.body["fb_url"])
    pprint(create_new_contact_response.body["twitter_url"])
    pprint(create_new_contact_response.body["instagram_url"])
    pprint(create_new_contact_response.body["linkedin_url"])
    pprint(create_new_contact_response.body["website_url"])
    pprint(create_new_contact_response.body["created_at"])
    pprint(create_new_contact_response.body["updated_at"])
    pprint(create_new_contact_response.headers)
    pprint(create_new_contact_response.status)
    pprint(create_new_contact_response.round_trip_time)
except ApiException as e:
    print("Exception when calling ContactApi.create_new_contact: %s\n" % e)
    pprint(e.body)
    if e.status == 400:
        pprint(e.body["error"])
    if e.status == 401:
        pprint(e.body["error"])
    pprint(e.headers)
    pprint(e.status)
    pprint(e.reason)
    pprint(e.round_trip_time)
```


## Reference<a id="reference"></a>
### `clickfunnels.contact.create_new_contact`<a id="clickfunnelscontactcreate_new_contact"></a>

Add a new contact to the workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_contact_response = clickfunnels.contact.create_new_contact(
    workspace_id=1,
    contact={
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### contact: `ContactParameters`<a id="contact-contactparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ContactCreateNewContactRequest`](./click_funnels_python_sdk/type/contact_create_new_contact_request.py)
Information about a new Contact

#### 🔄 Return<a id="🔄-return"></a>

[`ContactAttributes`](./click_funnels_python_sdk/pydantic/contact_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/contacts` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.contact.get_contact_by_id`<a id="clickfunnelscontactget_contact_by_id"></a>

Retrieve a contact

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_contact_by_id_response = clickfunnels.contact.get_contact_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ContactAttributes`](./click_funnels_python_sdk/pydantic/contact_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/contacts/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.contact.list_for_workspace`<a id="clickfunnelscontactlist_for_workspace"></a>

List contacts for the given workspace. By default, only identified contacts are shown so you won&#39;t see anonymous or GDPR-redacted contacts.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_for_workspace_response = clickfunnels.contact.list_for_workspace(
    workspace_id=1,
    after="string_example",
    sort_order="asc",
    filter={
        "email_address": [
            "russel@clickfunnels.com,todd@clickfunnels.com"
        ],
        "id": [
            "142"
        ],
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

##### filter: [`Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`](./click_funnels_python_sdk/type/typing_dict_str_typing_union_bool_date_datetime_dict_float_int_list_str_none.py)<a id="filter-dictstr-unionbool-date-datetime-dict-float-int-list-str-noneclick_funnels_python_sdktypetyping_dict_str_typing_union_bool_date_datetime_dict_float_int_list_str_nonepy"></a>

Filtering  - Keep in mind that depending on the tools that you use, you might run into different situations where additional encoding is needed. For example:     - You might need to encode `filter[id]=1` as `filter%5Bid%5D=1` or use special options in your tools of choice to do it for you (like `g` in CURL).     -  Special URL characters like `%`, `+`, or unicode characters in emails (like Chinese characters) will need additional encoding.  

#### 🔄 Return<a id="🔄-return"></a>

[`ContactListForWorkspaceResponse`](./click_funnels_python_sdk/pydantic/contact_list_for_workspace_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/contacts` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.contact.redact_personally_identifiable`<a id="clickfunnelscontactredact_personally_identifiable"></a>

This will destroy all personally identifiable information for a contact, including their name and phone number. This cannot be undone.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
clickfunnels.contact.redact_personally_identifiable(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/contacts/{id}/gdpr_destroy` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.contact.remove_by_id`<a id="clickfunnelscontactremove_by_id"></a>

Delete a contact

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
clickfunnels.contact.remove_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/contacts/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.contact.update_contact_by_id`<a id="clickfunnelscontactupdate_contact_by_id"></a>

Update a contact

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_contact_by_id_response = clickfunnels.contact.update_contact_by_id(
    id="id_example",
    contact={
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### contact: `ContactParameters`<a id="contact-contactparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ContactUpdateContactByIdRequest`](./click_funnels_python_sdk/type/contact_update_contact_by_id_request.py)
Information about updated fields in Contact

#### 🔄 Return<a id="🔄-return"></a>

[`ContactAttributes`](./click_funnels_python_sdk/pydantic/contact_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/contacts/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.contact.upsert`<a id="clickfunnelscontactupsert"></a>

Creates or updates a Contact, matching on the email address. If the Contact does not exist, it will be created. If the Contact does exist, it will be updated. It is not possible to delete a Contact via this endpoint. It is not possible to reset properties of a Contact by passing empty values. E.g. passing `null` for `first_name` or an empty array for `tag_ids` won't update previous values. To do that you would instead need to use the `Update Contact` endpoint.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
upsert_response = clickfunnels.contact.upsert(
    workspace_id="workspace_id_example",
    contact={
        "email_address": None,
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `str`<a id="workspace_id-str"></a>

##### contact: [`ContactUpsertRequestContact`](./click_funnels_python_sdk/type/contact_upsert_request_contact.py)<a id="contact-contactupsertrequestcontactclick_funnels_python_sdktypecontact_upsert_request_contactpy"></a>


#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ContactUpsertRequest`](./click_funnels_python_sdk/type/contact_upsert_request.py)
Contact to create or update, matching on the email address. Note that properties of a Contact are not reset when passed empty values, e.g. passing `null` for `first_name` or an empty array for `tag_ids` won't update previous values. To do that you would instead use the `Update Contact` endpoint.

#### 🔄 Return<a id="🔄-return"></a>

[`ContactUpsertResponse`](./click_funnels_python_sdk/pydantic/contact_upsert_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/contacts/upsert` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.contacts::applied_tag.create_applied_tag`<a id="clickfunnelscontactsapplied_tagcreate_applied_tag"></a>

Assign a tag to a contact by creating an applied tag

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_applied_tag_response = clickfunnels.contacts::applied_tag.create_applied_tag(
    contact_id=1,
    contacts_applied_tag={
        "tag_id": 3,
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### contact_id: `int`<a id="contact_id-int"></a>

##### contacts_applied_tag: `ContactsAppliedTagParameters`<a id="contacts_applied_tag-contactsappliedtagparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ContactsAppliedTagCreateAppliedTagRequest`](./click_funnels_python_sdk/type/contacts_applied_tag_create_applied_tag_request.py)
Information about a new Applied Tag

#### 🔄 Return<a id="🔄-return"></a>

[`ContactsAppliedTagAttributes`](./click_funnels_python_sdk/pydantic/contacts_applied_tag_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/contacts/{contact_id}/applied_tags` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.contacts::applied_tag.get_for_contact`<a id="clickfunnelscontactsapplied_tagget_for_contact"></a>

Retrieve an applied tag for a contact

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_for_contact_response = clickfunnels.contacts::applied_tag.get_for_contact(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ContactsAppliedTagAttributes`](./click_funnels_python_sdk/pydantic/contacts_applied_tag_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/contacts/applied_tags/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.contacts::applied_tag.list`<a id="clickfunnelscontactsapplied_taglist"></a>

List the applied tags for a contact

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = clickfunnels.contacts::applied_tag.list(
    contact_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### contact_id: `int`<a id="contact_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`ContactsAppliedTagListResponse`](./click_funnels_python_sdk/pydantic/contacts_applied_tag_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/contacts/{contact_id}/applied_tags` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.contacts::applied_tag.remove_by_id`<a id="clickfunnelscontactsapplied_tagremove_by_id"></a>

Remove a tag from a contact by deleting an applied tag

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
clickfunnels.contacts::applied_tag.remove_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/contacts/applied_tags/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.contacts::tag.create_new_tag`<a id="clickfunnelscontactstagcreate_new_tag"></a>

Add a new Contact Tag to your Workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_tag_response = clickfunnels.contacts::tag.create_new_tag(
    workspace_id=1,
    contacts_tag={
        "name": "Example Tag",
        "color": "#044662",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### contacts_tag: `ContactsTagParameters`<a id="contacts_tag-contactstagparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ContactsTagCreateNewTagRequest`](./click_funnels_python_sdk/type/contacts_tag_create_new_tag_request.py)
Information about a new Tag

#### 🔄 Return<a id="🔄-return"></a>

[`ContactsTagAttributes`](./click_funnels_python_sdk/pydantic/contacts_tag_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/contacts/tags` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.contacts::tag.get_single`<a id="clickfunnelscontactstagget_single"></a>

Retrieve a single Contact Tag

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_single_response = clickfunnels.contacts::tag.get_single(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ContactsTagAttributes`](./click_funnels_python_sdk/pydantic/contacts_tag_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/contacts/tags/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.contacts::tag.list`<a id="clickfunnelscontactstaglist"></a>

List all Contact Tags for your workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = clickfunnels.contacts::tag.list(
    workspace_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`ContactsTagListResponse`](./click_funnels_python_sdk/pydantic/contacts_tag_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/contacts/tags` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.contacts::tag.remove`<a id="clickfunnelscontactstagremove"></a>

Delete a Contact Tag from your workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
clickfunnels.contacts::tag.remove(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/contacts/tags/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.contacts::tag.update_specific_tag`<a id="clickfunnelscontactstagupdate_specific_tag"></a>

Update a Contact Tag

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_specific_tag_response = clickfunnels.contacts::tag.update_specific_tag(
    id="id_example",
    contacts_tag={
        "name": "Example Tag",
        "color": "#044662",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### contacts_tag: `ContactsTagParameters`<a id="contacts_tag-contactstagparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ContactsTagUpdateSpecificTagRequest`](./click_funnels_python_sdk/type/contacts_tag_update_specific_tag_request.py)
Information about updated fields in Tag

#### 🔄 Return<a id="🔄-return"></a>

[`ContactsTagAttributes`](./click_funnels_python_sdk/pydantic/contacts_tag_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/contacts/tags/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.course.get_by_id`<a id="clickfunnelscourseget_by_id"></a>

Retrieve a course

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_by_id_response = clickfunnels.course.get_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`CourseAttributes`](./click_funnels_python_sdk/pydantic/course_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/courses/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.course.list_for_workspace`<a id="clickfunnelscourselist_for_workspace"></a>

List courses for a team

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_for_workspace_response = clickfunnels.course.list_for_workspace(
    workspace_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`CourseListForWorkspaceResponse`](./click_funnels_python_sdk/pydantic/course_list_for_workspace_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/courses` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.courses::enrollment.create_new_enrollment`<a id="clickfunnelscoursesenrollmentcreate_new_enrollment"></a>

Add a new enrollment

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_enrollment_response = clickfunnels.courses::enrollment.create_new_enrollment(
    course_id=1,
    courses_enrollment={
        "contact_id": 3,
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### course_id: `int`<a id="course_id-int"></a>

##### courses_enrollment: `CoursesEnrollmentParameters`<a id="courses_enrollment-coursesenrollmentparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CoursesEnrollmentCreateNewEnrollmentRequest`](./click_funnels_python_sdk/type/courses_enrollment_create_new_enrollment_request.py)
Information about a new Enrollment

#### 🔄 Return<a id="🔄-return"></a>

[`CoursesEnrollmentAttributes`](./click_funnels_python_sdk/pydantic/courses_enrollment_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/courses/{course_id}/enrollments` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.courses::enrollment.get_by_id`<a id="clickfunnelscoursesenrollmentget_by_id"></a>

Retrieve an enrollment

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_by_id_response = clickfunnels.courses::enrollment.get_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`CoursesEnrollmentAttributes`](./click_funnels_python_sdk/pydantic/courses_enrollment_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/courses/enrollments/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.courses::enrollment.list`<a id="clickfunnelscoursesenrollmentlist"></a>

List enrollments for a course

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = clickfunnels.courses::enrollment.list(
    course_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### course_id: `int`<a id="course_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`CoursesEnrollmentListResponse`](./click_funnels_python_sdk/pydantic/courses_enrollment_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/courses/{course_id}/enrollments` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.courses::enrollment.update_specific_enrollment`<a id="clickfunnelscoursesenrollmentupdate_specific_enrollment"></a>

Update an enrollment

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_specific_enrollment_response = clickfunnels.courses::enrollment.update_specific_enrollment(
    id="id_example",
    courses_enrollment={
        "contact_id": 3,
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### courses_enrollment: `CoursesEnrollmentParameters`<a id="courses_enrollment-coursesenrollmentparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CoursesEnrollmentUpdateSpecificEnrollmentRequest`](./click_funnels_python_sdk/type/courses_enrollment_update_specific_enrollment_request.py)
Information about updated fields in Enrollment

#### 🔄 Return<a id="🔄-return"></a>

[`CoursesEnrollmentAttributes`](./click_funnels_python_sdk/pydantic/courses_enrollment_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/courses/enrollments/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.courses::lesson.get_by_id`<a id="clickfunnelscourseslessonget_by_id"></a>

Fetch Lesson

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_by_id_response = clickfunnels.courses::lesson.get_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`CoursesLessonAttributes`](./click_funnels_python_sdk/pydantic/courses_lesson_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/courses/lessons/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.courses::lesson.list_lessons`<a id="clickfunnelscourseslessonlist_lessons"></a>

List Lessons

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_lessons_response = clickfunnels.courses::lesson.list_lessons(
    section_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### section_id: `int`<a id="section_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`CoursesLessonListLessonsResponse`](./click_funnels_python_sdk/pydantic/courses_lesson_list_lessons_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/courses/sections/{section_id}/lessons` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.courses::lesson.update_lesson_by_id`<a id="clickfunnelscourseslessonupdate_lesson_by_id"></a>

Update Lesson

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_lesson_by_id_response = clickfunnels.courses::lesson.update_lesson_by_id(
    id="id_example",
    courses_lesson={
        "title": "Lesson 1",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### courses_lesson: `CoursesLessonParameters`<a id="courses_lesson-courseslessonparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CoursesLessonUpdateLessonByIdRequest`](./click_funnels_python_sdk/type/courses_lesson_update_lesson_by_id_request.py)
Information about updated fields in Lesson

#### 🔄 Return<a id="🔄-return"></a>

[`CoursesLessonAttributes`](./click_funnels_python_sdk/pydantic/courses_lesson_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/courses/lessons/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.courses::section.get_section`<a id="clickfunnelscoursessectionget_section"></a>

Fetch Section

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_section_response = clickfunnels.courses::section.get_section(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`CoursesSectionAttributes`](./click_funnels_python_sdk/pydantic/courses_section_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/courses/sections/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.courses::section.list_sections`<a id="clickfunnelscoursessectionlist_sections"></a>

List Sections

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_sections_response = clickfunnels.courses::section.list_sections(
    course_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### course_id: `int`<a id="course_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`CoursesSectionListSectionsResponse`](./click_funnels_python_sdk/pydantic/courses_section_list_sections_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/courses/{course_id}/sections` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.courses::section.update_section_by_id`<a id="clickfunnelscoursessectionupdate_section_by_id"></a>

Update Section

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_section_by_id_response = clickfunnels.courses::section.update_section_by_id(
    id="id_example",
    courses_section={
        "title": "Module 1",
        "blocker_lesson_id": "blocker_lesson_id_example",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### courses_section: `CoursesSectionParameters`<a id="courses_section-coursessectionparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CoursesSectionUpdateSectionByIdRequest`](./click_funnels_python_sdk/type/courses_section_update_section_by_id_request.py)
Information about updated fields in Section

#### 🔄 Return<a id="🔄-return"></a>

[`CoursesSectionAttributes`](./click_funnels_python_sdk/pydantic/courses_section_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/courses/sections/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.form.create_new_form`<a id="clickfunnelsformcreate_new_form"></a>

Add a new form

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_form_response = clickfunnels.form.create_new_form(
    workspace_id=1,
    form={
        "name": "Example Form",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### form: `FormParameters`<a id="form-formparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FormCreateNewFormRequest`](./click_funnels_python_sdk/type/form_create_new_form_request.py)
Information about a new Form

#### 🔄 Return<a id="🔄-return"></a>

[`FormAttributes`](./click_funnels_python_sdk/pydantic/form_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/forms` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.form.get_form`<a id="clickfunnelsformget_form"></a>

Retrieve a form

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_form_response = clickfunnels.form.get_form(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`FormAttributes`](./click_funnels_python_sdk/pydantic/form_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.form.list_workspace_forms`<a id="clickfunnelsformlist_workspace_forms"></a>

List forms for a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_workspace_forms_response = clickfunnels.form.list_workspace_forms(
    workspace_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`FormListWorkspaceFormsResponse`](./click_funnels_python_sdk/pydantic/form_list_workspace_forms_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/forms` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.form.remove`<a id="clickfunnelsformremove"></a>

Delete a form

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
clickfunnels.form.remove(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.form.update_form_by_id`<a id="clickfunnelsformupdate_form_by_id"></a>

Update a form

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_form_by_id_response = clickfunnels.form.update_form_by_id(
    id="id_example",
    form={
        "name": "Example Form",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### form: `FormParameters`<a id="form-formparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FormUpdateFormByIdRequest`](./click_funnels_python_sdk/type/form_update_form_by_id_request.py)
Information about updated fields in Form

#### 🔄 Return<a id="🔄-return"></a>

[`FormAttributes`](./click_funnels_python_sdk/pydantic/form_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::field.add_new_field`<a id="clickfunnelsformsfieldadd_new_field"></a>

Add a new field

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
add_new_field_response = clickfunnels.forms::field.add_new_field(
    field_set_id=1,
    forms_field={
        "label": "MyString",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### field_set_id: `int`<a id="field_set_id-int"></a>

##### forms_field: `FormsFieldParameters`<a id="forms_field-formsfieldparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FormsFieldAddNewFieldRequest`](./click_funnels_python_sdk/type/forms_field_add_new_field_request.py)
Information about a new Field

#### 🔄 Return<a id="🔄-return"></a>

[`FormsFieldAttributes`](./click_funnels_python_sdk/pydantic/forms_field_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/field_sets/{field_set_id}/fields` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::field.get_field`<a id="clickfunnelsformsfieldget_field"></a>

Retrieve a field

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_field_response = clickfunnels.forms::field.get_field(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`FormsFieldAttributes`](./click_funnels_python_sdk/pydantic/forms_field_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/fields/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::field.list_fields_for_field_set`<a id="clickfunnelsformsfieldlist_fields_for_field_set"></a>

List fields for a field set

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_fields_for_field_set_response = clickfunnels.forms::field.list_fields_for_field_set(
    field_set_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### field_set_id: `int`<a id="field_set_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`FormsFieldListFieldsForFieldSetResponse`](./click_funnels_python_sdk/pydantic/forms_field_list_fields_for_field_set_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/field_sets/{field_set_id}/fields` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::field.remove_field`<a id="clickfunnelsformsfieldremove_field"></a>

Delete a field

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
clickfunnels.forms::field.remove_field(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/fields/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::field.update_field_by_id`<a id="clickfunnelsformsfieldupdate_field_by_id"></a>

Update a field

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_field_by_id_response = clickfunnels.forms::field.update_field_by_id(
    id="id_example",
    forms_field={
        "label": "MyString",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### forms_field: `FormsFieldParameters`<a id="forms_field-formsfieldparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FormsFieldUpdateFieldByIdRequest`](./click_funnels_python_sdk/type/forms_field_update_field_by_id_request.py)
Information about updated fields in Field

#### 🔄 Return<a id="🔄-return"></a>

[`FormsFieldAttributes`](./click_funnels_python_sdk/pydantic/forms_field_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/fields/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::field_set.create_new_field_set`<a id="clickfunnelsformsfield_setcreate_new_field_set"></a>

Add a new field set

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_field_set_response = clickfunnels.forms::field_set.create_new_field_set(
    form_id=1,
    forms_field_set={
        "title": "Example Field Set",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### form_id: `int`<a id="form_id-int"></a>

##### forms_field_set: `FormsFieldSetParameters`<a id="forms_field_set-formsfieldsetparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FormsFieldSetCreateNewFieldSetRequest`](./click_funnels_python_sdk/type/forms_field_set_create_new_field_set_request.py)
Information about a new Field Set

#### 🔄 Return<a id="🔄-return"></a>

[`FormsFieldSetAttributes`](./click_funnels_python_sdk/pydantic/forms_field_set_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/{form_id}/field_sets` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::field_set.get_field_set`<a id="clickfunnelsformsfield_setget_field_set"></a>

Retrieve a field set

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_field_set_response = clickfunnels.forms::field_set.get_field_set(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`FormsFieldSetAttributes`](./click_funnels_python_sdk/pydantic/forms_field_set_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/field_sets/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::field_set.list`<a id="clickfunnelsformsfield_setlist"></a>

List field sets for a form

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = clickfunnels.forms::field_set.list(
    form_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### form_id: `int`<a id="form_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`FormsFieldSetListResponse`](./click_funnels_python_sdk/pydantic/forms_field_set_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/{form_id}/field_sets` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::field_set.remove`<a id="clickfunnelsformsfield_setremove"></a>

Delete a field set

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
clickfunnels.forms::field_set.remove(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/field_sets/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::field_set.update_field_set_by_id`<a id="clickfunnelsformsfield_setupdate_field_set_by_id"></a>

Update a field set

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_field_set_by_id_response = clickfunnels.forms::field_set.update_field_set_by_id(
    id="id_example",
    forms_field_set={
        "title": "Example Field Set",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### forms_field_set: `FormsFieldSetParameters`<a id="forms_field_set-formsfieldsetparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FormsFieldSetUpdateFieldSetByIdRequest`](./click_funnels_python_sdk/type/forms_field_set_update_field_set_by_id_request.py)
Information about updated fields in Field Set

#### 🔄 Return<a id="🔄-return"></a>

[`FormsFieldSetAttributes`](./click_funnels_python_sdk/pydantic/forms_field_set_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/field_sets/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::fields::option.create_new_field_option`<a id="clickfunnelsformsfieldsoptioncreate_new_field_option"></a>

Add a new option to a field

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_field_option_response = clickfunnels.forms::fields::option.create_new_field_option(
    field_id=1,
    forms_fields_option={
        "label": "accusamus",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### field_id: `int`<a id="field_id-int"></a>

##### forms_fields_option: `FormsFieldsOptionParameters`<a id="forms_fields_option-formsfieldsoptionparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FormsFieldsOptionCreateNewFieldOptionRequest`](./click_funnels_python_sdk/type/forms_fields_option_create_new_field_option_request.py)
Information about a new Option

#### 🔄 Return<a id="🔄-return"></a>

[`FormsFieldsOptionAttributes`](./click_funnels_python_sdk/pydantic/forms_fields_option_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/fields/{field_id}/options` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::fields::option.delete_option_for_field`<a id="clickfunnelsformsfieldsoptiondelete_option_for_field"></a>

Delete a option for a field

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
clickfunnels.forms::fields::option.delete_option_for_field(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/fields/options/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::fields::option.get_field_option`<a id="clickfunnelsformsfieldsoptionget_field_option"></a>

Retrieve a option for a field

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_field_option_response = clickfunnels.forms::fields::option.get_field_option(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`FormsFieldsOptionAttributes`](./click_funnels_python_sdk/pydantic/forms_fields_option_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/fields/options/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::fields::option.list`<a id="clickfunnelsformsfieldsoptionlist"></a>

List options for a field

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = clickfunnels.forms::fields::option.list(
    field_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### field_id: `int`<a id="field_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`FormsFieldsOptionListResponse`](./click_funnels_python_sdk/pydantic/forms_fields_option_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/fields/{field_id}/options` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::fields::option.update_field_option`<a id="clickfunnelsformsfieldsoptionupdate_field_option"></a>

Update a option for a field

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_field_option_response = clickfunnels.forms::fields::option.update_field_option(
    id="id_example",
    forms_fields_option={
        "label": "accusamus",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### forms_fields_option: `FormsFieldsOptionParameters`<a id="forms_fields_option-formsfieldsoptionparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FormsFieldsOptionUpdateFieldOptionRequest`](./click_funnels_python_sdk/type/forms_fields_option_update_field_option_request.py)
Information about updated fields in Option

#### 🔄 Return<a id="🔄-return"></a>

[`FormsFieldsOptionAttributes`](./click_funnels_python_sdk/pydantic/forms_fields_option_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/fields/options/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::submission.create_new_submission`<a id="clickfunnelsformssubmissioncreate_new_submission"></a>

Add a new submission to a form

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_submission_response = clickfunnels.forms::submission.create_new_submission(
    form_id=1,
    forms_submission={
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### form_id: `int`<a id="form_id-int"></a>

##### forms_submission: `FormsSubmissionParameters`<a id="forms_submission-formssubmissionparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FormsSubmissionCreateNewSubmissionRequest`](./click_funnels_python_sdk/type/forms_submission_create_new_submission_request.py)
Information about a new Submission

#### 🔄 Return<a id="🔄-return"></a>

[`FormsSubmissionAttributes`](./click_funnels_python_sdk/pydantic/forms_submission_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/{form_id}/submissions` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::submission.get_by_id`<a id="clickfunnelsformssubmissionget_by_id"></a>

Retrieve a submission for a form

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_by_id_response = clickfunnels.forms::submission.get_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`FormsSubmissionAttributes`](./click_funnels_python_sdk/pydantic/forms_submission_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/submissions/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::submission.list`<a id="clickfunnelsformssubmissionlist"></a>

List submissions for a form

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = clickfunnels.forms::submission.list(
    form_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### form_id: `int`<a id="form_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`FormsSubmissionListResponse`](./click_funnels_python_sdk/pydantic/forms_submission_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/{form_id}/submissions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::submission.remove`<a id="clickfunnelsformssubmissionremove"></a>

Delete a submission for a form

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
clickfunnels.forms::submission.remove(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/submissions/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::submission.update_submission`<a id="clickfunnelsformssubmissionupdate_submission"></a>

Update a submission for a form

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_submission_response = clickfunnels.forms::submission.update_submission(
    id="id_example",
    forms_submission={
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### forms_submission: `FormsSubmissionParameters`<a id="forms_submission-formssubmissionparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FormsSubmissionUpdateSubmissionRequest`](./click_funnels_python_sdk/type/forms_submission_update_submission_request.py)
Information about updated fields in Submission

#### 🔄 Return<a id="🔄-return"></a>

[`FormsSubmissionAttributes`](./click_funnels_python_sdk/pydantic/forms_submission_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/submissions/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::submissions::answer.add_new_answer`<a id="clickfunnelsformssubmissionsansweradd_new_answer"></a>

Add a new answer to a submission

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
add_new_answer_response = clickfunnels.forms::submissions::answer.add_new_answer(
    submission_id=1,
    forms_submissions_answer={
        "field_id": 3,
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### submission_id: `int`<a id="submission_id-int"></a>

##### forms_submissions_answer: `FormsSubmissionsAnswerParameters`<a id="forms_submissions_answer-formssubmissionsanswerparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FormsSubmissionsAnswerAddNewAnswerRequest`](./click_funnels_python_sdk/type/forms_submissions_answer_add_new_answer_request.py)
Information about a new Answer

#### 🔄 Return<a id="🔄-return"></a>

[`FormsSubmissionsAnswerAttributes`](./click_funnels_python_sdk/pydantic/forms_submissions_answer_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/submissions/{submission_id}/answers` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::submissions::answer.get`<a id="clickfunnelsformssubmissionsanswerget"></a>

Retrieve a answer for a submission

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = clickfunnels.forms::submissions::answer.get(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`FormsSubmissionsAnswerAttributes`](./click_funnels_python_sdk/pydantic/forms_submissions_answer_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/submissions/answers/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::submissions::answer.list`<a id="clickfunnelsformssubmissionsanswerlist"></a>

List answers for a submission

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = clickfunnels.forms::submissions::answer.list(
    submission_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### submission_id: `int`<a id="submission_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`FormsSubmissionsAnswerListResponse`](./click_funnels_python_sdk/pydantic/forms_submissions_answer_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/submissions/{submission_id}/answers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::submissions::answer.remove_by_id`<a id="clickfunnelsformssubmissionsanswerremove_by_id"></a>

Delete a answer for a submission

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
clickfunnels.forms::submissions::answer.remove_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/submissions/answers/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.forms::submissions::answer.update_answer`<a id="clickfunnelsformssubmissionsanswerupdate_answer"></a>

Update a answer for a submission

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_answer_response = clickfunnels.forms::submissions::answer.update_answer(
    id="id_example",
    forms_submissions_answer={
        "field_id": 3,
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### forms_submissions_answer: `FormsSubmissionsAnswerParameters`<a id="forms_submissions_answer-formssubmissionsanswerparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FormsSubmissionsAnswerUpdateAnswerRequest`](./click_funnels_python_sdk/type/forms_submissions_answer_update_answer_request.py)
Information about updated fields in Answer

#### 🔄 Return<a id="🔄-return"></a>

[`FormsSubmissionsAnswerAttributes`](./click_funnels_python_sdk/pydantic/forms_submissions_answer_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/forms/submissions/answers/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.fulfillment.cancel_fulfillment`<a id="clickfunnelsfulfillmentcancel_fulfillment"></a>

This will cancel a Fulfillment. A Fulfillment can only be cancelled when it's in a "fulfilled" state. The "cancelled" state is final.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
cancel_fulfillment_response = clickfunnels.fulfillment.cancel_fulfillment(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`FulfillmentAttributes`](./click_funnels_python_sdk/pydantic/fulfillment_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/fulfillments/{id}/cancel` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.fulfillment.create`<a id="clickfunnelsfulfillmentcreate"></a>

Create Fulfillment

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = clickfunnels.fulfillment.create(
    workspace_id=1,
    fulfillment={
        "contact_id": 6,
        "location_id": 1,
        "included_orders_invoices_line_items_attributes": [
            {
            }
        ],
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### fulfillment: `FulfillmentParameters`<a id="fulfillment-fulfillmentparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FulfillmentCreateRequest`](./click_funnels_python_sdk/type/fulfillment_create_request.py)
Information about a new Fulfillment

#### 🔄 Return<a id="🔄-return"></a>

[`FulfillmentAttributes`](./click_funnels_python_sdk/pydantic/fulfillment_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/fulfillments` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.fulfillment.get_by_id`<a id="clickfunnelsfulfillmentget_by_id"></a>

Fetch Fulfillment

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_by_id_response = clickfunnels.fulfillment.get_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`FulfillmentAttributes`](./click_funnels_python_sdk/pydantic/fulfillment_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/fulfillments/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.fulfillment.list`<a id="clickfunnelsfulfillmentlist"></a>

List Fulfillments

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = clickfunnels.fulfillment.list(
    workspace_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`FulfillmentListResponse`](./click_funnels_python_sdk/pydantic/fulfillment_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/fulfillments` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.fulfillment.update_by_id`<a id="clickfunnelsfulfillmentupdate_by_id"></a>

Update Fulfillment

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_by_id_response = clickfunnels.fulfillment.update_by_id(
    id="id_example",
    fulfillment={
        "contact_id": 6,
        "location_id": 1,
        "included_orders_invoices_line_items_attributes": [
            {
            }
        ],
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### fulfillment: `FulfillmentParameters`<a id="fulfillment-fulfillmentparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FulfillmentUpdateByIdRequest`](./click_funnels_python_sdk/type/fulfillment_update_by_id_request.py)
Information about updated fields in Fulfillment

#### 🔄 Return<a id="🔄-return"></a>

[`FulfillmentAttributes`](./click_funnels_python_sdk/pydantic/fulfillment_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/fulfillments/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.fulfillments::location.create_new_location`<a id="clickfunnelsfulfillmentslocationcreate_new_location"></a>

Create Location

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_location_response = clickfunnels.fulfillments::location.create_new_location(
    workspace_id=1,
    fulfillments_location={
        "name": "Example Location",
        "address_name": "Example Address",
        "email_address": "myemail1710866918@example.com",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### fulfillments_location: `FulfillmentsLocationParameters`<a id="fulfillments_location-fulfillmentslocationparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FulfillmentsLocationCreateNewLocationRequest`](./click_funnels_python_sdk/type/fulfillments_location_create_new_location_request.py)
Information about a new Location

#### 🔄 Return<a id="🔄-return"></a>

[`FulfillmentsLocationAttributes`](./click_funnels_python_sdk/pydantic/fulfillments_location_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/fulfillments/locations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.fulfillments::location.get_by_id`<a id="clickfunnelsfulfillmentslocationget_by_id"></a>

Fetch Location

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_by_id_response = clickfunnels.fulfillments::location.get_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`FulfillmentsLocationAttributes`](./click_funnels_python_sdk/pydantic/fulfillments_location_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/fulfillments/locations/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.fulfillments::location.list`<a id="clickfunnelsfulfillmentslocationlist"></a>

List Locations

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = clickfunnels.fulfillments::location.list(
    workspace_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`FulfillmentsLocationListResponse`](./click_funnels_python_sdk/pydantic/fulfillments_location_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/fulfillments/locations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.fulfillments::location.remove_by_id`<a id="clickfunnelsfulfillmentslocationremove_by_id"></a>

Remove Location

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
clickfunnels.fulfillments::location.remove_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/fulfillments/locations/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.fulfillments::location.update_by_id`<a id="clickfunnelsfulfillmentslocationupdate_by_id"></a>

Update Location

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_by_id_response = clickfunnels.fulfillments::location.update_by_id(
    id="id_example",
    fulfillments_location={
        "name": "Example Location",
        "address_name": "Example Address",
        "email_address": "myemail1710866918@example.com",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### fulfillments_location: `FulfillmentsLocationParameters`<a id="fulfillments_location-fulfillmentslocationparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FulfillmentsLocationUpdateByIdRequest`](./click_funnels_python_sdk/type/fulfillments_location_update_by_id_request.py)
Information about updated fields in Location

#### 🔄 Return<a id="🔄-return"></a>

[`FulfillmentsLocationAttributes`](./click_funnels_python_sdk/pydantic/fulfillments_location_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/fulfillments/locations/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.image.create`<a id="clickfunnelsimagecreate"></a>

Create Image

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = clickfunnels.image.create(
    workspace_id=1,
    image={
        "upload_source_url": "https://image-hosting-x.com/cdn/123",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### image: `ImageParameters`<a id="image-imageparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ImageCreateRequest`](./click_funnels_python_sdk/type/image_create_request.py)
Information about a new Image

#### 🔄 Return<a id="🔄-return"></a>

[`ImageAttributes`](./click_funnels_python_sdk/pydantic/image_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/images` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.image.get_by_id`<a id="clickfunnelsimageget_by_id"></a>

Fetch Image

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_by_id_response = clickfunnels.image.get_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ImageAttributes`](./click_funnels_python_sdk/pydantic/image_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/images/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.image.list`<a id="clickfunnelsimagelist"></a>

List Images

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = clickfunnels.image.list(
    workspace_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`ImageListResponse`](./click_funnels_python_sdk/pydantic/image_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/images` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.image.remove_by_id`<a id="clickfunnelsimageremove_by_id"></a>

Remove Image

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
clickfunnels.image.remove_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/images/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.image.update_by_id`<a id="clickfunnelsimageupdate_by_id"></a>

Update Image

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_by_id_response = clickfunnels.image.update_by_id(
    id="id_example",
    image={
        "upload_source_url": "https://image-hosting-x.com/cdn/123",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### image: `ImageParameters`<a id="image-imageparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ImageUpdateByIdRequest`](./click_funnels_python_sdk/type/image_update_by_id_request.py)
Information about updated fields in Image

#### 🔄 Return<a id="🔄-return"></a>

[`ImageAttributes`](./click_funnels_python_sdk/pydantic/image_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/images/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.order.get_single`<a id="clickfunnelsorderget_single"></a>

Retrieve a specific order in the current workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_single_response = clickfunnels.order.get_single(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`OrderAttributes`](./click_funnels_python_sdk/pydantic/order_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/orders/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.order.list_orders`<a id="clickfunnelsorderlist_orders"></a>

List all orders for the current workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_orders_response = clickfunnels.order.list_orders(
    workspace_id=1,
    after="string_example",
    sort_order="asc",
    filter={
        "contact_id": [
            "142"
        ],
        "id": [
            "142"
        ],
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

##### filter: [`Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`](./click_funnels_python_sdk/type/typing_dict_str_typing_union_bool_date_datetime_dict_float_int_list_str_none.py)<a id="filter-dictstr-unionbool-date-datetime-dict-float-int-list-str-noneclick_funnels_python_sdktypetyping_dict_str_typing_union_bool_date_datetime_dict_float_int_list_str_nonepy"></a>

Filtering  - Keep in mind that depending on the tools that you use, you might run into different situations where additional encoding is needed. For example:     - You might need to encode `filter[id]=1` as `filter%5Bid%5D=1` or use special options in your tools of choice to do it for you (like `g` in CURL).     -  Special URL characters like `%`, `+`, or unicode characters in emails (like Chinese characters) will need additional encoding.  

#### 🔄 Return<a id="🔄-return"></a>

[`OrderListOrdersResponse`](./click_funnels_python_sdk/pydantic/order_list_orders_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/orders` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.order.update_specific`<a id="clickfunnelsorderupdate_specific"></a>

Update a specific order in the current workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_specific_response = clickfunnels.order.update_specific(
    id="id_example",
    order={
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### order: `OrderParameters`<a id="order-orderparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`OrderUpdateSpecificRequest`](./click_funnels_python_sdk/type/order_update_specific_request.py)
Information about updated fields in Order

#### 🔄 Return<a id="🔄-return"></a>

[`OrderAttributes`](./click_funnels_python_sdk/pydantic/order_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/orders/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.orders::applied_tag.create_applied_tag`<a id="clickfunnelsordersapplied_tagcreate_applied_tag"></a>

Assign a tag to an order by creating an applied tag

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_applied_tag_response = clickfunnels.orders::applied_tag.create_applied_tag(
    order_id=1,
    orders_applied_tag={
        "tag_id": 4,
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### order_id: `int`<a id="order_id-int"></a>

##### orders_applied_tag: `OrdersAppliedTagParameters`<a id="orders_applied_tag-ordersappliedtagparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`OrdersAppliedTagCreateAppliedTagRequest`](./click_funnels_python_sdk/type/orders_applied_tag_create_applied_tag_request.py)
Information about a new Applied Tag

#### 🔄 Return<a id="🔄-return"></a>

[`OrdersAppliedTagAttributes`](./click_funnels_python_sdk/pydantic/orders_applied_tag_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/orders/{order_id}/applied_tags` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.orders::applied_tag.get`<a id="clickfunnelsordersapplied_tagget"></a>

Retrieve an applied tag for an order

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = clickfunnels.orders::applied_tag.get(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`OrdersAppliedTagAttributes`](./click_funnels_python_sdk/pydantic/orders_applied_tag_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/orders/applied_tags/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.orders::applied_tag.list`<a id="clickfunnelsordersapplied_taglist"></a>

List the applied tags for an order

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = clickfunnels.orders::applied_tag.list(
    order_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### order_id: `int`<a id="order_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`OrdersAppliedTagListResponse`](./click_funnels_python_sdk/pydantic/orders_applied_tag_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/orders/{order_id}/applied_tags` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.orders::applied_tag.remove_by_id`<a id="clickfunnelsordersapplied_tagremove_by_id"></a>

Remove a tag from an order by deleting an applied tag

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
clickfunnels.orders::applied_tag.remove_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/orders/applied_tags/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.orders::invoice.get_for_order`<a id="clickfunnelsordersinvoiceget_for_order"></a>

Retrieve an invoice for an order

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_for_order_response = clickfunnels.orders::invoice.get_for_order(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`OrdersInvoiceAttributes`](./click_funnels_python_sdk/pydantic/orders_invoice_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/orders/invoices/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.orders::invoice.list_for_order`<a id="clickfunnelsordersinvoicelist_for_order"></a>

List invoices for an order

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_for_order_response = clickfunnels.orders::invoice.list_for_order(
    order_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### order_id: `int`<a id="order_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`OrdersInvoiceListForOrderResponse`](./click_funnels_python_sdk/pydantic/orders_invoice_list_for_order_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/orders/{order_id}/invoices` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.orders::invoices::restock.get_restock`<a id="clickfunnelsordersinvoicesrestockget_restock"></a>

Fetch Restock

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_restock_response = clickfunnels.orders::invoices::restock.get_restock(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`OrdersInvoicesRestockGetRestockResponse`](./click_funnels_python_sdk/pydantic/orders_invoices_restock_get_restock_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/orders/invoices/restocks/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.orders::invoices::restock.list_restocks`<a id="clickfunnelsordersinvoicesrestocklist_restocks"></a>

List Restocks

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_restocks_response = clickfunnels.orders::invoices::restock.list_restocks(
    workspace_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`OrdersInvoicesRestockListRestocksResponse`](./click_funnels_python_sdk/pydantic/orders_invoices_restock_list_restocks_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/orders/invoices/restocks` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.orders::tag.create_new_tag`<a id="clickfunnelsorderstagcreate_new_tag"></a>

Add a new order tag to your workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_tag_response = clickfunnels.orders::tag.create_new_tag(
    workspace_id=1,
    orders_tag={
        "name": "Example Tag",
        "color": "#4f4ca7",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### orders_tag: `OrdersTagParameters`<a id="orders_tag-orderstagparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`OrdersTagCreateNewTagRequest`](./click_funnels_python_sdk/type/orders_tag_create_new_tag_request.py)
Information about a new Tag

#### 🔄 Return<a id="🔄-return"></a>

[`OrdersTagAttributes`](./click_funnels_python_sdk/pydantic/orders_tag_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/orders/tags` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.orders::tag.get_single`<a id="clickfunnelsorderstagget_single"></a>

Retrieve a single order tag

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_single_response = clickfunnels.orders::tag.get_single(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`OrdersTagAttributes`](./click_funnels_python_sdk/pydantic/orders_tag_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/orders/tags/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.orders::tag.list`<a id="clickfunnelsorderstaglist"></a>

List all order tags for your workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = clickfunnels.orders::tag.list(
    workspace_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`OrdersTagListResponse`](./click_funnels_python_sdk/pydantic/orders_tag_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/orders/tags` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.orders::tag.remove`<a id="clickfunnelsorderstagremove"></a>

Delete an order tag from your workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
clickfunnels.orders::tag.remove(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/orders/tags/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.orders::tag.update_specific_order_tag`<a id="clickfunnelsorderstagupdate_specific_order_tag"></a>

Update an order tag

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_specific_order_tag_response = clickfunnels.orders::tag.update_specific_order_tag(
    id="id_example",
    orders_tag={
        "name": "Example Tag",
        "color": "#4f4ca7",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### orders_tag: `OrdersTagParameters`<a id="orders_tag-orderstagparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`OrdersTagUpdateSpecificOrderTagRequest`](./click_funnels_python_sdk/type/orders_tag_update_specific_order_tag_request.py)
Information about updated fields in Tag

#### 🔄 Return<a id="🔄-return"></a>

[`OrdersTagAttributes`](./click_funnels_python_sdk/pydantic/orders_tag_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/orders/tags/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.orders::transaction.get_by_id`<a id="clickfunnelsorderstransactionget_by_id"></a>

Retrieve a transaction for an order

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_by_id_response = clickfunnels.orders::transaction.get_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`OrdersTransactionAttributes`](./click_funnels_python_sdk/pydantic/orders_transaction_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/orders/transactions/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.orders::transaction.get_list`<a id="clickfunnelsorderstransactionget_list"></a>

List transactions for an order

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_list_response = clickfunnels.orders::transaction.get_list(
    order_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### order_id: `int`<a id="order_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`OrdersTransactionGetListResponse`](./click_funnels_python_sdk/pydantic/orders_transaction_get_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/orders/{order_id}/transactions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.product.add_new_to_workspace`<a id="clickfunnelsproductadd_new_to_workspace"></a>

Add a new product to a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
add_new_to_workspace_response = clickfunnels.product.add_new_to_workspace(
    workspace_id=1,
    product={
        "name": "Small Steel Bottle 41972f",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### product: `ProductParameters`<a id="product-productparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ProductAddNewToWorkspaceRequest`](./click_funnels_python_sdk/type/product_add_new_to_workspace_request.py)
Information about a new Product

#### 🔄 Return<a id="🔄-return"></a>

[`ProductAttributes`](./click_funnels_python_sdk/pydantic/product_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/products` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.product.archive_product`<a id="clickfunnelsproductarchive_product"></a>

This will archive a Product. A product can only be archived if it's not in the "live" state.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
archive_product_response = clickfunnels.product.archive_product(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ProductAttributes`](./click_funnels_python_sdk/pydantic/product_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/products/{id}/archive` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.product.get_for_workspace`<a id="clickfunnelsproductget_for_workspace"></a>

Retrieve a product for a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_for_workspace_response = clickfunnels.product.get_for_workspace(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ProductAttributes`](./click_funnels_python_sdk/pydantic/product_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/products/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.product.list_for_workspace`<a id="clickfunnelsproductlist_for_workspace"></a>

List products for a workspace. All products are listed regardless of `archived` state.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_for_workspace_response = clickfunnels.product.list_for_workspace(
    workspace_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`ProductListForWorkspaceResponse`](./click_funnels_python_sdk/pydantic/product_list_for_workspace_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/products` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.product.unarchive_by_id`<a id="clickfunnelsproductunarchive_by_id"></a>

This will unarchive a Product.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
unarchive_by_id_response = clickfunnels.product.unarchive_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ProductAttributes`](./click_funnels_python_sdk/pydantic/product_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/products/{id}/unarchive` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.product.update_for_workspace`<a id="clickfunnelsproductupdate_for_workspace"></a>

Update a product for a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_for_workspace_response = clickfunnels.product.update_for_workspace(
    id="id_example",
    product={
        "name": "Small Steel Bottle 41972f",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### product: `ProductParameters`<a id="product-productparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ProductUpdateForWorkspaceRequest`](./click_funnels_python_sdk/type/product_update_for_workspace_request.py)
Information about updated fields in Product

#### 🔄 Return<a id="🔄-return"></a>

[`ProductAttributes`](./click_funnels_python_sdk/pydantic/product_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/products/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.products::price.create_variant_price`<a id="clickfunnelsproductspricecreate_variant_price"></a>

Create a new price for a given variant

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_variant_price_response = clickfunnels.products::price.create_variant_price(
    product_id=1,
    products_price={
        "amount": "100.00",
        "currency": "USD",
        "duration": 1,
        "interval": "months",
        "trial_interval": "trial_interval_example",
        "trial_duration": "trial_duration_example",
        "trial_amount": "0.00",
        "interval_count": 1,
        "payment_type": "one_time",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### product_id: `int`<a id="product_id-int"></a>

##### products_price: `ProductsPriceParameters`<a id="products_price-productspriceparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ProductsPriceCreateVariantPriceRequest`](./click_funnels_python_sdk/type/products_price_create_variant_price_request.py)
Information about a new Price

#### 🔄 Return<a id="🔄-return"></a>

[`ProductsPriceAttributes`](./click_funnels_python_sdk/pydantic/products_price_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/products/{product_id}/prices` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.products::price.get_single_price`<a id="clickfunnelsproductspriceget_single_price"></a>

Retrieve a single price

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_single_price_response = clickfunnels.products::price.get_single_price(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ProductsPriceAttributes`](./click_funnels_python_sdk/pydantic/products_price_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/products/prices/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.products::price.list_for_variant`<a id="clickfunnelsproductspricelist_for_variant"></a>

List all prices for a given variant

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_for_variant_response = clickfunnels.products::price.list_for_variant(
    product_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### product_id: `int`<a id="product_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`ProductsPriceListForVariantResponse`](./click_funnels_python_sdk/pydantic/products_price_list_for_variant_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/products/{product_id}/prices` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.products::price.update_single_price`<a id="clickfunnelsproductspriceupdate_single_price"></a>

Update a single price

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_single_price_response = clickfunnels.products::price.update_single_price(
    id="id_example",
    products_price={
        "amount": "100.00",
        "currency": "USD",
        "duration": 1,
        "interval": "months",
        "trial_interval": "trial_interval_example",
        "trial_duration": "trial_duration_example",
        "trial_amount": "0.00",
        "interval_count": 1,
        "payment_type": "one_time",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### products_price: `ProductsPriceParameters`<a id="products_price-productspriceparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ProductsPriceUpdateSinglePriceRequest`](./click_funnels_python_sdk/type/products_price_update_single_price_request.py)
Information about updated fields in Price

#### 🔄 Return<a id="🔄-return"></a>

[`ProductsPriceAttributes`](./click_funnels_python_sdk/pydantic/products_price_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/products/prices/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.products::tag.create_new_tag`<a id="clickfunnelsproductstagcreate_new_tag"></a>

Add a new tag to a product

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_tag_response = clickfunnels.products::tag.create_new_tag(
    workspace_id=1,
    products_tag={
        "name": "Example Tag",
        "color": "emerald",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### products_tag: `ProductsTagParameters`<a id="products_tag-productstagparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ProductsTagCreateNewTagRequest`](./click_funnels_python_sdk/type/products_tag_create_new_tag_request.py)
Information about a new Tag

#### 🔄 Return<a id="🔄-return"></a>

[`ProductsTagAttributes`](./click_funnels_python_sdk/pydantic/products_tag_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/products/tags` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.products::tag.delete_tag_by_id`<a id="clickfunnelsproductstagdelete_tag_by_id"></a>

Delete a tag for a product

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
clickfunnels.products::tag.delete_tag_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/products/tags/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.products::tag.get_tag_by_id`<a id="clickfunnelsproductstagget_tag_by_id"></a>

Retrieve a tag for a product

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_tag_by_id_response = clickfunnels.products::tag.get_tag_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ProductsTagAttributes`](./click_funnels_python_sdk/pydantic/products_tag_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/products/tags/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.products::tag.list`<a id="clickfunnelsproductstaglist"></a>

List tags for a product

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = clickfunnels.products::tag.list(
    workspace_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`ProductsTagListResponse`](./click_funnels_python_sdk/pydantic/products_tag_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/products/tags` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.products::tag.update_tag_by_id`<a id="clickfunnelsproductstagupdate_tag_by_id"></a>

Update a tag for a product

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_tag_by_id_response = clickfunnels.products::tag.update_tag_by_id(
    id="id_example",
    products_tag={
        "name": "Example Tag",
        "color": "emerald",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### products_tag: `ProductsTagParameters`<a id="products_tag-productstagparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ProductsTagUpdateTagByIdRequest`](./click_funnels_python_sdk/type/products_tag_update_tag_by_id_request.py)
Information about updated fields in Tag

#### 🔄 Return<a id="🔄-return"></a>

[`ProductsTagAttributes`](./click_funnels_python_sdk/pydantic/products_tag_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/products/tags/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.products::variant.create_new_variant`<a id="clickfunnelsproductsvariantcreate_new_variant"></a>

Create a new variant for a product

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_variant_response = clickfunnels.products::variant.create_new_variant(
    product_id=1,
    products_variant={
        "name": "Lightweight Bronze Clock variant e702",
        "product_type": "physical",
        "weight_unit": "lb",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### product_id: `int`<a id="product_id-int"></a>

##### products_variant: `ProductsVariantParameters`<a id="products_variant-productsvariantparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ProductsVariantCreateNewVariantRequest`](./click_funnels_python_sdk/type/products_variant_create_new_variant_request.py)
Information about a new Variant

#### 🔄 Return<a id="🔄-return"></a>

[`ProductsVariantAttributes`](./click_funnels_python_sdk/pydantic/products_variant_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/products/{product_id}/variants` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.products::variant.get_single`<a id="clickfunnelsproductsvariantget_single"></a>

Retrieve a single variant

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_single_response = clickfunnels.products::variant.get_single(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ProductsVariantAttributes`](./click_funnels_python_sdk/pydantic/products_variant_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/products/variants/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.products::variant.list`<a id="clickfunnelsproductsvariantlist"></a>

List variants for a product

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = clickfunnels.products::variant.list(
    product_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### product_id: `int`<a id="product_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`ProductsVariantListResponse`](./click_funnels_python_sdk/pydantic/products_variant_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/products/{product_id}/variants` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.products::variant.update_single`<a id="clickfunnelsproductsvariantupdate_single"></a>

Update a single variant

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_single_response = clickfunnels.products::variant.update_single(
    id="id_example",
    products_variant={
        "name": "Lightweight Bronze Clock variant e702",
        "product_type": "physical",
        "weight_unit": "lb",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### products_variant: `ProductsVariantParameters`<a id="products_variant-productsvariantparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ProductsVariantUpdateSingleRequest`](./click_funnels_python_sdk/type/products_variant_update_single_request.py)
Information about updated fields in Variant

#### 🔄 Return<a id="🔄-return"></a>

[`ProductsVariantAttributes`](./click_funnels_python_sdk/pydantic/products_variant_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/products/variants/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::location_group.get_profile_location_group`<a id="clickfunnelsshippinglocation_groupget_profile_location_group"></a>

Retrieve a location group for a profile

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_profile_location_group_response = clickfunnels.shipping::location_group.get_profile_location_group(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingLocationGroupAttributes`](./click_funnels_python_sdk/pydantic/shipping_location_group_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/shipping/location_groups/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::location_group.list`<a id="clickfunnelsshippinglocation_grouplist"></a>

List location groups for a profile

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = clickfunnels.shipping::location_group.list(
    profile_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### profile_id: `int`<a id="profile_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingLocationGroupListResponse`](./click_funnels_python_sdk/pydantic/shipping_location_group_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/shipping/profiles/{profile_id}/location_groups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::package.add_to_workspace`<a id="clickfunnelsshippingpackageadd_to_workspace"></a>

Add a new package to a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
add_to_workspace_response = clickfunnels.shipping::package.add_to_workspace(
    workspace_id=1,
    shipping_package={
        "package_type": "box",
        "height": 4.0,
        "width": 2.0,
        "length": 2.0,
        "distance_unit": "in",
        "weight_unit": "lb",
        "name": "Example Package",
        "carrier": "fedex",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### shipping_package: `ShippingPackageParameters`<a id="shipping_package-shippingpackageparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ShippingPackageAddToWorkspaceRequest`](./click_funnels_python_sdk/type/shipping_package_add_to_workspace_request.py)
Information about a new Package

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingPackageAttributes`](./click_funnels_python_sdk/pydantic/shipping_package_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/shipping/packages` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::package.get_for_workspace`<a id="clickfunnelsshippingpackageget_for_workspace"></a>

Retrieve a package for a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_for_workspace_response = clickfunnels.shipping::package.get_for_workspace(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingPackageAttributes`](./click_funnels_python_sdk/pydantic/shipping_package_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/shipping/packages/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::package.list_for_workspace`<a id="clickfunnelsshippingpackagelist_for_workspace"></a>

List packages for a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_for_workspace_response = clickfunnels.shipping::package.list_for_workspace(
    workspace_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingPackageListForWorkspaceResponse`](./click_funnels_python_sdk/pydantic/shipping_package_list_for_workspace_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/shipping/packages` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::package.remove_by_id`<a id="clickfunnelsshippingpackageremove_by_id"></a>

Delete a package for a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
clickfunnels.shipping::package.remove_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/shipping/packages/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::package.update_for_workspace`<a id="clickfunnelsshippingpackageupdate_for_workspace"></a>

Update a package for a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_for_workspace_response = clickfunnels.shipping::package.update_for_workspace(
    id="id_example",
    shipping_package={
        "package_type": "box",
        "height": 4.0,
        "width": 2.0,
        "length": 2.0,
        "distance_unit": "in",
        "weight_unit": "lb",
        "name": "Example Package",
        "carrier": "fedex",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### shipping_package: `ShippingPackageParameters`<a id="shipping_package-shippingpackageparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ShippingPackageUpdateForWorkspaceRequest`](./click_funnels_python_sdk/type/shipping_package_update_for_workspace_request.py)
Information about updated fields in Package

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingPackageAttributes`](./click_funnels_python_sdk/pydantic/shipping_package_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/shipping/packages/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::profile.create_new`<a id="clickfunnelsshippingprofilecreate_new"></a>

Add a new shipping profile to a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_response = clickfunnels.shipping::profile.create_new(
    workspace_id=1,
    shipping_profile={
        "name": "Example Shipping Profile",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### shipping_profile: `ShippingProfileParameters`<a id="shipping_profile-shippingprofileparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ShippingProfileCreateNewRequest`](./click_funnels_python_sdk/type/shipping_profile_create_new_request.py)
Information about a new Profile

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingProfileAttributes`](./click_funnels_python_sdk/pydantic/shipping_profile_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/shipping/profiles` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::profile.get_workspace_profile`<a id="clickfunnelsshippingprofileget_workspace_profile"></a>

Retrieve a shipping profile for a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_workspace_profile_response = clickfunnels.shipping::profile.get_workspace_profile(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingProfileAttributes`](./click_funnels_python_sdk/pydantic/shipping_profile_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/shipping/profiles/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::profile.list`<a id="clickfunnelsshippingprofilelist"></a>

List shipping profiles for a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = clickfunnels.shipping::profile.list(
    workspace_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingProfileListResponse`](./click_funnels_python_sdk/pydantic/shipping_profile_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/shipping/profiles` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::profile.remove`<a id="clickfunnelsshippingprofileremove"></a>

Delete a shipping profile for a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
clickfunnels.shipping::profile.remove(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/shipping/profiles/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::profile.update_for_workspace`<a id="clickfunnelsshippingprofileupdate_for_workspace"></a>

Update a shipping profile for a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_for_workspace_response = clickfunnels.shipping::profile.update_for_workspace(
    id="id_example",
    shipping_profile={
        "name": "Example Shipping Profile",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### shipping_profile: `ShippingProfileParameters`<a id="shipping_profile-shippingprofileparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ShippingProfileUpdateForWorkspaceRequest`](./click_funnels_python_sdk/type/shipping_profile_update_for_workspace_request.py)
Information about updated fields in Profile

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingProfileAttributes`](./click_funnels_python_sdk/pydantic/shipping_profile_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/shipping/profiles/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::rate.create_rate_for_zone`<a id="clickfunnelsshippingratecreate_rate_for_zone"></a>

Add a new shipping rate to a zone

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_rate_for_zone_response = clickfunnels.shipping::rate.create_rate_for_zone(
    zone_id=1,
    shipping_rate={
        "price": "10.00",
        "price_currency": "USD",
        "rates_name_id": 1,
        "live_rates_provider": "Shippo",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### zone_id: `int`<a id="zone_id-int"></a>

##### shipping_rate: `ShippingRateParameters`<a id="shipping_rate-shippingrateparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ShippingRateCreateRateForZoneRequest`](./click_funnels_python_sdk/type/shipping_rate_create_rate_for_zone_request.py)
Information about a new Rate

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingRateAttributes`](./click_funnels_python_sdk/pydantic/shipping_rate_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/shipping/zones/{zone_id}/rates` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::rate.get_rate_by_id`<a id="clickfunnelsshippingrateget_rate_by_id"></a>

Retrieve a shipping rate for a zone

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_rate_by_id_response = clickfunnels.shipping::rate.get_rate_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingRateAttributes`](./click_funnels_python_sdk/pydantic/shipping_rate_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/shipping/rates/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::rate.list_for_zone`<a id="clickfunnelsshippingratelist_for_zone"></a>

List shipping rates for a zone

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_for_zone_response = clickfunnels.shipping::rate.list_for_zone(
    zone_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### zone_id: `int`<a id="zone_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingRateListForZoneResponse`](./click_funnels_python_sdk/pydantic/shipping_rate_list_for_zone_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/shipping/zones/{zone_id}/rates` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::rate.remove_by_id`<a id="clickfunnelsshippingrateremove_by_id"></a>

Delete a shipping rate for a zone

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
clickfunnels.shipping::rate.remove_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/shipping/rates/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::rate.update_rate_for_zone`<a id="clickfunnelsshippingrateupdate_rate_for_zone"></a>

Update a shipping rate for a zone

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_rate_for_zone_response = clickfunnels.shipping::rate.update_rate_for_zone(
    id="id_example",
    shipping_rate={
        "price": "10.00",
        "price_currency": "USD",
        "rates_name_id": 1,
        "live_rates_provider": "Shippo",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### shipping_rate: `ShippingRateParameters`<a id="shipping_rate-shippingrateparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ShippingRateUpdateRateForZoneRequest`](./click_funnels_python_sdk/type/shipping_rate_update_rate_for_zone_request.py)
Information about updated fields in Rate

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingRateAttributes`](./click_funnels_python_sdk/pydantic/shipping_rate_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/shipping/rates/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::rates::name.create_new_rate_name`<a id="clickfunnelsshippingratesnamecreate_new_rate_name"></a>

Add a new rate name to a shipping profile

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_rate_name_response = clickfunnels.shipping::rates::name.create_new_rate_name(
    workspace_id=1,
    shipping_rates_name={
        "name": "Example Shipping Rates Name",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### shipping_rates_name: `ShippingRatesNameParameters`<a id="shipping_rates_name-shippingratesnameparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ShippingRatesNameCreateNewRateNameRequest`](./click_funnels_python_sdk/type/shipping_rates_name_create_new_rate_name_request.py)
Information about a new Name

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingRatesNameAttributes`](./click_funnels_python_sdk/pydantic/shipping_rates_name_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/shipping/rates/names` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::rates::name.get_rate_name`<a id="clickfunnelsshippingratesnameget_rate_name"></a>

Retrieve a rate name for a shipping profile

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_rate_name_response = clickfunnels.shipping::rates::name.get_rate_name(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingRatesNameAttributes`](./click_funnels_python_sdk/pydantic/shipping_rates_name_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/shipping/rates/names/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::rates::name.list`<a id="clickfunnelsshippingratesnamelist"></a>

List rate names for a shipping profile

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = clickfunnels.shipping::rates::name.list(
    workspace_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingRatesNameListResponse`](./click_funnels_python_sdk/pydantic/shipping_rates_name_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/shipping/rates/names` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::rates::name.remove`<a id="clickfunnelsshippingratesnameremove"></a>

Delete a rate name for a shipping profile

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
clickfunnels.shipping::rates::name.remove(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/shipping/rates/names/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::rates::name.update_name`<a id="clickfunnelsshippingratesnameupdate_name"></a>

Update a rate name for a shipping profile

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_name_response = clickfunnels.shipping::rates::name.update_name(
    id="id_example",
    shipping_rates_name={
        "name": "Example Shipping Rates Name",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### shipping_rates_name: `ShippingRatesNameParameters`<a id="shipping_rates_name-shippingratesnameparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ShippingRatesNameUpdateNameRequest`](./click_funnels_python_sdk/type/shipping_rates_name_update_name_request.py)
Information about updated fields in Name

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingRatesNameAttributes`](./click_funnels_python_sdk/pydantic/shipping_rates_name_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/shipping/rates/names/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::zone.add_new_zone`<a id="clickfunnelsshippingzoneadd_new_zone"></a>

Add a new zone to a location group

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
add_new_zone_response = clickfunnels.shipping::zone.add_new_zone(
    location_group_id=1,
    shipping_zone={
        "name": "Bruce Marquardt",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### location_group_id: `int`<a id="location_group_id-int"></a>

##### shipping_zone: `ShippingZoneParameters`<a id="shipping_zone-shippingzoneparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ShippingZoneAddNewZoneRequest`](./click_funnels_python_sdk/type/shipping_zone_add_new_zone_request.py)
Information about a new Zone

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingZoneAttributes`](./click_funnels_python_sdk/pydantic/shipping_zone_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/shipping/location_groups/{location_group_id}/zones` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::zone.get_zone_by_id`<a id="clickfunnelsshippingzoneget_zone_by_id"></a>

Retrieve a zone for a location group

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_zone_by_id_response = clickfunnels.shipping::zone.get_zone_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingZoneAttributes`](./click_funnels_python_sdk/pydantic/shipping_zone_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/shipping/zones/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::zone.list_zones`<a id="clickfunnelsshippingzonelist_zones"></a>

List zones for a location group

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_zones_response = clickfunnels.shipping::zone.list_zones(
    location_group_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### location_group_id: `int`<a id="location_group_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingZoneListZonesResponse`](./click_funnels_python_sdk/pydantic/shipping_zone_list_zones_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/shipping/location_groups/{location_group_id}/zones` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::zone.remove_by_id`<a id="clickfunnelsshippingzoneremove_by_id"></a>

Delete a zone for a location group

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
clickfunnels.shipping::zone.remove_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/shipping/zones/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.shipping::zone.update_zone_by_id`<a id="clickfunnelsshippingzoneupdate_zone_by_id"></a>

Update a zone for a location group

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_zone_by_id_response = clickfunnels.shipping::zone.update_zone_by_id(
    id="id_example",
    shipping_zone={
        "name": "Bruce Marquardt",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### shipping_zone: `ShippingZoneParameters`<a id="shipping_zone-shippingzoneparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ShippingZoneUpdateZoneByIdRequest`](./click_funnels_python_sdk/type/shipping_zone_update_zone_by_id_request.py)
Information about updated fields in Zone

#### 🔄 Return<a id="🔄-return"></a>

[`ShippingZoneAttributes`](./click_funnels_python_sdk/pydantic/shipping_zone_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/shipping/zones/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.team.get_all`<a id="clickfunnelsteamget_all"></a>

List all teams for the current account

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_all_response = clickfunnels.team.get_all(
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`TeamGetAllResponse`](./click_funnels_python_sdk/pydantic/team_get_all_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/teams` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.team.get_single`<a id="clickfunnelsteamget_single"></a>

Retrieve a single team

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_single_response = clickfunnels.team.get_single(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`TeamAttributes`](./click_funnels_python_sdk/pydantic/team_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/teams/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.team.update_team_by_id`<a id="clickfunnelsteamupdate_team_by_id"></a>

List all teams for the current account

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_team_by_id_response = clickfunnels.team.update_team_by_id(
    id="id_example",
    team={
        "name": "Example Team",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### team: `TeamParameters`<a id="team-teamparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`TeamUpdateTeamByIdRequest`](./click_funnels_python_sdk/type/team_update_team_by_id_request.py)
Information about updated fields in Team

#### 🔄 Return<a id="🔄-return"></a>

[`TeamAttributes`](./click_funnels_python_sdk/pydantic/team_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/teams/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.user.get_single`<a id="clickfunnelsuserget_single"></a>

Retrieve a single user

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_single_response = clickfunnels.user.get_single(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`UserAttributes`](./click_funnels_python_sdk/pydantic/user_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/users/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.user.list_current_account_users`<a id="clickfunnelsuserlist_current_account_users"></a>

List all users for the current account

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_current_account_users_response = clickfunnels.user.list_current_account_users(
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`UserListCurrentAccountUsersResponse`](./click_funnels_python_sdk/pydantic/user_list_current_account_users_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.user.update_single_user`<a id="clickfunnelsuserupdate_single_user"></a>

Update a single user

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_single_user_response = clickfunnels.user.update_single_user(
    id="id_example",
    user={
        "email": "huong@stroman-kuhlman.co",
        "first_name": "Louis",
        "last_name": "Von",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### user: `UserParameters`<a id="user-userparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`UserUpdateSingleUserRequest`](./click_funnels_python_sdk/type/user_update_single_user_request.py)
Information about updated fields in User

#### 🔄 Return<a id="🔄-return"></a>

[`UserAttributes`](./click_funnels_python_sdk/pydantic/user_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/users/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.webhooks::outgoing::endpoint.create_new`<a id="clickfunnelswebhooksoutgoingendpointcreate_new"></a>

Add a new webhook endpoint to a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_response = clickfunnels.webhooks::outgoing::endpoint.create_new(
    workspace_id=1,
    webhooks_outgoing_endpoint={
        "url": "https://example.com/some-endpoint-url",
        "name": "Example Endpoint",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### webhooks_outgoing_endpoint: `WebhooksOutgoingEndpointParameters`<a id="webhooks_outgoing_endpoint-webhooksoutgoingendpointparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`WebhooksOutgoingEndpointCreateNewRequest`](./click_funnels_python_sdk/type/webhooks_outgoing_endpoint_create_new_request.py)
Information about a new Endpoint

#### 🔄 Return<a id="🔄-return"></a>

[`WebhooksOutgoingEndpointAttributes`](./click_funnels_python_sdk/pydantic/webhooks_outgoing_endpoint_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/webhooks/outgoing/endpoints` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.webhooks::outgoing::endpoint.get`<a id="clickfunnelswebhooksoutgoingendpointget"></a>

Retrieve a webhook endpoint for a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = clickfunnels.webhooks::outgoing::endpoint.get(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`WebhooksOutgoingEndpointAttributes`](./click_funnels_python_sdk/pydantic/webhooks_outgoing_endpoint_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/webhooks/outgoing/endpoints/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.webhooks::outgoing::endpoint.list_endpoints`<a id="clickfunnelswebhooksoutgoingendpointlist_endpoints"></a>

List webhook endpoints for a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_endpoints_response = clickfunnels.webhooks::outgoing::endpoint.list_endpoints(
    workspace_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`WebhooksOutgoingEndpointListEndpointsResponse`](./click_funnels_python_sdk/pydantic/webhooks_outgoing_endpoint_list_endpoints_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/webhooks/outgoing/endpoints` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.webhooks::outgoing::endpoint.update_endpoint`<a id="clickfunnelswebhooksoutgoingendpointupdate_endpoint"></a>

Update a webhook endpoint for a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_endpoint_response = clickfunnels.webhooks::outgoing::endpoint.update_endpoint(
    id="id_example",
    webhooks_outgoing_endpoint={
        "url": "https://example.com/some-endpoint-url",
        "name": "Example Endpoint",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### webhooks_outgoing_endpoint: `WebhooksOutgoingEndpointParameters`<a id="webhooks_outgoing_endpoint-webhooksoutgoingendpointparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`WebhooksOutgoingEndpointUpdateEndpointRequest`](./click_funnels_python_sdk/type/webhooks_outgoing_endpoint_update_endpoint_request.py)
Information about updated fields in Endpoint

#### 🔄 Return<a id="🔄-return"></a>

[`WebhooksOutgoingEndpointAttributes`](./click_funnels_python_sdk/pydantic/webhooks_outgoing_endpoint_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/webhooks/outgoing/endpoints/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.webhooks::outgoing::event.get_for_workspace`<a id="clickfunnelswebhooksoutgoingeventget_for_workspace"></a>

Retrieve an webhook event for a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_for_workspace_response = clickfunnels.webhooks::outgoing::event.get_for_workspace(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`WebhooksOutgoingEventAttributes`](./click_funnels_python_sdk/pydantic/webhooks_outgoing_event_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/webhooks/outgoing/events/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.webhooks::outgoing::event.list_for_workspace`<a id="clickfunnelswebhooksoutgoingeventlist_for_workspace"></a>

List webhook events for a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_for_workspace_response = clickfunnels.webhooks::outgoing::event.list_for_workspace(
    workspace_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### workspace_id: `int`<a id="workspace_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`WebhooksOutgoingEventListForWorkspaceResponse`](./click_funnels_python_sdk/pydantic/webhooks_outgoing_event_list_for_workspace_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{workspace_id}/webhooks/outgoing/events` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.workspace.add_new`<a id="clickfunnelsworkspaceadd_new"></a>

Add a new workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
add_new_response = clickfunnels.workspace.add_new(
    team_id=1,
    workspace={
        "name": "Example Workspace",
        "subdomain": "example",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### team_id: `int`<a id="team_id-int"></a>

##### workspace: `WorkspaceParameters`<a id="workspace-workspaceparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`WorkspaceAddNewRequest`](./click_funnels_python_sdk/type/workspace_add_new_request.py)
Information about a new Workspace

#### 🔄 Return<a id="🔄-return"></a>

[`WorkspaceAttributes`](./click_funnels_python_sdk/pydantic/workspace_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/teams/{team_id}/workspaces` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.workspace.get_by_id`<a id="clickfunnelsworkspaceget_by_id"></a>

Retrieve a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_by_id_response = clickfunnels.workspace.get_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`WorkspaceAttributes`](./click_funnels_python_sdk/pydantic/workspace_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.workspace.list_workspaces`<a id="clickfunnelsworkspacelist_workspaces"></a>

List workspaces for a team

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_workspaces_response = clickfunnels.workspace.list_workspaces(
    team_id=1,
    after="string_example",
    sort_order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### team_id: `int`<a id="team_id-int"></a>

##### after: `str`<a id="after-str"></a>

ID of item after which the collection should be returned

##### sort_order: `str`<a id="sort_order-str"></a>

Sort order of a list response. Use 'desc' to reverse the default 'asc' (ascending) sort order.

#### 🔄 Return<a id="🔄-return"></a>

[`WorkspaceListWorkspacesResponse`](./click_funnels_python_sdk/pydantic/workspace_list_workspaces_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/teams/{team_id}/workspaces` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `clickfunnels.workspace.update`<a id="clickfunnelsworkspaceupdate"></a>

Update a workspace

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_response = clickfunnels.workspace.update(
    id="id_example",
    workspace={
        "name": "Example Workspace",
        "subdomain": "example",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### workspace: `WorkspaceParameters`<a id="workspace-workspaceparameters"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`WorkspaceUpdateRequest`](./click_funnels_python_sdk/type/workspace_update_request.py)
Information about updated fields in Workspace

#### 🔄 Return<a id="🔄-return"></a>

[`WorkspaceAttributes`](./click_funnels_python_sdk/pydantic/workspace_attributes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/workspaces/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---


## Author<a id="author"></a>
This Python package is automatically generated by [Konfig](https://konfigthis.com)
