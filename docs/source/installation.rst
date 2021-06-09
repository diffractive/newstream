.. _installation:

*************
Installation
*************

Google Cloud
============

The simplest way to deploy Newstream is via Google Cloud. You will need to configure the following

* :ref:`setup-google-cloud-project`
* :ref:`setup-google-cloud-sql`
* :ref:`setup-google-secret-manager`
* :ref:`setup-mailgun`
* Google Cloud Run
* Access newstream site

Once the site is up and running, there is some additional configuration you can apply

* Domain Mapping (essential)
* Google Cloud Storage (optional)

And if you wanting to customise newstream, beyond what is possible via the admin interface, please see

* Google Container Registry (optional)
* Building custom images
* Deploying custom images

----

.. _setup-google-cloud-project:

Google Cloud Project
--------------------

Sign up for Google Cloud at https://cloud.google.com/

Create a new project to deploy newstream. We recommend that you create a “Newstream Staging” project first to test everything out, before setting up “Newstream Production”. 

You can keep the staging project to test any future changes / upgrades before updating production.

.. image:: images/google-cloud-add-project.png
  :width: 400
  :alt: Google Cloud Add Project

----

.. _setup-google-cloud-sql:

Google Cloud SQL
----------------

The Google Cloud SQL database will hold all of your user data, as well as the site configuration and page content. We chose the lowest cost options available.

If you are wanting additional performance or reliability, you may want to adjust some of the settings here. Given the nature of the system (infrequent usage, low concurrency) it’s unlikely that this is required.

Go to `Database > SQL` from the Google Cloud console and choose to create an instance

.. image:: images/google-cloud-sql-new-instance.png
  :width: 400
  :alt: Google Cloud SQL New Instance

We want to use PostgreSQL as the database backend

.. image:: images/google-cloud-sql-choose-engine.png
  :width: 400
  :alt: Google Cloud Add Choose Engine

Enter the instance details

* Instance ID: newstream-db
* Password: Generate from interface, but you don't need to copy this

.. image:: images/google-cloud-sql-new-instance-info.png
  :width: 400
  :alt: Google Cloud SQL Instance Info

Set the region you are deploying to. Note that we don’t enable high availability, as it increases the cost significantly.

.. image:: images/google-cloud-sql-set-region-ha.png
  :width: 400
  :alt: Google Cloud SQL Instance Info

Under *Customise your instance* choose *Show Configuration Options* to set the next two

.. image:: images/google-cloud-sql-customise-instance.png
  :width: 400
  :alt: Google Cloud SQL Instance Info

Set the storage to 10GB on HDD

.. image:: images/google-cloud-sql-set-storage-type.png
  :width: 400
  :alt: Google Cloud SQL Instance Info

Set the machine type to “Shared core” with 1vCPU and 0.614GB of RAM

.. image:: images/google-cloud-sql-set-instance-type.png
  :width: 400
  :alt: Google Cloud SQL Instance Info

All other settings can be left as default. Now that the instance is running, you will need to create a database. Go to Databases > Create Databaseand create the newstream database

Finally, you need to create a user account. Go to `Users > Create User` and create a user newstream. Enter a randomly generated password, and save this for later - you will it when adding secrets to Google Secret Manager

----

.. _setup-google-secret-manager:

Google Secret Manager
---------------------

The Google Cloud SQL database will hold all of your user data, as well as the site configuration and page content. We chose the lowest cost options available.

.. _setup-mailgun:

Mailgun
-------

There are multiple email providers available for sending email. See https://cloud.google.com/compute/docs/tutorials/sending-mail for more details.
Other options recommended by Google are

* Sendgrid
* Mailgun
* Mailjet
* Google Workspace

Mailgun is a good option for medium volume sites due to it's pay as you go pricing model. Other services are free, but only for a limited number of
emails per day, which may cause problems during fundraising campaigns if a large number of donors register at once. Note that Google Workspace isn't
free as it requires a user account to be configured.





