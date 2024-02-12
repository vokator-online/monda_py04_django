# Functional permissioned CRUD Views

We have created most important CRUD based workflow for a permissioned object Project last time. Now we will improve our Task views with similar functionality but keep them function based. Later you will have an option to refactor all of them to class based views.

## Objectives

Update these views:
* `task_list` to get filters by user and project, and search function
* add a link to project and owner's management controls to `taks_detail`
* create `task_create` for logged in user
* create `task_update` and `task_delete` for task owner
* fix `task_done` permissions to limit task and related project owners to be able to mark task done
* `index` to get more statistical metrics and re-style the dashboard

## Filters for the Task List view

Let's begin with something simple - adding a few filters to the `task_list` viwq:

